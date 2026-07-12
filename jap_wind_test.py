from copy import deepcopy
import json
import os
import sqlite3
import urllib.error
import urllib.request
import pandas as pd
from random import sample,shuffle

from PyQt5.QtWidgets import QMainWindow, QFrame, QTableWidgetItem,QTableWidget, QScrollArea, QLabel, QComboBox, QLineEdit,QCheckBox, QRadioButton, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,QMenu,QAction,QApplication,QMessageBox,QTextEdit, QSizePolicy, QWidget, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QCloseEvent

from others_scripts import resource_path, BackgroundScrollArea, cell_has_value, merge_by_column, i_get_read
import styles as st
import stats_script as stat
from stats_script import STATS_SOURCES
from ai_settings import load_ai_secrets, ai_secrets_complete



class Rand_window(QMainWindow):
    # Columns tracked by SRS stats (Words: reading is in the Read column, not Kun)
    _STAT_COLUMNS = ('Kanji', 'Trans', 'Kun', 'Read')
    # Only the main test tables (no stats tables like kanji_* / words_* etc.)
    _TEST_TABLE_ORDER = ('Kanji', 'Words', 'Frazes', 'Name', 'Kana')
    _SHEETS_WITH_SUSH = ('Kanji', 'Kana')
    _SHEETS_WITH_STATS = frozenset(STATS_SOURCES)

    def __init__(self):
        super().__init__()
        japanese_logo_path = resource_path('japanese_logo.png')
        self.setWindowIcon(QIcon(japanese_logo_path)) # window icon
        self.setWindowTitle('Testing')
        QApplication.setFont(QFont("Roboto  ", 10))
        self.load_data_from_db()
        self.all_of_lessons = ['Select one lesson']
        self.len_of_words = 0
        self.options_for_zero()
        self.main()

    def closeEvent(self, event: QCloseEvent):
        """On window close, save stats if the test was started."""
        self._save_all_stats()
        if getattr(self, 'conn', None) is not None:
            try:
                self.conn.close()
            except Exception:
                pass
        super().closeEvent(event)

    def _stats_table_prefix(self):
        entry = STATS_SOURCES.get(self.current_sheet)
        return entry[0] if entry else 'words'

    def _uses_stats(self):
        return (
            self.current_sheet in self._SHEETS_WITH_STATS
            and self.current_column in self._STAT_COLUMNS
        )

    def _get_stats_tables(self):
        """List of (answer_col, table_name) for the current table/column."""
        prefix = self._stats_table_prefix()
        column_part = (self.current_column or "").lower()
        return [(col, f"{prefix}_{column_part}_{col.lower()}") for col in (self.test_for_answer or [])]

    def _update_merged_stat(self, row, col, new_stat):
        """Updates one record in self.stats after record_*_db / set_difficulty_only_db."""
        num_key, item_key = stat.get_item_key(row, self.current_column, col)
        self.stats.setdefault(num_key, {})[item_key] = new_stat

    def _save_all_stats(self):
        """When using the DB, stats are saved immediately in record_*_db; this path is unused."""
        pass

    def _normalize_lesson_column(self, df):
        """
        Coerces Lesson to a number for any dictionary table.
        All non-numeric/empty values are dropped so range filters don't fail.
        """
        if 'Lesson' not in df.columns:
            return df
        df = df.copy()
        df['Lesson'] = pd.to_numeric(df['Lesson'], errors='coerce')
        df = df[df['Lesson'].notna()]
        df['Lesson'] = df['Lesson'].astype(int)
        return df

    def load_data_from_db(self):
        """Loads data from SQLite (Jp.db)."""
        self.db_path = os.path.join(os.path.dirname(__file__), 'Jp.db')

        # Close the previous connection to avoid accumulating open connections and holding a database lock
        old_conn = getattr(self, 'conn', None)
        if old_conn is not None:
            try:
                old_conn.close()
            except Exception:
                pass

        self.conn = sqlite3.connect(self.db_path, timeout=10)
        stat.ensure_all_stats_tables(self.conn)
        cur = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        all_table_names = [row[0] for row in cur.fetchall()]
        self.sheet_names = [n for n in self._TEST_TABLE_ORDER if n in all_table_names]
        if not self.sheet_names:
            # None of the expected tables exist — show all so the window doesn't crash
            self.sheet_names = all_table_names
        if 'Words' in self.sheet_names:
            self.df_w = pd.read_sql('SELECT * FROM "Words"', self.conn)
        else:
            self.df_w = pd.read_sql(
                f'SELECT * FROM "{self.sheet_names[0]}"', self.conn
            )
        self.df_w.columns = self.df_w.columns.astype(str).str.strip()
        self.df_w = self._normalize_lesson_column(self.df_w)
        self.alls_words = self.df_w.reset_index().to_dict('records')


    def options_for_zero(self):
        self.value_of_test = 0
        self.shet_know = 0 # counter of known/unknown words
        self.known_clicked = False
        self.per_element_clicked = False  # a per-option button was pressed (table)
        self.unknown_words = []
        self.current_word = None # current word
        self.showing_translation = True 
        self.mnemonic_text=''
        self.len_of_count_for_proc = 0
        self.current_word_test = None
        self.past_word = ''
        self.current_table_rows = []  # table rows for stats (multiple-answers mode)
        self.clicked_columns_for_current = set()  # which columns (On/Kun/Trans) are marked for the current word
        self.all_variations = {}
        self.all_answers_variant = False  # "all answers" test variant (group by kanji/kun/on)
        self.answered_right_nums = set()  # Num of rows whose answer button was pressed (right)
        self.answered_right_pairs = set()  # (Num, col) — which (row, column) were pressed (for per-element buttons)


    def load_sheet_data(self, sheet_name):
        """Loads data of the selected DB table and updates the lesson fields."""
        self.df = pd.read_sql(f'SELECT * FROM "{sheet_name}"', self.conn)
        self.df.columns = self.df.columns.astype(str).str.strip()
        self.df = self._normalize_lesson_column(self.df)
        self.alls_dict = self.df.reset_index().to_dict('records')
        # Only numeric lessons, no nan; displayed as integers (40, not 40.0)
        valid = []
        for x in self.alls_dict:
            v = x.get('Lesson')
            try:
                if v is not None and v == v and str(v).strip() != '':
                    valid.append(int(float(v)))
            except (TypeError, ValueError):
                pass
        lessons = sorted(set(valid))
        self.len_of_words = max(lessons) if lessons else 0
        self.all_of_lessons = ['Select one lesson'] + [str(x) for x in lessons]
        if sheet_name in self._SHEETS_WITH_SUSH:
            self.chast_rechi = self.df['Sush'].unique().tolist()
        # Update the lesson widgets to the table's real lesson count
        self.ent_less.setText('1')
        self.ent_less_end.setText(str(self.len_of_words))
        self.lb_max_ur.setText(f'Total lessons = {self.len_of_words}')
        self.lb_err.setText('')
        self.choose_one_lesson.clear()
        self.choose_one_lesson.addItems(self.all_of_lessons)

    def main(self):
        self.setGeometry(300, 300, 480, 560)
        # The default table is the first one; parameters update when the table is switched
        self.current_sheet = self.sheet_names[0]

        self.frame_main = QFrame()
        self.frame_main.setStyleSheet("background-color: transparent;")

        # Table selection (in the same window as the parameters)
        self.context_menu = QMenu(self)
        self.sheets_dict = {}
        self.menu_button = QPushButton(self.current_sheet, self)
        self.menu_button.setStyleSheet(st.btn_test)
        self.menu_button.setFixedSize(400, 40)
        self.menu_button.setMenu(self.context_menu)
        for sheet_name in self.sheet_names:
            df = pd.read_sql(f'SELECT * FROM "{sheet_name}"', self.conn)
            df.columns = df.columns.astype(str).str.strip()
            columns = [col for col in df.columns if col not in ['Lesson', 'Num','Sush', 'Mnem']]
            self.sheets_dict[sheet_name] = columns
            action = QAction(sheet_name, self)
            action.triggered.connect(lambda checked, sheet_name=sheet_name: self.on_sheet_selected(sheet_name))
            self.context_menu.addAction(action)

        self.frame_rest = QFrame()
        self.frame_rest.setStyleSheet("background-color: transparent;")

        self.frame_up = QFrame()
        nbur = self.len_of_words
        self.label_type_of_test = QLabel('Select test type')
        self.chec_repeat_mode = QCheckBox('Repeat mode (normal + easy only)')
        self.chec_repeat_mode.setStyleSheet(st.checkbox)
        self.chec_type_of_test = QCheckBox ('Quiz mode with 4 answer choices,\n no stats')
        self.chec_all_answers = QCheckBox('All-answers variant')
        self.chec_all_answers.setStyleSheet(st.checkbox)
        self.chec_type_of_test.stateChanged.connect(self._on_type_of_test_changed)
        self.chec_repeat_mode.stateChanged.connect(self._on_repeat_mode_changed)
        self.lb_start = QLabel('First lesson')
        self.ent_less = QLineEdit(text='1')
        self.ent_less.setStyleSheet(st.but_line_check)
        self.lb_end = QLabel('Last lesson')
        self.ent_less_end = QLineEdit(text=str(nbur))
        self.all_test_without_filter = QCheckBox('All words without filtering')
        self.all_test_without_filter.setStyleSheet(st.checkbox)

        self.choose_one_lesson = QComboBox()
        self.choose_one_lesson.addItems([str(x) for x in self.all_of_lessons])
        self.choose_one_lesson.setFixedWidth(200)
        self.choose_one_lesson.setStyleSheet(st.combobox)

        self.ent_less_end.setStyleSheet(st.but_line_check)
        self.ent_less.setFixedWidth(50)
        self.ent_less_end.setFixedWidth(50)
        self.lb_err = QLabel('')
        self.lb_err.setStyleSheet(st.lb_err)
        self.frame_center=QFrame()
        self.label = QLabel('Select what to test')
        self.label.setVisible(False)
        self.frame_center2=QFrame()
        self.frame_for_options1 = QFrame()
        self.frame_for_options2 = QFrame()
        self.frame_down = QFrame()
        self.lb_max_ur = QLabel(f'Total lessons = {self.len_of_words}')
        self.btn3 = QPushButton("Enable test")
        self.btn3.setVisible(False)
        self.btn3.setStyleSheet(st.btn_test)
        self.btn3.setFixedSize(400, 50)
        self.choose_lang = QLabel('Select test subject')
        self.choose_lang.setVisible(False)
        layout_frame_up = QVBoxLayout()
        layout_frame_up.addWidget(self.label_type_of_test)
        layout_frame_up.addWidget(self.chec_repeat_mode)
        layout_frame_up.addWidget(self.chec_type_of_test)
        layout_frame_up.addWidget(self.chec_all_answers)
        layout_frame_up.addWidget(self.lb_start)
        if self.current_sheet == 'Kanji':
            self.chec_all_answers.setVisible(True)  # Kanji table only (has Kanji column)
        else:
            self.chec_all_answers.setVisible(False)
        layout_frame_up.addWidget(self.ent_less)
        layout_frame_up.addWidget(self.lb_end)
        layout_frame_up.addWidget(self.ent_less_end)
        layout_frame_up.addWidget(self.choose_one_lesson)
        layout_frame_up.addWidget(self.lb_max_ur)
        layout_frame_up.addWidget(self.all_test_without_filter)
        layout_frame_up.addWidget(self.choose_lang)
        self.frame_up.setLayout(layout_frame_up)

        self.layout_frame_centr1 = QVBoxLayout()        
        self.layout_frame_centr2 = QVBoxLayout()

        self.frame_center.setLayout(self.layout_frame_centr1)
        self.frame_center2.setLayout(self.layout_frame_centr2)

        self.layout_options1 = QHBoxLayout()
        self.frame_for_options1.setLayout(self.layout_options1)

        layout_frame_down = QVBoxLayout()
        layout_frame_down.addWidget(self.lb_err)
        layout_frame_down.addWidget(self.btn3)
        self.frame_down.setLayout(layout_frame_down)

        layout_frame_rest = QVBoxLayout()
        layout_frame_rest.addWidget(self.menu_button)
        layout_frame_rest.addWidget(self.frame_up)
        layout_frame_rest.addWidget(self.frame_center)
        layout_frame_rest.addWidget(self.label)
        layout_frame_rest.addWidget(self.frame_center2)
        layout_frame_rest.addWidget(self.frame_for_options1)
        layout_frame_rest.addWidget(self.frame_down)
        self.frame_rest.setLayout(layout_frame_rest)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.frame_rest)
        self.frame_main.setLayout(main_layout)
        self.scroll_with_backgr()
        self.btn3.clicked.connect(self.checks)
        self.load_sheet_data(self.current_sheet)
        self.build_sheet_options()

    def scroll_with_backgr(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        background_image_path2 = resource_path('japanese_background2.png')
        self.scroll_area = BackgroundScrollArea(background_image_path2)
        self.scroll_area.setWidget(self.frame_main)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(st.scroll)
        self.setCentralWidget(self.scroll_area)

    def on_sheet_selected(self, sheet_name):
        """Table selection: refresh lessons and options in the parameters window."""
        self.menu_button.setText(sheet_name)
        self.current_sheet = sheet_name
        self.load_sheet_data(sheet_name)
        self.build_sheet_options()

    def build_sheet_options(self):
        """Builds the column radio buttons and (for Kanji) part-of-speech checkboxes."""
        self.clear_layout(self.layout_frame_centr1)
        self.clear_layout(self.layout_frame_centr2)
        self.choose_lang.setVisible(True)
        self.label.setVisible(False)
        self.btn3.setVisible(False)
        # "All-answers variant" only for the Kanji table tab
        self.chec_all_answers.setVisible(self.current_sheet == 'Kanji')
        columns = self.get_filtered_columns(self.current_sheet)
        for column in columns:
            radio_button = QRadioButton(column, self)
            radio_button.setStyleSheet(st.radios)
            radio_button.clicked.connect(lambda checked, column=column: self.on_column_selected(column))
            self.layout_frame_centr1.addWidget(radio_button)
        if self.current_sheet in self._SHEETS_WITH_SUSH:
            self.clear_layout(self.layout_options1)
            self.checkboxes = []
            for i in range(len(self.chast_rechi)):
                self.checkboxes.append(QCheckBox(self.chast_rechi[i]))
                self.checkboxes[i].setChecked(True)
                self.checkboxes[i].setStyleSheet(st.checkbox)
                self.layout_options1.addWidget(self.checkboxes[i])
        else:
            self.clear_layout(self.layout_options1)

    def get_filtered_columns(self, sheet_name):
        """Returns the table's columns without the service columns."""
        sheet = pd.read_sql(f'SELECT * FROM "{sheet_name}"', self.conn)
        sheet.columns = sheet.columns.astype(str).str.strip()
        columns = list(sheet.columns)
        excluded_columns = ['Lesson', 'Num','Sush', 'Mnem']
        return [col for col in columns if col not in excluded_columns]

    def on_column_selected(self, column):
        # Clear the current layer of checkboxes
        self.clear_layout(self.layout_frame_centr2)
        self.label.setVisible(True)
        self.btn3.setVisible(True)
        self.current_column = column
        # Get the list of all unique values in the selected column
        values = self.get_unique_values(self.current_sheet, column)
        if 'Mnem' in values:
            values.remove('Mnem')
        # Add a checkbox for each unique value
        self.checkbox_for_test = []
        for value in values:
            if value == '':
                # Skip empty values
                continue
            checkbox = QCheckBox(str(value), self)
            checkbox.setStyleSheet(st.checkbox)
            self.checkbox_for_test.append(checkbox)
            self.layout_frame_centr2.addWidget(checkbox)

    def get_unique_values(self,sheet_name, column):
        need_column = deepcopy(self.sheets_dict[sheet_name])
        need_column.remove(column)
        return need_column

    def clear_layout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _answer_columns_for_stats(self):
        """Answer columns tracked by stats (including On)."""
        return list(self.test_for_answer) if self.test_for_answer else []

    def _columns_with_value(self, row):
        """Columns from test_for_answer that are non-empty and not '0' in the row (we don't record zeros in stats)."""
        return [c for c in self.test_for_answer if str(row.get(c, '')).strip() and str(row.get(c, '')) != '0']

    def _on_type_of_test_changed(self):
        """When the 4-choice test is enabled, disable the "All-answers variant"."""
        if self.chec_type_of_test.isChecked():
            self.chec_all_answers.setChecked(False)
            self.chec_all_answers.setEnabled(False)
        else:
            self.chec_all_answers.setEnabled(True)

    def _on_repeat_mode_changed(self):
        """When repeat mode is enabled, disable quiz mode (4 choices, no stats)."""
        if self.chec_repeat_mode.isChecked():
            self.chec_type_of_test.setChecked(False)
            self.chec_type_of_test.setEnabled(False)
        else:
            self.chec_type_of_test.setEnabled(True)

    def checks(self):
        if self.chec_type_of_test.isChecked():
            self.value_of_test = 1  # Quiz mode with 4 answer choices
        else:
            self.value_of_test = 0 # standard test
        self.all_answers_variant = self.chec_all_answers.isChecked() if hasattr(self, 'chec_all_answers') else False
        self.test_for_answer=[]
        self.property_choose = []
        for rb in self.checkbox_for_test:
            if rb.isChecked():
                self.test_for_answer.append(rb.text())
        if self.current_sheet in self._SHEETS_WITH_SUSH:
            for rb in self.checkboxes:
                if rb.isChecked():
                    self.property_choose.append(rb.text())
        if self.test_for_answer == []:
            self.lb_err.setText('Select at least one\n option to test')
        elif self.property_choose == [] and self.current_sheet in self._SHEETS_WITH_SUSH:
            self.lb_err.setText('Select at least one\n property to test')
        else:
            if len(self.test_for_answer) >1 and self.value_of_test == 1: # quiz mode with 4 answer choices
                self.lb_err.setText('For this test type, select\nonly one option to test')
            elif len(self.test_for_answer) >1 and self.all_answers_variant: # "all answers" test variant
                self.lb_err.setText('For the all-answers test\nselect only one option\n to test')
            else:
                self.lb_err.setText('')
                self.df2 = pd.read_sql(f'SELECT * FROM "{self.current_sheet}"', self.conn)
                self.df2.columns = self.df2.columns.astype(str).str.strip()
                self.df2 = self._normalize_lesson_column(self.df2)
                self.alls  = self.df2.reset_index().to_dict('records')
                self.lb_err.setText('')
                if self.choose_one_lesson.currentText() =='Select one lesson':
                    if self.ent_less.text() == '' or self.ent_less_end.text() == '':
                        self.lb_err.setText('Enter a lesson number')
                    else:
                        self.st = int(self.ent_less.text())
                        self.en = int(self.ent_less_end.text())

                        if self.st == 0 or self.en == 0:
                            self.lb_err.setText('Enter a lesson number')
                        elif self.st > self.en:
                            self.lb_err.setText('First lesson is greater than the last')
                        elif self.en > self.len_of_words:
                            self.lb_err.setText('Last lesson is greater than the maximum')
                        elif self.st == None or self.en == None:
                            self.lb_err.setText('Enter a lesson number')
                        else:
                            self.continue_check()
                else:
                    self.continue_check()

    def continue_check(self):
        self.lb_err.setText('')
        if self.choose_one_lesson.currentText() =='Select one lesson':
            self.alls =  [i for i in self.alls if (i['Lesson'] >= self.st and i['Lesson'] <= self.en)]  
        else:
            self.alls =  [i for i in self.alls if i['Lesson'] == int(self.choose_one_lesson.currentText())]
        if self.current_sheet in self._SHEETS_WITH_SUSH:
            self.alls = [i for i in self.alls if i['Sush'] in self.property_choose]
        if len(self.test_for_answer) == 1:
            self.alls_for_copy = [i for i in self.alls if str(i[self.test_for_answer[0]]) != '0' and str(i[self.current_column]) != '0']
        else:
            self.alls_for_copy = [i for i in self.alls if str(i[self.current_column]) != '0']
        self.alls = deepcopy(self.alls_for_copy)
        self.current_answer_column = self.test_for_answer[0] if self.test_for_answer else None
        self.stats_tables = self._get_stats_tables()
        self.stats_tables_dict = dict(self.stats_tables)  # col -> table_name
        self.stats = stat.load_stats_from_db(self.conn, self.stats_tables)
        if getattr(self, "chec_repeat_mode", None) is not None and self.chec_repeat_mode.isChecked():
            self.alls = stat.filter_items_for_repeat(
                self.alls, self.stats, self.current_column,
                answer_columns=list(self.test_for_answer) if self.test_for_answer else None
            )
        elif not self.all_test_without_filter.isChecked():
            self.alls = stat.filter_items_for_test(
                self.alls, self.stats, self.current_column,
                answer_columns=list(self.test_for_answer) if self.test_for_answer else None
            )
        self.len_of_count_for_proc = len(self.alls)
        self.alls = stat.sort_items_for_choice_test(self.alls, self.stats, self.current_column, self.current_answer_column)
        if self.value_of_test == 1: # quiz mode with 4 answer choices
            self._apply_choice_test_merge()
            if len(self.alls) <=3:
                self.lb_err.setText('Too few words for a 4-choice quiz')
                return
        self.main2()


    def main2(self):
        self.frame_main.deleteLater()
        self.setGeometry(300, 300, 700, 750)  # Taller window for the table
        self._test_content_width = 660
        self.frame_main = QFrame()
        self.frame_main.setStyleSheet("background-color: transparent;")

        self.frame_up2 = QFrame()
        self.frame_down2 = QFrame()
        self.frame_know = QFrame()
        self.btn_back = QPushButton("Back to main menu")
        self.btn_back.setStyleSheet(st.but_line_check)

        layout_frame_up2 = QHBoxLayout()
        layout_frame_up2.addWidget(self.btn_back)
        self.frame_up2.setLayout(layout_frame_up2)

        self.btn_continue = QPushButton("Start test")
        self.btn_continue.setStyleSheet(st.btn_test) 
        self.btn_continue.setFixedHeight(40)
        self.btn_continue.setFixedWidth(400)
        self.label_total = QLabel("Total words")
        self.mnemonic_text = QLabel("")
        self.mnemonic_text.setStyleSheet("color: #8B0000;")
        self.name_of_difficulty = QLabel("")
        self.part_of_speech = QLabel("")
        self.label_question = QTextEdit()  # Word
        self.label_question.setReadOnly(True)  # Make it read-only.
        self.label_question.setFrameStyle(QFrame.NoFrame)  # No border.
        self.label_question.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No vertical scroll bar.
        self.label_question.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No horizontal scroll bar.
        self.label_answer = QTextEdit("")    # Translation
        self.label_answer.setReadOnly(True)  # Make it read-only.
        self.label_answer.setFrameStyle(QFrame.NoFrame)  # No border.
        self.label_answer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No vertical scroll bar.
        self.label_answer.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No horizontal scroll bar.
        self.where_in_words_label = QLabel("")  # Which entries in the Words table contain this word
        font1 = QFont()
        font2 = QFont()
        if self.current_column =='Kanji':
            font1.setPointSize(40)
            font2.setPointSize(18)
        elif len(self.test_for_answer) == 1 and self.test_for_answer[0] == 'Kanji':
            font1.setPointSize(18)
            font2.setPointSize(40)
        else:
            font1.setPointSize(18)
            font2.setPointSize(18)
        self.label_question.setFont(font1)
        self.label_answer.setFont(font2)
        layout_frame_down2 = QVBoxLayout()
        layout_continue_row = QHBoxLayout()
        self.context_button = QPushButton("Context")
        self.context_button.setVisible(False)
        self.context_button.setStyleSheet(st.btn_test)
        self.context_button.setFixedHeight(40)
        self.context_button.setFixedWidth(140)
        self.context_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout_continue_row.addWidget(self.btn_continue)
        layout_continue_row.addWidget(self.context_button)
        layout_frame_down2.addLayout(layout_continue_row)
        layout_frame_down2.addWidget(self.label_total)
        layout_frame_down2.addWidget(self.mnemonic_text)
        layout_frame_down2.addWidget(self.name_of_difficulty)
        layout_frame_down2.addWidget(self.part_of_speech)
        layout_frame_down2.addWidget(self.label_question)
        layout_frame_down2.addWidget(self.where_in_words_label)
        self.frame_down2.setLayout(layout_frame_down2)

        layout_frame_know = QVBoxLayout()
        layout_context = QVBoxLayout()
        layout_buttons_row = QHBoxLayout()
        self.but_know = QPushButton("Know")
        self.but_know.setVisible(False)
        self.but_hard = QPushButton("Hard")
        self.but_hard.setVisible(False)
        self.but_hard.setStyleSheet(st.btn_test)
        self.but_easy = QPushButton("Easy")
        self.but_easy.setVisible(False)
        self.but_easy.setStyleSheet(st.btn_test)
        self.context_label = QLabel("")
        self.context_label.setVisible(False)
        self.context_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.context_label.setWordWrap(True)
        context_font = QFont()
        context_font.setPointSize(16)  # desired size
        self.context_label.setFont(context_font)
        self.but_know.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.but_hard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.but_easy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout_buttons_row.addWidget(self.but_know)
        layout_buttons_row.addWidget(self.but_hard)
        layout_buttons_row.addWidget(self.but_easy)
        layout_frame_know.addLayout(layout_buttons_row)
        self.table_widget = QTableWidget(self)
        self.table_widget.setMinimumHeight(300)  # Minimum table height
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.setWordWrap(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.setStyleSheet(st.table)
        if len(self.test_for_answer) == 1 and not getattr(self, 'all_answers_variant', False):
            self.table_widget.setVisible(False)
        elif getattr(self, 'all_answers_variant', False):
            # In the "all answers" variant, show the table only with multiple answer columns
            self.table_widget.setVisible(len(self.test_for_answer) > 1)
        else:
            self.table_widget.setVisible(len(self.test_for_answer) > 1)
        layout_frame_know.addWidget(self.table_widget, 1)  # Stretch factor = 1, table takes maximum space
        # Answer-option buttons (only with a table: multiple columns, without "all answers")
        self.frame_table_buttons = QFrame()
        self.layout_table_buttons = QHBoxLayout()
        self.frame_table_buttons.setLayout(self.layout_table_buttons)
        self.frame_table_buttons.setVisible(len(self.test_for_answer) > 1 and self.value_of_test == 0 and not getattr(self, 'all_answers_variant', False))
        self.table_column_buttons = []
        layout_frame_know.addWidget(self.frame_table_buttons)
        # "All answers" button block (one per group row) — only for the "all answers" variant
        self.frame_all_answer_buttons = QFrame()
        self.layout_all_answer_buttons = QGridLayout()
        self.frame_all_answer_buttons.setLayout(self.layout_all_answer_buttons)
        self.frame_all_answer_buttons.setVisible(False)
        self.answer_row_buttons = []  # per-row answer buttons (for all_answers_variant)
        layout_frame_know.addWidget(self.frame_all_answer_buttons)
        if self.value_of_test==0: # standard test
            layout_frame_know.addWidget(self.label_answer)
        else: # Quiz mode with 4 answer choices
            self.checkBoxes_in_test = []
            for _ in range(4):
                checkBox, row_widget = self._create_answer_checkbox()
                self.checkBoxes_in_test.append(checkBox)
                layout_frame_know.addWidget(row_widget)
            for checkBox in self.checkBoxes_in_test:
                self._set_answer_checkbox_visible(checkBox, False)
        layout_context.addWidget(self.context_label)
        layout_frame_know.addLayout(layout_context)
        self.frame_know.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.frame_know.setLayout(layout_frame_know)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.frame_up2)
        self.main_layout.addWidget(self.frame_down2)
        self.main_layout.addWidget(self.frame_know, 1)
        self.frame_main.setLayout(self.main_layout)
        self.frame_main.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.scroll_with_backgr()
        if self.value_of_test==0: # стандартный тест 
            self.btn_continue.clicked.connect(self.show_next_word)
        else:
            self.btn_continue.clicked.connect(self.show_next_word2)
        self.but_know.clicked.connect(self.know)
        self.but_hard.clicked.connect(self.on_hard_clicked)
        self.but_easy.clicked.connect(self.on_easy_clicked)
        self.context_button.clicked.connect(self.on_context_clicked)
        self.btn_back.clicked.connect(self.back)

    def repeat_frame(self):
        self.frame_repeat = QFrame()
        self.layout_frame_repeat = QVBoxLayout()  # Block for repeat, returned-words stats and the "Repeat" button
        self.label_end = QLabel("")
        self.label_count_right = QLabel("")
        self.again_but = QPushButton("Repeat")
        self.again_but.setFixedHeight(40)
        self.again_but.setFixedWidth(400)
        self.again_but.setVisible(False)
        self.again_but.setStyleSheet(st.btn_test)
        self.again_unknow = QPushButton("Repeat unrecognized words")
        self.again_unknow.setVisible(False)
        self.again_unknow.setStyleSheet(st.btn_test)
        self.again_unknow.setFixedHeight(40)
        self.again_unknow.setFixedWidth(400)
        self.again_label = QLabel("")
        if self.value_of_test ==1: # quiz mode with 4 answer choices
            # remove all checkboxes
            for checkBox in self.checkBoxes_in_test:
                self._set_answer_checkbox_visible(checkBox, False)
        self.layout_frame_repeat.addWidget(self.label_end)
        self.layout_frame_repeat.addWidget(self.label_count_right)
        self.layout_frame_repeat.addWidget(self.again_but)
        self.layout_frame_repeat.addWidget(self.again_label)
        self.layout_frame_repeat.addWidget(self.again_unknow)
        self.again_but.clicked.connect(self.reset_test)
        self.again_unknow.clicked.connect(self.retry_unknown_words)
        self.frame_repeat.setLayout(self.layout_frame_repeat)
        self.main_layout.addWidget(self.frame_repeat)

    def retry_unknown_words(self):
        self.shet_know = 0
        self.alls = self.unknown_words
        self.len_of_count_for_proc = len(self.alls)
        self.unknown_words = []
        self.options_for_again()

    def keyPressEvent(self, event):
        if self.value_of_test == 0: # standard test
            if event.key() == Qt.Key_Space:
                self.show_next_word()
            if event.key() == Qt.Key_Return:
                self.know()
    
    def _create_answer_checkbox(self):
        row_widget = QWidget()
        row_widget.setMaximumWidth(self._test_content_width)
        layout = QHBoxLayout(row_widget)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(8)
        checkBox = QCheckBox()
        label = QLabel("")
        label.setWordWrap(True)
        label.setMaximumWidth(self._test_content_width - 28)
        label.setStyleSheet("margin: 0; padding: 0;")
        answer_font = QFont('Arial', 16)
        label.setFont(answer_font)
        layout.addWidget(checkBox, 0, Qt.AlignVCenter)
        layout.addWidget(label, 1, Qt.AlignVCenter)

        def on_label_clicked(event, cb=checkBox, lbl=label):
            if event.button() == Qt.LeftButton and cb.isEnabled():
                cb.setChecked(not cb.isChecked())
            QLabel.mousePressEvent(lbl, event)

        label.mousePressEvent = on_label_clicked
        label.setCursor(Qt.PointingHandCursor)

        checkBox.answer_label = label
        checkBox.row_widget = row_widget
        checkBox.stateChanged.connect(self.checkAnswer)
        return checkBox, row_widget

    def _apply_choice_test_merge(self):
        """Merges rows with the same question value for the 4-choice test."""
        self.alls = merge_by_column(self.alls, self.current_column, self.test_for_answer[0])
        self.all_variations = deepcopy(self.alls)

    def _set_answer_checkbox_text(self, checkBox, text):
        checkBox.base_answer_text = text
        checkBox.answer_label.setText(text)
        checkBox.setToolTip(text)

    def _get_answer_checkbox_text(self, checkBox):
        return getattr(checkBox, 'base_answer_text', None) or checkBox.answer_label.text()

    def _reset_answer_checkbox(self, checkBox):
        checkBox.setStyleSheet("")
        checkBox.answer_label.setStyleSheet("")
        checkBox.setEnabled(True)
        checkBox.setChecked(False)
        checkBox.base_answer_text = ""
        self._set_answer_checkbox_text(checkBox, "")

    def _set_answer_checkbox_visible(self, checkBox, visible):
        checkBox.row_widget.setVisible(visible)

    def resetCheckBoxes(self):
        for checkBox in self.checkBoxes_in_test:
            self._reset_answer_checkbox(checkBox)

    def checkAnswer(self, state):
        if state == Qt.Checked:
            for checkBox in self.checkBoxes_in_test:
                checkBox.setEnabled(False)
                if checkBox.isChecked():
                    if checkBox.userData:
                        checkBox.answer_label.setStyleSheet("color: green;")
                        self._set_answer_checkbox_text(
                            checkBox,
                            self._get_answer_checkbox_text(checkBox) + " - Correct"
                        )
                        self.shet_know += 1
                    else:
                        checkBox.answer_label.setStyleSheet("color: red;")
                        self._set_answer_checkbox_text(
                            checkBox,
                            self._get_answer_checkbox_text(checkBox) + " - Wrong"
                        )
                        self.unknown_words.append(self.past_word)
                        for other in self.checkBoxes_in_test:
                            if other.userData:
                                other.answer_label.setStyleSheet("color: green;")
                                self._set_answer_checkbox_text(
                                    other,
                                    self._get_answer_checkbox_text(other) + " - Correct"
                                )
            self.btn_continue.setVisible(True)
            self.btn_continue.setText("Next word")
            self.context_button.setVisible(self._should_show_context_button())
            
            
            if self.current_sheet == 'Kanji' and self.current_column == 'Kanji':
                lines = []
                text=''
                for i in self.alls_words:
                    if self.current_word_test in i['Kanji'] and len(lines)<=5:
                        strings = str(i['Kanji'])+', '+i['Trans']
                        lines.append(strings)
                    if len(lines)>=1:
                        text = "Found in words:\n"+"\n".join(lines)
                        self.label_question.setToolTip(text)
                        self.label_question.setStyleSheet('QTextEdit {color: #8B0000;}')
            elif self.current_sheet == 'Kanji' and self.current_column =='Trans':
                lines = []
                text=''
                lines_translations2=[]
                for i in self.alls:
                    if i[self.current_column]==self.current_word_test:
                        lines_translations2.append(i[self.test_for_answer[0]])
                for j in lines_translations2:
                    for i in self.alls_words:
                        if j in i['Kanji'] and len(lines)<=5:
                            strings = str(i['Kanji'])+', '+i['Trans']
                            lines.append(strings)
                if len(lines)>=1:
                    text = "Found in words:\n"+"\n".join(lines)
                    self.label_question.setToolTip(text)
                    self.label_question.setStyleSheet('QTextEdit {color: #8B0000;}')
        else:
            self.label_question.setToolTip('')
            self.label_question.setStyleSheet('QTextEdit {color: #000000;}')
            self.context_button.setVisible(False)

    def _should_show_context_button(self):
        if not ai_secrets_complete():
            return False
        has_trans = self.current_column == 'Trans' or 'Trans' in self.test_for_answer
        has_kanji_or_kun = (
            self.current_column in ('Kanji', 'Kun', 'Read')
            or any(col in ('Kanji', 'Kun', 'Read') for col in self.test_for_answer)
        )
        return has_trans and has_kanji_or_kun

    def _has_meaningful_value(self, value):
        if value is None:
            return False
        if isinstance(value, str):
            value = value.strip()
            return value != "" and value != "0"
        return value != 0

    def _build_context_fields(self, word):
        trans = word.get('Trans')
        if not self._has_meaningful_value(trans):
            return None
        fields = {'Trans': str(trans).strip()}
        kanji = word.get('Kanji')
        kun = word.get('Kun') or word.get('Read')
        if self._has_meaningful_value(kanji):
            fields['Kanji'] = str(kanji).strip()
        if self._has_meaningful_value(kun):
            fields['Kun'] = str(kun).strip()
        return fields

    def _request_context_from_ai(self, fields):
        secrets = load_ai_secrets()
        api_key = secrets["AI_API_KEY"]
        if not api_key:
            return "API key not found. Fill in the AI settings."
        prompt = "Please write a sentence in Russian and in Japanese that can use this word. Return only the sentence, without comments or conclusions. If the data is insufficient or contradictory/erroneous, reply exactly: There is an error in the data."
        payload = {
            "model": secrets["AI_MODEL"],
            "messages": [
                {"role": "system", "content": "You are a Japanese language assistant."},
                {"role": "user", "content": f"{prompt}\n\nWord data: {json.dumps(fields, ensure_ascii=False)}"}
            ],
            "temperature": 0.7
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            secrets["AI_API_URL"],
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read().decode("utf-8")
            parsed = json.loads(body)
            choices = parsed.get("choices", [])
            if not choices:
                return "The AI returned no answer."
            content = choices[0].get("message", {}).get("content", "")
            return content.strip() if content else "The AI returned an empty answer."
        except urllib.error.HTTPError as e:
            err_text = e.read().decode("utf-8", errors="ignore")
            return f"API error ({e.code}): {err_text[:300]}"
        except Exception as e:
            return f"AI request error: {e}"

    def on_context_clicked(self):
        # Context is shown only after the answer is revealed/selected.
        if not self.showing_translation and self.value_of_test == 0:
            return
        if not self._should_show_context_button():
            return
        if not self.current_word:
            self.context_label.setText("No current word for context.")
            self.context_label.setVisible(True)
            return
        fields = self._build_context_fields(self.current_word)
        if not fields:
            self.context_label.setText("Could not collect word data for the request.")
            self.context_label.setVisible(True)
            return
        self.context_label.setText("Generating context...")
        QApplication.processEvents()
        ai_answer = self._request_context_from_ai(fields)
        self.context_label.setText(ai_answer)
        self.context_label.setVisible(True)

    def show_next_word(self):
        if self.showing_translation:
            self.btn_continue.setText("Show answer")
            self.table_widget.clearContents()
            self.label_question.setStyleSheet('QTextEdit {color: #000000;}')
            self.label_question.setToolTip('')
            self.but_know.setVisible(True)
            if not getattr(self, 'all_answers_variant', False):
                self.but_hard.setVisible(True)
                self.but_easy.setVisible(True)
            else:
                self.but_hard.setVisible(False)
                self.but_easy.setVisible(False)
            self.but_know.setDisabled(True)
            self.frame_table_buttons.setVisible(False)
            self.frame_all_answer_buttons.setVisible(False)
            self.context_button.setVisible(False)
            self.context_label.setVisible(False)
            self.context_label.setText("")
            self.but_know.setStyleSheet('QPushButton {background-color: red; color: white;}')
            self._reset_difficulty_buttons_style()
            self.but_hard.setEnabled(False)
            self.but_easy.setEnabled(False)
            self.showing_translation = False
            if self.past_word !='':
                if self.known_clicked == True:
                    self.known_clicked = False
                else:
                    # "Know" was not pressed — add to unlearned and record wrong for unmarked items
                    if getattr(self, 'all_answers_variant', False):
                        # "All answers" variant: wrong for unmarked (row, column) or for whole rows
                        if len(self.test_for_answer) > 1:
                            # Per-element buttons: wrong only for unpressed (row, col)
                            for row in getattr(self, 'current_table_rows', []):
                                missed = False
                                for col in self._columns_with_value(row):
                                    if (row.get('Num'), col) not in getattr(self, 'answered_right_pairs', set()):
                                        if col in self.stats_tables_dict:
                                            s = stat.record_wrong_db(self.conn, self.stats_tables_dict[col], row, self.current_column, col)
                                            self._update_merged_stat(row, col, s)
                                        missed = True
                                if missed:
                                    self.unknown_words.append(row)
                        else:
                            for row in getattr(self, 'current_table_rows', []):
                                if row.get('Num') not in getattr(self, 'answered_right_nums', set()):
                                    self.unknown_words.append(row)
                                    for col in self._columns_with_value(row):
                                        if col in self.stats_tables_dict:
                                            s = stat.record_wrong_db(self.conn, self.stats_tables_dict[col], row, self.current_column, col)
                                            self._update_merged_stat(row, col, s)
                    else:
                        self.unknown_words.append(self.past_word)
                        if self._uses_stats():
                            if len(self.test_for_answer) > 1:
                                # For the table: wrong only for columns that were not marked (Kanji/Kun/Trans)
                                for row in getattr(self, 'current_table_rows', []):
                                    for col in self._columns_with_value(row):
                                        if col not in getattr(self, 'clicked_columns_for_current', set()):
                                            if col in self.stats_tables_dict:
                                                s = stat.record_wrong_db(self.conn, self.stats_tables_dict[col], row, self.current_column, col)
                                                self._update_merged_stat(row, col, s)
                            else:
                                if self.current_answer_column and self.current_answer_column in self._columns_with_value(self.past_word):
                                    if self.current_answer_column in self.stats_tables_dict:
                                        s = stat.record_wrong_db(self.conn, self.stats_tables_dict[self.current_answer_column], self.past_word, self.current_column, self.current_answer_column)
                                        self._update_merged_stat(self.past_word, self.current_answer_column, s)
                self.per_element_clicked = False
                if getattr(self, 'all_answers_variant', False):
                    self._clear_all_answer_buttons()
                    self.answered_right_nums = set()
                    self.answered_right_pairs = set()
            if not self.alls: # If all words are exhausted
                self.past_word = ''
                self.label_question.setText("Test finished.")
                self.mnemonic_text.setText('')
                self.mnemonic_text.setToolTip('')
                self.name_of_difficulty.setText('')
                self.part_of_speech.setText('')
                self.table_widget.setVisible(False)
                self.label_total.setText('')
                self.label_answer.setText("")
                self.repeat_frame()
                self.again_but.setVisible(True)
                self.btn_continue.setVisible(False)
                self.but_know.setVisible(False)
                self.context_button.setVisible(False)
                self.context_label.setVisible(False)
                self.context_label.setText("")
                if not getattr(self, 'all_answers_variant', False):
                    self.but_hard.setVisible(False)
                    self.but_easy.setVisible(False)
                self.where_in_words_label.setText('')
                if getattr(self, 'all_answers_variant', False):
                    self._clear_all_answer_buttons()
                if len(self.unknown_words) > 0:
                    self.again_unknow.setVisible(True)
                if self.len_of_count_for_proc==0:
                    self.label_count_right.setText('No words for the test')
                else:
                    prots = int(round((100 / self.len_of_count_for_proc * self.shet_know), 2))
                    self.label_count_right.setText(f'Total={self.len_of_count_for_proc}, Correct={self.shet_know}, correct percentage = {prots}.')
                return

            if getattr(self, 'all_answers_variant', False):
                # Group by matching kanji/kun/on: all rows with the same current_column value
                first = self.alls[0]
                self.current_word_test = first[self.current_column]
                self.current_table_rows = [r for r in self.alls if r[self.current_column] == self.current_word_test]
                for r in self.current_table_rows:
                    if r in self.alls:
                        self.alls.remove(r)
                self.current_word = self.current_table_rows[0]
                self.answered_right_nums = set()
                self.answered_right_pairs = set()
            else:
                self.current_word = self.alls[0]
                self.current_word_test = self.current_word[self.current_column]
            num_key, item_key = stat.get_item_key(self.current_word, self.current_column, self.current_answer_column)
            difficulty = self.stats.get(num_key, {}).get(item_key, {}).get('difficulty', 'normal')
            self.name_of_difficulty.setText(f'Difficulty: {difficulty}')
            if len(self.property_choose) > 1 and not getattr(self, 'all_answers_variant', False):
                self.part_of_speech.setText(f'Part of speech: {self.current_word.get("Sush", "")}')
            for i in self.alls:
                if cell_has_value(i.get('Mnem')):
                    if i.get('Trans') == self.current_word['Trans'] or i_get_read(i, self.current_word, self.current_sheet):
                        self.mnemonic_text.setText('has mnemonic')
                        self.mnemonic_text.setToolTip(str(i['Mnem']))
                        break
                else:
                    self.mnemonic_text.setText('')
                    self.mnemonic_text.setToolTip('')
            self.past_word = self.current_word
            t = f'Word count= {len(self.alls)}'
            self.label_total.setText(t)
            if self.current_sheet == 'Kanji' and self.current_column == 'Kanji': # test type where kanji is shown first, then the translation
                lines = []
                text=''
                for i in self.alls_words:
                    if self.current_word_test in i['Kanji'] and len(lines)<=5:
                        lines.append(i['Trans'])
                    if len(lines)>=1:
                        text = "Found in words:\n"+"\n".join(lines)
                        self.label_question.setToolTip(text)
                        self.label_question.setStyleSheet('QTextEdit {color: #8B0000;}')
            elif self.current_sheet == 'Kanji' and self.current_column =='Trans':  # test type where the translation is shown first, then the kanji
                lines = [] # list of words that contain the kanji
                text=''
                lines_translations2=[]
                for i in self.alls:
                    if i[self.current_column]==self.current_word_test:
                        lines_translations2.append(i[self.test_for_answer[0]])
                for j in lines_translations2:
                    for i in self.alls_words:
                        if j in i['Kanji'] and len(lines)<=5:
                            lines.append(i['Trans'])
                if len(lines)>=1:
                    text = "Found in words:\n"+"\n".join(lines)
                    self.label_question.setToolTip(text)
                    self.label_question.setStyleSheet('QTextEdit {color: #8B0000;}')
            self.label_question.setText(self.current_word_test)
            self.label_answer.setText("")
        else:
            self.btn_continue.setText("Next word")
            self.but_know.setDisabled(False)
            self._reset_difficulty_buttons_style()
            self.but_hard.setEnabled(True)
            self.but_easy.setEnabled(False)  # "Easy" is available only after pressing "Know"
            self.showing_translation = True
            self.context_button.setVisible(self._should_show_context_button())
            self.context_label.setVisible(False)
            self.context_label.setText("")
            if self.current_sheet == 'Kanji' and self.current_column == 'Kanji':
                lines = []
                text=''
                for i in self.alls_words:
                    if self.current_word_test in i['Kanji'] and len(lines)<=5:
                        strings = str(i['Kanji'])+', '+i['Trans']
                        lines.append(strings)
                    if len(lines)>=1:
                        text = "Found in words:\n"+"\n".join(lines)
                        self.label_question.setToolTip(text)
                        self.label_question.setStyleSheet('QTextEdit {color: #8B0000;}')
            elif self.current_sheet == 'Kanji' and self.current_column =='Trans':
                lines = []
                text=''
                lines_translations2=[]
                for i in self.alls:
                    if i[self.current_column]==self.current_word_test:
                        lines_translations2.append(i[self.test_for_answer[0]])
                for j in lines_translations2:
                    for i in self.alls_words:
                        if j in i['Kanji'] and len(lines)<=5:
                            strings = str(i['Kanji'])+', '+i['Trans']
                            lines.append(strings)
                if len(lines)>=1:
                    text = "Found in words:\n"+"\n".join(lines)
                    self.label_question.setToolTip(text)
                    self.label_question.setStyleSheet('QTextEdit {color: #8B0000;}')
            
            if getattr(self, 'all_answers_variant', False):
                self._clear_all_answer_buttons()
                if len(self.current_table_rows) == 1:
                    # Single answer — show as text, like in normal mode
                    row = self.current_table_rows[0]
                    if len(self.test_for_answer) == 1:
                        self.label_answer.setText(str(row.get(self.test_for_answer[0], '')))
                    else:
                        parts = [str(row.get(p, '')) for p in self.test_for_answer]
                        self.label_answer.setText(" | ".join(parts))
                    self.frame_all_answer_buttons.setVisible(False)
                elif len(self.test_for_answer) > 1:
                    # Multiple answer columns: table + a button per element (study, まなぶ, ガク, ...)
                    self.label_answer.setText("")
                    self.update_table(
                        [self.current_word.get(p, '') for p in self.test_for_answer],
                        self.current_word_test,
                        multiple_words=self.current_table_rows,
                        remove_from_alls=False,
                        show_column_buttons=False
                    )
                    cols_per_row = 4
                    idx = 0
                    for row in self.current_table_rows:
                        for col in self._columns_with_value(row):
                            text = str(row.get(col, ''))
                            btn = QPushButton(text)
                            btn.setStyleSheet(st.btn_test)
                            btn._row_data = (row, col)
                            btn.clicked.connect(lambda checked, r=row, c=col: self._on_answer_element_clicked(r, c))
                            self.layout_all_answer_buttons.addWidget(btn, idx // cols_per_row, idx % cols_per_row)
                            self.answer_row_buttons.append(btn)
                            idx += 1
                    self.frame_all_answer_buttons.setVisible(True)
                else:
                    # Multiple rows, one column — one button per group row
                    self.label_answer.setText("")
                    cols_per_row = 3
                    for i, row in enumerate(self.current_table_rows):
                        text = str(row.get(self.test_for_answer[0], ''))
                        btn = QPushButton(text)
                        btn.setStyleSheet(st.btn_test)
                        btn._row_data = row
                        btn.clicked.connect(lambda checked, r=row: self._on_answer_row_clicked(r))
                        self.layout_all_answer_buttons.addWidget(btn, i // cols_per_row, i % cols_per_row)
                        self.answer_row_buttons.append(btn)
                    self.frame_all_answer_buttons.setVisible(True)
            elif len(self.test_for_answer) == 1:
                # Only one element — the answer of the current row, not all with the same kanji
                self.translations = str(self.current_word.get(self.test_for_answer[0], ''))
                self.label_answer.setText(self.translations)
                if self.current_word in self.alls:
                    self.alls.remove(self.current_word) 
            else:
                self.translations = [self.current_word[prop] for prop in self.test_for_answer]
                self.update_table(self.translations, self.current_word_test, single_word=self.current_word)

    def show_next_word2(self):
        self.resetCheckBoxes()
        self.context_button.setVisible(False)
        self.context_label.setVisible(False)
        self.context_label.setText("")
        for checkBox in self.checkBoxes_in_test:
                self._set_answer_checkbox_visible(checkBox, True)
        self.btn_continue.setVisible(False)   
        if not self.alls: # If all words are exhausted
            self.past_word = ''
            self.label_question.setText("Test finished.")
            self.mnemonic_text.setText('')
            self.mnemonic_text.setToolTip('')
            self.name_of_difficulty.setText('')
            self.table_widget.setVisible(False)
            self.label_total.setText('')
            self.label_answer.setText("")
            self.repeat_frame()
            self.again_but.setVisible(True)
            self.btn_continue.setVisible(False)
            if len(self.unknown_words) > 0:
                self.again_unknow.setVisible(True)
            if self.len_of_count_for_proc==0:
                self.label_count_right.setText('No words for the test')
            else:
                prots = int(round((100 / self.len_of_count_for_proc * self.shet_know), 2))
                self.label_count_right.setText(f'Total={self.len_of_count_for_proc}, Correct={self.shet_know}, correct percentage = {prots}.')
            return

        self.current_word = self.alls[0]
        self.current_word_test = self.current_word[self.current_column]
        num_key, item_key = stat.get_item_key(self.current_word, self.current_column, self.current_answer_column)
        difficulty = self.stats.get(num_key, {}).get(item_key, {}).get('difficulty', 'normal')
        self.name_of_difficulty.setText(f'Difficulty: {difficulty}')
        self.past_word = self.current_word

        for i in self.alls:
            if cell_has_value(i.get('Mnem')):
                if i.get('Trans') == self.current_word['Trans'] or i_get_read(i, self.current_word, self.current_sheet):
                    self.mnemonic_text.setText('has mnemonic')
                    self.mnemonic_text.setToolTip(str(i['Mnem']))
                    break
            else:
                self.mnemonic_text.setText('')
                self.mnemonic_text.setToolTip('')

        t = f'Word count= {len(self.alls)}'
        self.label_total.setText(t)
        if self.current_sheet == 'Words' and self.current_column == 'Kanji':
            reading = self.current_word_test + ' - ' + self.current_word['Read']
            self.label_question.setText(reading)
        else:
            self.label_question.setText(self.current_word_test)

        answer_col = self.test_for_answer[0]
        correct_answer = self.current_word[answer_col]
        correct_kanji = self.current_word.get('Kanji')
        question_val = self.current_word[self.current_column]

        # Candidates: not the current word; if a kanji exists — a different kanji
        filtered_words = [
            word for word in self.all_variations
            if word[self.current_column] != question_val
            and (not cell_has_value(correct_kanji) or word.get('Kanji') != correct_kanji)
        ]

        # Unique wrong answers (no repeat of the correct one and no duplicate rows)
        wrong_pool = []
        seen_answers = set()
        for word in filtered_words:
            ans = word[answer_col]
            if ans == correct_answer or ans in seen_answers:
                continue
            seen_answers.add(ans)
            wrong_pool.append(ans)

        if len(wrong_pool) < 3:
            if self.current_word in self.alls:
                self.alls.remove(self.current_word)
            self.show_next_word2()
            return

        wrong_answers = sample(wrong_pool, 3)

        # Mix the correct answer with the wrong ones
        all_answers = wrong_answers + [correct_answer]
        shuffle(all_answers)

        # Set the text for the checkboxes
        for i, checkBox in enumerate(self.checkBoxes_in_test):
            self._set_answer_checkbox_text(checkBox, all_answers[i])
            checkBox.setEnabled(True)
            checkBox.setChecked(False)
            checkBox.userData = (all_answers[i] == correct_answer)

        # Remove only the current word, not all with the same kanji/translation
        if self.current_word in self.alls:
            self.alls.remove(self.current_word)

    def reset_test(self):
        self.shet_know = 0
        self.alls = deepcopy(self.alls_for_copy)
        self.alls = stat.sort_items_for_choice_test(self.alls, self.stats, self.current_column, self.current_answer_column)
        if self.value_of_test == 1:
            self._apply_choice_test_merge()
        self.options_for_again()

    def options_for_again(self):
        if getattr(self, 'all_answers_variant', False):
            self.table_widget.setVisible(len(self.test_for_answer) > 1)
            self._clear_all_answer_buttons()
        elif len(self.test_for_answer)==1:
            self.table_widget.setVisible(False)
        else:
            self.table_widget.setVisible(True)
        self.current_word = None
        self.current_word_test = None
        self.showing_translation = True
        self.label_question.setText("")
        self.label_answer.setText("")
        self.context_button.setVisible(False)
        self.context_label.setVisible(False)
        self.context_label.setText("")
        self.label_count_right.setText('')
        self.again_but.setVisible(False)
        self.btn_continue.setVisible(True)
        self.frame_repeat.deleteLater()
        self.known_clicked = False
        if self.value_of_test ==0:
            self.show_next_word() # standard test
        else:
            self.show_next_word2() # quiz mode with 4 answer choices

    def _reset_difficulty_buttons_style(self):
        """Reset the Hard/Easy button styles to normal."""
        self.but_hard.setStyleSheet(st.btn_test)
        self.but_easy.setStyleSheet(st.btn_test)

    def on_hard_clicked(self):
        if not self.but_hard.isEnabled():
            return
        self.but_hard.setStyleSheet('QPushButton {background-color: lime; color: white;}')
        self.but_hard.setEnabled(False)
        self.but_easy.setEnabled(False)
        if self._uses_stats():
                if self.current_answer_column and self.current_answer_column in self._columns_with_value(self.current_word):
                    if self.current_answer_column in self.stats_tables_dict:
                        s = stat.set_difficulty_only_db(self.conn, self.stats_tables_dict[self.current_answer_column], self.current_word, "hard", self.current_column, self.current_answer_column)
                        self._update_merged_stat(self.current_word, self.current_answer_column, s)

    def on_easy_clicked(self):
        if not self.but_easy.isEnabled():
            return
        self.but_easy.setStyleSheet('QPushButton {background-color: lime; color: white;}')
        self.but_easy.setEnabled(False)
        self.but_hard.setEnabled(False)
        if self._uses_stats():
            if self.current_answer_column and self.current_answer_column in self._columns_with_value(self.current_word):
                if self.current_answer_column in self.stats_tables_dict:
                    s = stat.set_difficulty_only_db(self.conn, self.stats_tables_dict[self.current_answer_column], self.current_word, "easy", self.current_column, self.current_answer_column)
                    self._update_merged_stat(self.current_word, self.current_answer_column, s)

    def on_table_column_clicked(self, col):
        """Pressing the On/Kun/Trans button: right only for that column of the current row."""
        if not self._uses_stats():
            return
        rows = getattr(self, 'current_table_rows', [])
        if not rows or col not in self._columns_with_value(rows[0]):
            return
        self.clicked_columns_for_current.add(col)
        if col in self.stats_tables_dict:
            s = stat.record_correct_db(self.conn, self.stats_tables_dict[col], rows[0], self.current_column, col)
            self._update_merged_stat(rows[0], col, s)
        self.per_element_clicked = True
        self.but_know.setEnabled(False)
        self.but_know.setStyleSheet('QPushButton {background-color: gray; color: white;}')
        for btn in getattr(self, 'table_column_buttons', []):
            if btn.text() == col:
                btn.setEnabled(False)
                break

    def know(self):
        if self.showing_translation:  # Update stats only when the word is shown, not the translation
            if self.known_clicked == False:
                self.but_know.setStyleSheet('QPushButton {background-color: lime; color: white;}')
                if self._uses_stats():
                    if getattr(self, 'all_answers_variant', False):
                        # "All answers" variant: right for all rows of the group
                        for row in getattr(self, 'current_table_rows', []):
                            for col in self._columns_with_value(row):
                                if col in self.stats_tables_dict:
                                    s = stat.record_correct_db(self.conn, self.stats_tables_dict[col], row, self.current_column, col)
                                    self._update_merged_stat(row, col, s)
                    elif len(self.test_for_answer) > 1:
                        for row in getattr(self, 'current_table_rows', []):
                            for col in self._columns_with_value(row):
                                if col in self.stats_tables_dict:
                                    s = stat.record_correct_db(self.conn, self.stats_tables_dict[col], row, self.current_column, col)
                                    self._update_merged_stat(row, col, s)
                    else:
                        if self.current_answer_column and self.current_answer_column in self._columns_with_value(self.current_word):
                            if self.current_answer_column in self.stats_tables_dict:
                                s = stat.record_correct_db(self.conn, self.stats_tables_dict[self.current_answer_column], self.current_word, self.current_column, self.current_answer_column)
                                self._update_merged_stat(self.current_word, self.current_answer_column, s)
                self.shet_know += 1
                self.known_clicked = True
                if not getattr(self, 'all_answers_variant', False):
                    # "Easy" is available only after "Know" and only if the word is not marked hard
                    if self.current_answer_column and self.current_answer_column in self._columns_with_value(self.current_word):
                        self.but_easy.setEnabled(stat.can_press_easy_db(self.conn, self.stats_tables_dict[self.current_answer_column], self.current_word, self.current_column, self.current_answer_column))
                    else:
                        self.but_easy.setEnabled(True)

    def back(self):
        # Save stats once when leaving the test (instead of saving on every word)
        self._save_all_stats()
        self.load_data_from_db()
        self.options_for_zero()
        self.frame_main.deleteLater()
        self.main()       

    def _clear_all_answer_buttons(self):
        """Removes the answer buttons in the "all answers" variant."""
        self.answer_row_buttons.clear()
        while self.layout_all_answer_buttons.count():
            child = self.layout_all_answer_buttons.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.frame_all_answer_buttons.setVisible(False)

    def _on_answer_row_clicked(self, row):
        """Pressing one of the answer buttons: right for that row, "Know" is disabled."""
        if not self._uses_stats():
            return
        self.answered_right_nums.add(row.get('Num'))
        for col in self._columns_with_value(row):
            if col in self.stats_tables_dict:
                s = stat.record_correct_db(self.conn, self.stats_tables_dict[col], row, self.current_column, col)
                self._update_merged_stat(row, col, s)
        self.per_element_clicked = True
        self.but_know.setEnabled(False)
        self.but_know.setStyleSheet('QPushButton {background-color: gray; color: white;}')
        # Find the button for this row and make it green and disabled
        for btn in self.answer_row_buttons:
            if getattr(btn, '_row_data', None) and btn._row_data.get('Num') == row.get('Num'):
                btn.setEnabled(False)
                btn.setStyleSheet('QPushButton {background-color: lime; color: white;}')
                break

    def _on_answer_element_clicked(self, row, col):
        """Pressing a single element (cell) button: right for that (row, column), "Know" is disabled."""
        if not self._uses_stats():
            return
        self.answered_right_pairs.add((row.get('Num'), col))
        if col in self.stats_tables_dict:
            s = stat.record_correct_db(self.conn, self.stats_tables_dict[col], row, self.current_column, col)
            self._update_merged_stat(row, col, s)
        self.per_element_clicked = True
        self.but_know.setEnabled(False)
        self.but_know.setStyleSheet('QPushButton {background-color: gray; color: white;}')
        for btn in self.answer_row_buttons:
            data = getattr(btn, '_row_data', None)
            if data and isinstance(data, (tuple, list)) and len(data) == 2 and data[0].get('Num') == row.get('Num') and data[1] == col:
                btn.setEnabled(False)
                btn.setStyleSheet('QPushButton {background-color: lime; color: white;}')
                break

    def update_table(self, translations, current_word, single_word=None, multiple_words=None, remove_from_alls=True, show_column_buttons=True):
        # single_word / multiple_words — an explicit list of rows; otherwise taken from self.alls by current_word
        if multiple_words is not None:
            filtered_words = list(multiple_words)
        elif single_word is not None:
            filtered_words = [single_word]
        else:
            filtered_words = [i for i in self.alls if i[self.current_column] == current_word]

        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(len(self.test_for_answer) + 1)
        headers = [self.current_column] + list(self.test_for_answer)
        self.table_widget.setHorizontalHeaderLabels(headers)

        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        font = QFont()
        font.setPointSize(18)
        self.table_widget.setFont(font)
        self.table_widget.horizontalHeader().setFont(header_font)
        self.table_widget.verticalHeader().setFont(header_font)

        self.current_table_rows = list(filtered_words)
        self.clicked_columns_for_current = set()

        # Buttons by column name (On, Kun, Trans) — only when not in "per-element" mode
        self.clear_layout(self.layout_table_buttons)
        self.table_column_buttons.clear()
        if show_column_buttons and filtered_words:
            word = filtered_words[0]
            for col in self._columns_with_value(word):
                btn = QPushButton(col)
                btn.setStyleSheet(st.btn_test)
                btn.clicked.connect(lambda checked, c=col: self.on_table_column_clicked(c))
                self.layout_table_buttons.addWidget(btn)
                self.table_column_buttons.append(btn)
            self.frame_table_buttons.setVisible(True)
            self.frame_table_buttons.setMinimumHeight(50)
        else:
            self.frame_table_buttons.setVisible(False)

        for word in filtered_words:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            item = QTableWidgetItem(str(word.get(self.current_column, '')))
            self.table_widget.setItem(row, 0, item)
            for i, prop in enumerate(self.test_for_answer, 1):
                item = QTableWidgetItem(str(word.get(prop, '')))
                self.table_widget.setItem(row, i, item)
        if remove_from_alls:
            for w in filtered_words:
                if w in self.alls:
                    self.alls.remove(w)

        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.resizeRowsToContents()
                
'''
Notes:
self.current_column # the column chosen for the test — what is shown as the question
self.test_for_answer # list of chosen test options (kanji/kun/on) — what is shown as the answer

self.value_of_test = 1 # Quiz mode with 4 answer choices
self.value_of_test = 0 # standard test
self.current_sheet # the chosen dictionary table
self.current_word = None # the current word as a dict:
Words:
{'index': 514, 'Lesson': 140, 'Num': 567, 'Kanji': '理由）', 'Read': 'りゆう', 'Trans': 'reason', 'Mnem': ''}
Kanji:
{'index': 1027, 'Lesson': 140, 'Num': 1095, 'Kanji': '求', 'On': 'キュウ、グ', 'Kun': 'もとめる', 'Trans': 'demand', 'Sush': 'Noun', 'Mnem': ''}
Kana:
{'index': 1027, 'Lesson': 140, 'Num': 1095, 'Kun': 'もとめる', 'Trans': 'demand', 'Sush': 'Noun', 'Mnem': ''}
self.len_of_count_for_proc = 0 # number of words in the test, used to compute the correct-answer percentage
self.current_word_test = None # the current word as a string
self.current_table_rows = []  # table rows for stats (multiple-answers mode)
self.clicked_columns_for_current = set()  # which columns (On/Kun/Trans) are marked for the current word
self.all_variations = {} # list of all word variants for the test; filters by kanji (exact purpose unclear)
self.all_answers_variant = False  # "all answers" test variant (group by kanji/kun/on)
self.answered_right_nums = set()  # Num of rows whose answer button was pressed (right)
self.answered_right_pairs = set()  # (Num, col) — which (row, column) were pressed (for per-element buttons)
self.property_choose # list of chosen test properties (part of speech)
self.past_word # the previous word as a dict

self.unknown_words = [] # list of unknown words for a repeat test
self.shet_know = 0 # counter of known/unknown words
self.known_clicked = False # flag that the "Know" button was pressed
self.per_element_clicked = False  # a per-option button was pressed (table)
'''
