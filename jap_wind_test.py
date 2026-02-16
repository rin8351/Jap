from copy import deepcopy
import json
from pandas import ExcelFile
import pygame
from random import sample,shuffle

from PyQt5.QtWidgets import QMainWindow, QFrame, QTableWidgetItem,QTableWidget, QScrollArea, QLabel, QComboBox, QLineEdit,QCheckBox, QRadioButton, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,QMenu,QAction,QApplication,QMessageBox,QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QFont

from others_scripts import resource_path, BackgroundScrollArea, cell_has_value
import styles as st
import stats_script as stat



class Rand_window(QMainWindow):
    def __init__(self):
        super().__init__()
        japanese_logo_path = resource_path('japanese_logo.png')
        self.setWindowIcon(QIcon(japanese_logo_path)) # иконка окна
        self.setWindowTitle('Testing')
        QApplication.setFont(QFont("Roboto  ", 10))
        self.data_from_xls()
        pygame.mixer.init()
        # Уроки и счётчик задаются после выбора листа и нажатия "Далее"
        self.all_of_lessons = ['Выбрать один урок']
        self.len_of_words = 0
        self.current_sheet = None  # выбранный лист до нажатия "Далее"
        self.options_for_zero()
        self.main()

    def data_from_xls(self):
        self.xl = ExcelFile('Jp.xlsx')
        self.sheet_names = self.xl.sheet_names
        self.df_w = self.xl.parse('Words')
        # Очистка self.df_w от элементов, у которых 'Lesson' == nan
        if 'Lesson' in self.df_w.columns:
            self.df_w = self.df_w[self.df_w['Lesson'].notna()]
        self.alls_words = self.df_w.reset_index().to_dict('records')


    def options_for_zero(self):
        self.shet_know = 0 # счетчик знаю или не знаю слово
        self.known_clicked = False
        self.per_element_clicked = False  # нажата кнопка по одному варианту (таблица)
        self.unknown_words = []
        self.current_word = None # текущее слово
        self.showing_translation = True 
        self.mnemonic_text=''
        self.count_for_proc = []
        self.len_of_count_for_proc = 0
        self.current_word_test = None
        self.past_word = ''
        self.current_table_rows = []  # строки таблицы для статистики (режим с несколькими ответами)
        self.clicked_columns_for_current = set()  # какие колонки (On/Kun/Trans) отмечены для текущего слова
        self.all_variations = {}
        self.all_answers_variant = False  # вариант теста «со всеми ответами» (группа по кандзи/куну/ону)
        self.answered_right_nums = set()  # Num строк, по которым нажали кнопку ответа (right)
        self.answered_right_pairs = set()  # (Num, col) — по каким (строка, колонка) нажали (для кнопок по элементам)

    def load_sheet_data(self, sheet_name):
        """Загружает данные выбранного листа и обновляет поля уроков."""
        self.df = self.xl.parse(sheet_name)
        self.alls_dict = self.df.reset_index().to_dict('records')
        # Только числовые уроки, без nan; отображаем как целые (40, не 40.0)
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
        self.all_of_lessons = ['Выбрать один урок'] + [str(x) for x in lessons]
        if sheet_name == 'Dictio':
            self.chast_rechi = self.df['Sush'].unique().tolist()
        # Обновляем виджеты уроков под реальное количество уроков листа
        self.ent_less.setText('1')
        self.ent_less_end.setText(str(self.len_of_words))
        self.lb_max_ur.setText(f'Всего уроков = {self.len_of_words}')
        self.choose_one_lesson.clear()
        self.choose_one_lesson.addItems(self.all_of_lessons)

    def main(self):
        self.setGeometry(300, 300, 480, 560)

        self.frame_main = QFrame()
        self.frame_main.setStyleSheet("background-color: transparent;")

        # Шаг 1: только выбор листа и кнопка "Далее"
        self.frame_initial = QFrame()
        self.frame_initial.setStyleSheet("background-color: transparent;")
        self.context_menu = QMenu(self)
        self.sheets_dict = {}
        self.menu_button = QPushButton("Выберите лист", self)
        self.menu_button.setStyleSheet(st.btn_test)
        self.menu_button.setFixedSize(400, 40)
        self.menu_button.setMenu(self.context_menu)
        for sheet_name in self.sheet_names:
            df = self.xl.parse(sheet_name)
            columns = [col for col in df.columns if col not in ['Lesson', 'Num','Sush']]
            self.sheets_dict[sheet_name] = columns
            action = QAction(sheet_name, self)
            action.triggered.connect(lambda checked, sheet_name=sheet_name: self.on_sheet_selected(sheet_name))
            self.context_menu.addAction(action)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda pos: self.context_menu.exec_(self.mapToGlobal(pos)))
        self.btn_dalee = QPushButton("Далее")
        self.btn_dalee.setStyleSheet(st.btn_test)
        self.btn_dalee.setFixedSize(400, 40)
        self.btn_dalee.setVisible(False)
        self.btn_dalee.clicked.connect(self.on_dalee_clicked)
        layout_initial = QVBoxLayout()
        layout_initial.addWidget(self.menu_button)
        layout_initial.addWidget(self.btn_dalee)
        self.frame_initial.setLayout(layout_initial)

        # Остальной интерфейс (появляется после нажатия "Далее")
        self.frame_rest = QFrame()
        self.frame_rest.setStyleSheet("background-color: transparent;")
        self.frame_rest.setVisible(False)

        self.frame_up = QFrame()
        nbur = self.len_of_words
        self.label_type_of_test = QLabel('Выберите тип теста')
        self.chec_type_of_test = QCheckBox ('Тестовый режим с 4-мя вар. ответов,\n без статистики')
        self.chec_all_answers = QCheckBox('Вариант со всеми ответами')
        self.chec_all_answers.setStyleSheet(st.checkbox)
        self.chec_type_of_test.stateChanged.connect(self._on_type_of_test_changed)
        self.lb_start = QLabel('Первый урок')
        self.ent_less = QLineEdit(text='1')
        self.ent_less.setStyleSheet(st.but_line_check)
        self.lb_end = QLabel('Последний урок')
        self.ent_less_end = QLineEdit(text=str(nbur))
        self.all_test_without_filter = QCheckBox('Все слова без фильтрации')
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
        self.label = QLabel('Выберите что тестировать')
        self.label.setVisible(False)
        self.frame_center2=QFrame()
        self.frame_for_options1 = QFrame()
        self.frame_for_options2 = QFrame()
        self.frame_down = QFrame()
        self.lb_max_ur = QLabel(f'Всего уроков = {self.len_of_words}')
        self.btn3 = QPushButton("Включить тест")
        self.btn3.setVisible(False)
        self.btn3.setStyleSheet(st.btn_test)
        self.btn3.setFixedSize(400, 50)
        self.choose_lang = QLabel('Выберите предмет теста')
        self.choose_lang.setVisible(False)
        layout_frame_up = QVBoxLayout()
        layout_frame_up.addWidget(self.label_type_of_test)
        layout_frame_up.addWidget(self.chec_type_of_test)
        layout_frame_up.addWidget(self.chec_all_answers)
        layout_frame_up.addWidget(self.lb_start)
        if self.current_sheet == 'Dictio':
            self.chec_all_answers.setVisible(True)
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
        self.layout_options2 = QVBoxLayout()
        self.frame_for_options1.setLayout(self.layout_options1)
        self.frame_for_options2.setLayout(self.layout_options2)

        layout_frame_down = QVBoxLayout()
        layout_frame_down.addWidget(self.lb_err)
        layout_frame_down.addWidget(self.btn3)
        self.frame_down.setLayout(layout_frame_down)

        layout_frame_rest = QVBoxLayout()
        layout_frame_rest.addWidget(self.frame_up)
        layout_frame_rest.addWidget(self.frame_center)
        layout_frame_rest.addWidget(self.label)
        layout_frame_rest.addWidget(self.frame_center2)
        layout_frame_rest.addWidget(self.frame_for_options1)
        layout_frame_rest.addWidget(self.frame_for_options2)
        layout_frame_rest.addWidget(self.frame_down)
        self.frame_rest.setLayout(layout_frame_rest)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.frame_initial)
        main_layout.addWidget(self.frame_rest)
        self.frame_main.setLayout(main_layout)
        self.scroll_with_backgr()
        self.btn3.clicked.connect(self.checks)

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
        """Выбор листа: показываем кнопку «Далее» или обновляем форму, если уже открыта."""
        self.menu_button.setText(sheet_name)
        self.current_sheet = sheet_name
        if self.frame_rest.isVisible():
            # Пользователь сменил лист после нажатия «Далее» — обновляем уроки и опции
            self.load_sheet_data(sheet_name)
            self.build_sheet_options()
        else:
            self.btn_dalee.setVisible(True)

    def on_dalee_clicked(self):
        """После нажатия «Далее» загружаем данные листа, обновляем уроки и показываем остальной интерфейс."""
        self.load_sheet_data(self.current_sheet)
        self.build_sheet_options()
        self.frame_rest.setVisible(True)
        self.btn_dalee.setVisible(False)

    def build_sheet_options(self):
        """Строит радиокнопки столбцов и (для Dictio) чекбоксы частей речи."""
        self.clear_layout(self.layout_frame_centr1)
        self.clear_layout(self.layout_frame_centr2)
        self.choose_lang.setVisible(True)
        self.label.setVisible(False)
        self.btn3.setVisible(False)
        # «Вариант со всеми ответами» только для вкладки Dictio
        self.chec_all_answers.setVisible(self.current_sheet == 'Dictio')
        columns = self.get_filtered_columns(self.xl, self.current_sheet)
        for column in columns:
            radio_button = QRadioButton(column, self)
            radio_button.setStyleSheet(st.radios)
            radio_button.clicked.connect(lambda checked, column=column: self.on_column_selected(column))
            self.layout_frame_centr1.addWidget(radio_button)
        if self.current_sheet == 'Dictio':
            self.checkboxes = []
            for i in range(len(self.chast_rechi)):
                self.checkboxes.append(QCheckBox(self.chast_rechi[i]))
                self.checkboxes[i].setChecked(True)
                self.checkboxes[i].setStyleSheet(st.checkbox)
                self.layout_options1.addWidget(self.checkboxes[i])
        else:
            self.clear_layout(self.layout_options1)

    def get_filtered_columns(self,xl, sheet_name):
        sheet = xl.parse(sheet_name)
        columns = list(sheet.columns)
        excluded_columns = ['Lesson', 'Num','Sush', 'Mnem']
        return [col for col in columns if col not in excluded_columns]

    def on_column_selected(self, column):
        # Очищаем текущий слой с галочками
        self.clear_layout(self.layout_frame_centr2)
        self.label.setVisible(True)
        self.btn3.setVisible(True)
        self.current_column = column
        # Получаем список всех уникальных значений в выбранном столбце
        values = self.get_unique_values(self.current_sheet, column)
        if 'Mnem' in values:
            values.remove('Mnem')
        # Добавляем галочки для каждого уникального значения
        self.checkbox_for_test = []
        for value in values:
            if value == '':
                # Пропускаем пустые значения
                continue
            checkbox = QCheckBox(str(value), self)
            checkbox.setStyleSheet(st.checkbox)
            self.checkbox_for_test.append(checkbox)
            self.layout_frame_centr2.addWidget(checkbox)
            # положить все знаечния в список
        if (column == 'Trans' or column == 'Kun' or column == 'Kanji') and self.current_sheet == 'Dictio':
            self.clear_layout(self.layout_options2) 
            self.label_all_with_kanji = QLabel('Слова с кандзи или без?')
            self.layout_options2.addWidget(self.label_all_with_kanji) 
            menu_op = 'Все слова', 'Только слова с кандзи', 'Слова без кандзи'
            self.menu_button2 = QComboBox()
            for i in menu_op:
                self.menu_button2.addItem(i)
            self.menu_button2.setCurrentText(menu_op[0])
            self.menu_button2.setStyleSheet(st.combobox)
            self.layout_options2.addWidget(self.menu_button2)   
            self.label_all_with_mnemonics = QLabel('Слова с мнемоникой или без?')
            self.layout_options2.addWidget(self.label_all_with_mnemonics)
            menu_op2 = 'Все слова', 'Только слова с мнемоникой', 'Слова без мнемоники'
            self.menu_button3 = QComboBox()
            for i in menu_op2:
                self.menu_button3.addItem(i)
            self.menu_button3.setCurrentText(menu_op2[0])
            self.menu_button3.setStyleSheet(st.combobox)
            self.layout_options2.addWidget(self.menu_button3)
        else:
            self.clear_layout(self.layout_options2)   

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
        """Колонки ответов, по которым ведём статистику (включая On)."""
        return list(self.test_for_answer) if self.test_for_answer else []

    def _columns_with_value(self, row):
        """Колонки из test_for_answer, у которых в строке не пусто и не '0' (не записываем в статистику нули)."""
        return [c for c in self.test_for_answer if str(row.get(c, '')).strip() and str(row.get(c, '')) != '0']

    def _on_type_of_test_changed(self):
        """При включении теста с 4 вариантами отключаем «Вариант со всеми ответами»."""
        if self.chec_type_of_test.isChecked():
            self.chec_all_answers.setChecked(False)
            self.chec_all_answers.setEnabled(False)
        else:
            self.chec_all_answers.setEnabled(True)

    def checks(self):
        if self.chec_type_of_test.isChecked():
            self.value_of_test = 1 # Тестовый режим с 4-мя вариантами ответов
        else:
            self.value_of_test = 0 # стандартный тест
        self.all_answers_variant = self.chec_all_answers.isChecked() if hasattr(self, 'chec_all_answers') else False
        self.test_for_answer=[]
        self.property_choose = []
        for rb in self.checkbox_for_test:
            if rb.isChecked():
                self.test_for_answer.append(rb.text())
        if self.current_sheet == 'Dictio':
            for rb in self.checkboxes:
                if rb.isChecked():
                    self.property_choose.append(rb.text())
        if self.test_for_answer == []:
            self.lb_err.setText('Выберите хотя бы один\n вариант для теста')
        elif self.property_choose ==[] and self.current_sheet == 'Dictio':
            self.lb_err.setText('Выберите хотя бы одно\n свойство для теста')
        else:
            if len(self.test_for_answer) >1 and self.value_of_test == 1:
                self.lb_err.setText('Для этого типа теста нужно выбрать\nтолько один вариант что тестировать')
            else:
                self.lb_err.setText('')
                self.df2 = self.xl.parse(self.current_sheet)
                if 'Lesson' in self.df2.columns:
                    self.df2 = self.df2[self.df2['Lesson'].notna()]
                self.alls  = self.df2.reset_index().to_dict('records')
                self.lb_err.setText('')
                if self.choose_one_lesson.currentText() =='Выбрать один урок':
                    if self.ent_less.text() == '' or self.ent_less_end.text() == '':
                        self.lb_err.setText('Введите номер урока')
                    else:
                        self.st = int(self.ent_less.text())
                        self.en = int(self.ent_less_end.text())

                        if self.st == 0 or self.en == 0:
                            self.lb_err.setText('Введите номер урока')
                        elif self.st > self.en:
                            self.lb_err.setText('Начальный урок больше конечного')
                        elif self.en > self.len_of_words:
                            self.lb_err.setText('Конечный урок больше максимального')
                        elif self.st == None or self.en == None:
                            self.lb_err.setText('Введите номер урока')
                        else:
                            self.continue_check()
                else:
                    self.continue_check()

    def continue_check(self):
        self.lb_err.setText('')
        if self.choose_one_lesson.currentText() =='Выбрать один урок':
            self.alls =  [i for i in self.alls if (i['Lesson'] >= self.st and i['Lesson'] <= self.en)]  
        else:
            self.alls =  [i for i in self.alls if i['Lesson'] == int(self.choose_one_lesson.currentText())]
        if self.current_sheet == 'Dictio':
            self.alls =  [i for i in self.alls if i['Sush'] in self.property_choose]
            try:
                if hasattr(self, "menu_button3") and self.menu_button3 is not None:
                    text = self.menu_button3.currentText()
                    if text == 'Только слова с мнемоникой':
                        self.alls = [i for i in self.alls if cell_has_value(i.get('Mnem'))]
                    elif text == 'Слова без мнемоники':
                        self.alls = [i for i in self.alls if not cell_has_value(i.get('Mnem'))]
            except RuntimeError:
                # Виджет был удален, пропускаем проверку
                pass
            if self.current_column == 'Kun' or self.current_column=='Trans':
                try:
                    if hasattr(self, "menu_button2") and self.menu_button2 is not None:
                        text = self.menu_button2.currentText()
                        if text == 'Только слова с кандзи':
                            self.alls = [i for i in self.alls if cell_has_value(i.get('Kanji'))]
                        elif text == 'Слова без кандзи':
                            self.alls = [i for i in self.alls if not cell_has_value(i.get('Kanji'))]
                except RuntimeError:
                    # Виджет был удален, пропускаем проверку
                    pass
        if len(self.test_for_answer) == 1:
            self.alls_for_copy = [i for i in self.alls if str(i[self.test_for_answer[0]]) != '0' and str(i[self.current_column]) != '0']
        else:
            self.alls_for_copy = [i for i in self.alls if str(i[self.current_column]) != '0']
        self.alls = deepcopy(self.alls_for_copy)
        if self.current_sheet == 'Dictio':
            self.name_of_file = "stats.json"
        else:
            self.name_of_file = "stats_words.json"
        self.current_answer_column = self.test_for_answer[0] if self.test_for_answer else None
        try:
            with open(self.name_of_file, 'r', encoding='utf-8') as f:
                self.stats = json.load(f)
        except FileNotFoundError:
            self.stats = {}
            with open(self.name_of_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False)
        if not self.all_test_without_filter.isChecked():
            self.alls = stat.filter_items_for_test(self.alls, self.stats, self.current_column, self.current_answer_column)
        self.alls = stat.sort_items_for_choice_test(self.alls, self.stats, self.current_column, self.current_answer_column)
        if self.value_of_test == 1 and len(self.alls) <=3:
            self.lb_err.setText('Слишком мало слов для теста с 4-мя вариантами ответов')
        else:
            self.count_for_proc_funk()
            if self.value_of_test==1:
                self.all_variations = deepcopy(self.alls)
            self.main2()

    def main2(self):
        self.frame_main.deleteLater()
        self.setGeometry(300, 300, 700, 750)  # Увеличена высота окна для таблицы
        self.frame_main = QFrame()
        self.frame_main.setStyleSheet("background-color: transparent;")

        self.frame_up2 = QFrame()
        self.frame_down2 = QFrame()
        self.frame_know = QFrame()
        self.btn_back = QPushButton("В начальное меню")
        self.btn_back.setStyleSheet(st.but_line_check)

        layout_frame_up2 = QHBoxLayout()
        layout_frame_up2.addWidget(self.btn_back)
        self.frame_up2.setLayout(layout_frame_up2)

        self.btn_continue = QPushButton("Начать тест")
        self.btn_continue.setStyleSheet(st.btn_test) 
        self.btn_continue.setFixedHeight(40)
        self.btn_continue.setFixedWidth(400)
        self.label_total = QLabel("Всего слов")
        self.mnemonic_text = QLabel("")
        self.mnemonic_text.setStyleSheet("color: #8B0000;")
        self.name_of_difficulty = QLabel("")
        self.part_of_speech = QLabel("")
        self.label_question = QTextEdit()  # Слово
        self.label_question.setReadOnly(True)  # Make it read-only.
        self.label_question.setFrameStyle(QFrame.NoFrame)  # No border.
        self.label_question.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No vertical scroll bar.
        self.label_question.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No horizontal scroll bar.
        self.label_answer = QTextEdit("")    # Перевод
        self.label_answer.setReadOnly(True)  # Make it read-only.
        self.label_answer.setFrameStyle(QFrame.NoFrame)  # No border.
        self.label_answer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No vertical scroll bar.
        self.label_answer.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No horizontal scroll bar.
        self.where_in_words_label = QLabel("") #В каких словах в листе Words есть это слово
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
        layout_frame_down2.addWidget(self.btn_continue)
        layout_frame_down2.addWidget(self.label_total)
        layout_frame_down2.addWidget(self.mnemonic_text)
        layout_frame_down2.addWidget(self.name_of_difficulty)
        layout_frame_down2.addWidget(self.part_of_speech)
        layout_frame_down2.addWidget(self.label_question)
        layout_frame_down2.addWidget(self.where_in_words_label)
        self.frame_down2.setLayout(layout_frame_down2)

        layout_frame_know = QVBoxLayout()
        layout_buttons_row = QHBoxLayout()
        self.but_know = QPushButton("Знаю")
        self.but_know.setVisible(False)
        self.but_hard = QPushButton("Сложно")
        self.but_hard.setVisible(False)
        self.but_hard.setStyleSheet(st.btn_test)
        self.but_easy = QPushButton("Легко")
        self.but_easy.setVisible(False)
        self.but_easy.setStyleSheet(st.btn_test)
        layout_buttons_row.addWidget(self.but_know)
        layout_buttons_row.addWidget(self.but_hard)
        layout_buttons_row.addWidget(self.but_easy)
        layout_frame_know.addLayout(layout_buttons_row)
        self.table_widget = QTableWidget(self)
        self.table_widget.setMinimumHeight(300)  # Минимальная высота таблицы
        self.table_widget.setStyleSheet(st.table)
        if len(self.test_for_answer) == 1 and not getattr(self, 'all_answers_variant', False):
            self.table_widget.setVisible(False)
        elif getattr(self, 'all_answers_variant', False):
            # В варианте «со всеми ответами» таблицу показываем только при нескольких колонках ответа
            self.table_widget.setVisible(len(self.test_for_answer) > 1)
        else:
            self.table_widget.setVisible(len(self.test_for_answer) > 1)
        layout_frame_know.addWidget(self.table_widget, 1)  # Stretch factor = 1, таблица займет максимум места
        # Кнопки по вариантам ответа (только при таблице: несколько колонок, без «всех ответов»)
        self.frame_table_buttons = QFrame()
        self.layout_table_buttons = QHBoxLayout()
        self.frame_table_buttons.setLayout(self.layout_table_buttons)
        self.frame_table_buttons.setVisible(len(self.test_for_answer) > 1 and self.value_of_test == 0 and not getattr(self, 'all_answers_variant', False))
        self.table_column_buttons = []
        layout_frame_know.addWidget(self.frame_table_buttons)
        # Блок кнопок «все ответы» (по одной на каждую строку группы) — только для варианта «со всеми ответами»
        self.frame_all_answer_buttons = QFrame()
        self.layout_all_answer_buttons = QGridLayout()
        self.frame_all_answer_buttons.setLayout(self.layout_all_answer_buttons)
        self.frame_all_answer_buttons.setVisible(False)
        self.answer_row_buttons = []  # кнопки ответов по строкам (для all_answers_variant)
        layout_frame_know.addWidget(self.frame_all_answer_buttons)
        if self.value_of_test==0:  # тестовый вариант с 4-мя вариантами ответов
            layout_frame_know.addWidget(self.label_answer)
        else:
            self.checkBoxes_in_test = []
            for _ in range(4):
                checkBox = QCheckBox(self)
                checkBox.stateChanged.connect(self.checkAnswer)
                self.checkBoxes_in_test.append(checkBox)
                layout_frame_know.addWidget(checkBox)
            for checkBox in self.checkBoxes_in_test:
                checkBox.setVisible(False)
        self.frame_know.setLayout(layout_frame_know)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.frame_up2)
        self.main_layout.addWidget(self.frame_down2)
        self.main_layout.addWidget(self.frame_know)
        self.frame_main.setLayout(self.main_layout)
        self.scroll_with_backgr()
        if self.value_of_test==0: # тестовый вариант с 4-мя вариантами ответов
            self.btn_continue.clicked.connect(self.show_next_word)
        else:
            self.btn_continue.clicked.connect(self.show_next_word2)
        self.but_know.clicked.connect(self.know)
        self.but_hard.clicked.connect(self.on_hard_clicked)
        self.but_easy.clicked.connect(self.on_easy_clicked)
        self.btn_back.clicked.connect(self.back)

    def repeat_frame(self):
        self.frame_repeat = QFrame()
        self.layout_frame_repeat = QVBoxLayout()  # Блок для повтора, статистики вернух слов и кнопки "Повторить"
        self.label_end = QLabel("")
        self.label_count_right = QLabel("")
        self.again_but = QPushButton("Повторить")
        self.again_but.setFixedHeight(40)
        self.again_but.setFixedWidth(400)
        self.again_but.setVisible(False)
        self.again_but.setStyleSheet(st.btn_test)
        self.again_unknow = QPushButton("Повторить не узнанные слова")
        self.again_unknow.setVisible(False)
        self.again_unknow.setStyleSheet(st.btn_test)
        self.again_unknow.setFixedHeight(40)
        self.again_unknow.setFixedWidth(400)
        self.again_label = QLabel("")
        if self.value_of_test ==1:
            # убрать все чекбоксы
            for checkBox in self.checkBoxes_in_test:
                checkBox.setVisible(False)
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
        self.count_for_proc_funk()
        self.unknown_words = []
        self.options_for_again()


    def keyPressEvent(self, event):
            if event.key() == Qt.Key_Space:
                self.show_next_word()
            if event.key() == Qt.Key_Return:
                self.know()
    
    def resetCheckBoxes(self):
        for checkBox in self.checkBoxes_in_test:
            checkBox.setStyleSheet("")
            checkBox.setEnabled(True)
            checkBox.setChecked(False)

    def checkAnswer(self, state):
        if state == Qt.Checked:
            for checkBox in self.checkBoxes_in_test:
                checkBox.setEnabled(False)
                if checkBox.isChecked():
                    if checkBox.userData:
                        checkBox.setStyleSheet("QCheckBox { color: green; }")
                        checkBox.setText(checkBox.text() + " - Правильно")
                        self.shet_know += 1
                    else:
                        checkBox.setStyleSheet("QCheckBox { color: red; }")
                        checkBox.setText(checkBox.text() + " - Неправильно")
                        self.unknown_words.append(self.past_word)  
                        # выделить правильный результат зеленым
                        for checkBox in self.checkBoxes_in_test:
                            if checkBox.userData:
                                checkBox.setStyleSheet("QCheckBox { color: green; }")
                                checkBox.setText(checkBox.text() + " - Правильно")
            self.btn_continue.setVisible(True)
            self.btn_continue.setText("Следующее слово")

    def show_next_word(self):
        
        if self.showing_translation:
            self.btn_continue.setText("Показать ответ")
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
            self.but_know.setStyleSheet('QPushButton {background-color: red; color: white;}')
            self._reset_difficulty_buttons_style()
            self.but_hard.setEnabled(False)
            self.but_easy.setEnabled(False)
            self.showing_translation = False
            if self.past_word !='':
                if self.known_clicked == True:
                    self.known_clicked = False
                else:
                    # Не нажали «Знаю» — добавляем в невыученные и пишем wrong по неотмеченным
                    if getattr(self, 'all_answers_variant', False):
                        # Вариант «со всеми ответами»: wrong по неотмеченным (строка, колонка) или по целым строкам
                        if len(self.test_for_answer) > 1:
                            # Кнопки по элементам: wrong только по не нажатым (row, col)
                            for row in getattr(self, 'current_table_rows', []):
                                missed = False
                                for col in self._columns_with_value(row):
                                    if (row.get('Num'), col) not in getattr(self, 'answered_right_pairs', set()):
                                        stat.record_wrong(self.stats, row, self.current_column, self.name_of_file, col)
                                        missed = True
                                if missed:
                                    self.unknown_words.append(row)
                        else:
                            for row in getattr(self, 'current_table_rows', []):
                                if row.get('Num') not in getattr(self, 'answered_right_nums', set()):
                                    self.unknown_words.append(row)
                                    for col in self._columns_with_value(row):
                                        stat.record_wrong(self.stats, row, self.current_column, self.name_of_file, col)
                    else:
                        self.unknown_words.append(self.past_word)
                        if self.current_sheet in ('Dictio', 'Words') and self.current_column in ('Kanji', 'Trans', 'Kun'):
                            if len(self.test_for_answer) > 1:
                                # Для таблицы: wrong только по колонкам, которые не отмечали (Kanji/Kun/Trans)
                                for row in getattr(self, 'current_table_rows', []):
                                    for col in self._columns_with_value(row):
                                        if col not in getattr(self, 'clicked_columns_for_current', set()):
                                            stat.record_wrong(self.stats, row, self.current_column, self.name_of_file, col)
                            else:
                                if self.current_answer_column and self.current_answer_column in self._columns_with_value(self.past_word):
                                    stat.record_wrong(self.stats, self.past_word, self.current_column, self.name_of_file, self.current_answer_column)
                self.per_element_clicked = False
                if getattr(self, 'all_answers_variant', False):
                    self._clear_all_answer_buttons()
                    self.answered_right_nums = set()
                    self.answered_right_pairs = set()
            if not self.alls: #Если все слова закончились
                self.past_word = ''
                self.label_question.setText("Тест завершен.")
                self.name_of_difficulty.setText('')
                self.part_of_speech.setText('')
                self.table_widget.setVisible(False)
                self.label_total.setText('')
                self.label_answer.setText("")
                self.repeat_frame()
                self.again_but.setVisible(True)
                self.btn_continue.setVisible(False)
                self.but_know.setVisible(False)
                if not getattr(self, 'all_answers_variant', False):
                    self.but_hard.setVisible(False)
                    self.but_easy.setVisible(False)
                self.where_in_words_label.setText('')
                if getattr(self, 'all_answers_variant', False):
                    self._clear_all_answer_buttons()
                if len(self.unknown_words) > 0:
                    self.again_unknow.setVisible(True)
                if self.len_of_count_for_proc==0:
                    self.label_count_right.setText('Нет слов для теста')
                else:
                    prots = int(round((100 / self.len_of_count_for_proc * self.shet_know), 2))
                    self.label_count_right.setText(f'Общее число={self.len_of_count_for_proc}, Верно={self.shet_know}, процент верных = {prots}.')
                return

            if getattr(self, 'all_answers_variant', False):
                # Группа по совпадению кандзи/куна/она: все строки с тем же значением current_column
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
            self.name_of_difficulty.setText(f'Сложность: {difficulty}')
            if len(self.property_choose) > 1 and not getattr(self, 'all_answers_variant', False):
                self.part_of_speech.setText(f'Часть речи: {self.current_word.get("Sush", "")}')
            if self.current_sheet=='Dictio' and self.current_column=='Trans':
                for i in self.alls:
                    if cell_has_value(i.get('Mnem')):
                        if i.get('Trans') == self.current_word['Trans']:
                            self.mnemonic_text.setText('есть мнемоника')
                            self.mnemonic_text.setToolTip(str(i['Mnem']))
                            break
                    else:
                        self.mnemonic_text.setText('нет мнемоники')
                        self.mnemonic_text.setToolTip('')
            self.past_word = self.current_word
            t = f'Количество слов= {len(self.alls)}'
            self.label_total.setText(t)
            if self.current_sheet == 'Dictio' and self.current_column == 'Kanji': # тип теста, где сначала показывается кандзи, а потом перевод
                lines = []
                text=''
                for i in self.alls_words:
                    if self.current_word_test in i['Kanji'] and len(lines)<=5:
                        lines.append(i['Trans'])
                    if len(lines)>=1:
                        text = "Встречаются в словах:\n"+"\n".join(lines)
                        self.label_question.setToolTip(text)
                        self.label_question.setStyleSheet('QTextEdit {color: #8B0000;}')
            elif self.current_sheet == 'Dictio' and self.current_column =='Trans':  # тип теста, где сначала показывается перевод, а потом кандзи
                lines = [] # список слов в которых встречается кандзи
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
                    text = "Встречаются в словах:\n"+"\n".join(lines)
                    self.label_question.setToolTip(text)
                    self.label_question.setStyleSheet('QTextEdit {color: #8B0000;}')
            self.label_question.setText(self.current_word_test)
            self.label_answer.setText("")
            if self.current_word_test in self.count_for_proc:
                self.count_for_proc.remove(self.current_word_test)
        else:
            self.btn_continue.setText("Следующее слово")
            self.but_know.setDisabled(False)
            self._reset_difficulty_buttons_style()
            self.but_hard.setEnabled(True)
            self.but_easy.setEnabled(False)  # "Легко" доступна только после нажатия "Знаю"
            self.showing_translation = True
            if self.current_sheet == 'Dictio' and self.current_column == 'Kanji':
                lines = []
                text=''
                for i in self.alls_words:
                    if self.current_word_test in i['Kanji'] and len(lines)<=5:
                        strings = str(i['Kanji'])+', '+i['Trans']
                        lines.append(strings)
                    if len(lines)>=1:
                        text = "Встречаются в словах:\n"+"\n".join(lines)
                        self.label_question.setToolTip(text)
                        self.label_question.setStyleSheet('QTextEdit {color: #8B0000;}')
            elif self.current_sheet == 'Dictio' and self.current_column =='Trans':
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
                    text = "Встречаются в словах:\n"+"\n".join(lines)
                    self.label_question.setToolTip(text)
                    self.label_question.setStyleSheet('QTextEdit {color: #8B0000;}')
            if getattr(self, 'all_answers_variant', False):
                self._clear_all_answer_buttons()
                if len(self.current_table_rows) == 1:
                    # Один ответ — показываем текстом, как в обычном режиме
                    row = self.current_table_rows[0]
                    if len(self.test_for_answer) == 1:
                        self.label_answer.setText(str(row.get(self.test_for_answer[0], '')))
                    else:
                        parts = [str(row.get(p, '')) for p in self.test_for_answer]
                        self.label_answer.setText(" | ".join(parts))
                    self.frame_all_answer_buttons.setVisible(False)
                elif len(self.test_for_answer) > 1:
                    # Несколько колонок ответа: таблица + кнопка на каждый элемент (учёба, まなぶ, ガク, ...)
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
                    # Несколько строк, одна колонка — кнопки по одному на каждую строку группы
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
                # Только один элемент — ответ текущей строки, не все с тем же кандзи
                self.translations = str(self.current_word.get(self.test_for_answer[0], ''))
                self.label_answer.setText(self.translations)
                if self.current_word in self.alls:
                    self.alls.remove(self.current_word) 
            else:
                self.translations = [self.current_word[prop] for prop in self.test_for_answer]
                self.update_table(self.translations, self.current_word_test, single_word=self.current_word)

    def show_next_word2(self):
        self.resetCheckBoxes()
        for checkBox in self.checkBoxes_in_test:
                checkBox.setVisible(True)
        self.btn_continue.setVisible(False)   
        if not self.alls: #Если все слова закончились
            self.past_word = ''
            self.label_question.setText("Тест завершен.")
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
                self.label_count_right.setText('Нет слов для теста')
            else:
                prots = int(round((100 / self.len_of_count_for_proc * self.shet_know), 2))
                self.label_count_right.setText(f'Общее число={self.len_of_count_for_proc}, Верно={self.shet_know}, процент верных = {prots}.')
            return

        self.current_word = self.alls[0]
        self.current_word_test = self.current_word[self.current_column]
        num_key, item_key = stat.get_item_key(self.current_word, self.current_column, self.current_answer_column)
        difficulty = self.stats.get(num_key, {}).get(item_key, {}).get('difficulty', 'normal')
        self.name_of_difficulty.setText(f'Сложность: {difficulty}')
        self.past_word = self.current_word

        t = f'Количество слов= {len(self.alls)}'
        self.label_total.setText(t)

        self.label_question.setText(self.current_word_test)

        if self.current_word_test in self.count_for_proc:
            self.count_for_proc.remove(self.current_word_test)

        correct_answer = self.current_word[self.test_for_answer[0]]
        correct_kanji = self.current_word['Kanji']

        # Исключаем слова с тем же кандзи
        if not cell_has_value(correct_kanji):
            filtered_words = [word for word in self.all_variations]
        else:
            filtered_words = [word for word in self.all_variations if word['Kanji'] != correct_kanji]

        # Выбираем три неправильных ответа
        wrong_answers = sample([word[self.test_for_answer[0]] for word in filtered_words], 3)

        # Смешиваем правильный ответ с неправильными
        all_answers = wrong_answers + [correct_answer]
        shuffle(all_answers)

        # Устанавливаем текст для чекбоксов
        for i, checkBox in enumerate(self.checkBoxes_in_test):
            checkBox.setText(all_answers[i])
            checkBox.setEnabled(True)
            checkBox.setChecked(False)
            checkBox.userData = (all_answers[i] == correct_answer)
            # увеличить шрифт
            checkBox.setFont(QFont('Arial', 16))

        # Удаляем только текущее слово, а не все с тем же кандзи/переводом
        if self.current_word in self.alls:
            self.alls.remove(self.current_word)

    def reset_test(self):
        self.shet_know = 0
        self.alls = deepcopy(self.alls_for_copy)
        self.alls = stat.sort_items_for_choice_test(self.alls, self.stats, self.current_column, self.current_answer_column)
        self.count_for_proc_funk()
        self.options_for_again()

    def count_for_proc_funk(self):
        for i in self.alls:
            if i[self.current_column] not in self.count_for_proc:
                self.count_for_proc.append(i[self.current_column])
        self.len_of_count_for_proc = len(self.count_for_proc)

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
        self.label_count_right.setText('')
        self.again_but.setVisible(False)
        self.btn_continue.setVisible(True)
        self.frame_repeat.deleteLater()
        self.known_clicked = False
        if self.value_of_test ==0:
            self.show_next_word()
        else:
            self.show_next_word2()

    def _reset_difficulty_buttons_style(self):
        """Сброс стиля кнопок Сложно/Легко к обычному."""
        self.but_hard.setStyleSheet(st.btn_test)
        self.but_easy.setStyleSheet(st.btn_test)

    def on_hard_clicked(self):
        if not self.but_hard.isEnabled():
            return
        self.but_hard.setStyleSheet('QPushButton {background-color: lime; color: white;}')
        self.but_hard.setEnabled(False)
        self.but_easy.setEnabled(False)
        if self.current_sheet in ('Dictio', 'Words') and self.current_column in ('Kanji', 'Trans', 'Kun'):
            if self.current_answer_column and self.current_answer_column in self._columns_with_value(self.current_word):
                stat.set_difficulty_only(self.stats, self.current_word, "hard", self.current_column, self.name_of_file, self.current_answer_column)

    def on_easy_clicked(self):
        if not self.but_easy.isEnabled():
            return
        self.but_easy.setStyleSheet('QPushButton {background-color: lime; color: white;}')
        self.but_easy.setEnabled(False)
        self.but_hard.setEnabled(False)
        if self.current_sheet in ('Dictio', 'Words') and self.current_column in ('Kanji', 'Trans', 'Kun'):
            if self.current_answer_column and self.current_answer_column in self._columns_with_value(self.current_word):
                stat.set_difficulty_only(self.stats, self.current_word, "easy", self.current_column, self.name_of_file, self.current_answer_column)

    def on_table_column_clicked(self, col):
        """Нажатие на кнопку On/Kun/Trans: right только этой колонке для текущей строки."""
        if self.current_sheet not in ('Dictio', 'Words') or self.current_column not in ('Kanji', 'Trans', 'Kun'):
            return
        rows = getattr(self, 'current_table_rows', [])
        if not rows or col not in self._columns_with_value(rows[0]):
            return
        self.clicked_columns_for_current.add(col)
        stat.record_correct(self.stats, rows[0], None, self.current_column, self.name_of_file, col)
        self.per_element_clicked = True
        self.but_know.setEnabled(False)
        self.but_know.setStyleSheet('QPushButton {background-color: gray; color: white;}')
        for btn in getattr(self, 'table_column_buttons', []):
            if btn.text() == col:
                btn.setEnabled(False)
                break

    def know(self):
        if self.showing_translation:  # Обновляем статистику только если показано слово, а не перевод
            if self.known_clicked == False:
                self.but_know.setStyleSheet('QPushButton {background-color: lime; color: white;}')
                if self.current_sheet in ('Dictio', 'Words') and self.current_column in ('Kanji', 'Trans', 'Kun'):
                    if getattr(self, 'all_answers_variant', False):
                        # Вариант «со всеми ответами»: right всем строкам группы
                        for row in getattr(self, 'current_table_rows', []):
                            for col in self._columns_with_value(row):
                                stat.record_correct(self.stats, row, None, self.current_column, self.name_of_file, col)
                    elif len(self.test_for_answer) > 1:
                        for row in getattr(self, 'current_table_rows', []):
                            for col in self._columns_with_value(row):
                                stat.record_correct(self.stats, row, None, self.current_column, self.name_of_file, col)
                    else:
                        if self.current_answer_column and self.current_answer_column in self._columns_with_value(self.current_word):
                            stat.record_correct(self.stats, self.current_word, None, self.current_column, self.name_of_file, self.current_answer_column)
                self.shet_know += 1
                self.known_clicked = True
                if not getattr(self, 'all_answers_variant', False):
                    self.but_easy.setEnabled(True)  # "Легко" доступна только после "Знаю"

    def back(self):
        self.data_from_xls()
        self.options_for_zero()
        self.frame_main.deleteLater()
        self.main()       

    def _clear_all_answer_buttons(self):
        """Удаляет кнопки ответов в варианте «со всеми ответами»."""
        self.answer_row_buttons.clear()
        while self.layout_all_answer_buttons.count():
            child = self.layout_all_answer_buttons.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.frame_all_answer_buttons.setVisible(False)

    def _on_answer_row_clicked(self, row):
        """Нажатие на кнопку одного из ответов: right для этой строки, «Знаю» отключается."""
        if self.current_sheet not in ('Dictio', 'Words') or self.current_column not in ('Kanji', 'Trans', 'Kun'):
            return
        self.answered_right_nums.add(row.get('Num'))
        for col in self._columns_with_value(row):
            stat.record_correct(self.stats, row, None, self.current_column, self.name_of_file, col)
        self.per_element_clicked = True
        self.but_know.setEnabled(False)
        self.but_know.setStyleSheet('QPushButton {background-color: gray; color: white;}')
        # Найти кнопку для этой row и сделать зелёной, неактивной
        for btn in self.answer_row_buttons:
            if getattr(btn, '_row_data', None) and btn._row_data.get('Num') == row.get('Num'):
                btn.setEnabled(False)
                btn.setStyleSheet('QPushButton {background-color: lime; color: white;}')
                break

    def _on_answer_element_clicked(self, row, col):
        """Нажатие на кнопку одного элемента (ячейки): right для этой (строка, колонка), «Знаю» отключается."""
        if self.current_sheet not in ('Dictio', 'Words') or self.current_column not in ('Kanji', 'Trans', 'Kun'):
            return
        self.answered_right_pairs.add((row.get('Num'), col))
        stat.record_correct(self.stats, row, None, self.current_column, self.name_of_file, col)
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
        # single_word / multiple_words — явный список строк; иначе берём из self.alls по current_word
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

        # Кнопки по названиям колонок (On, Kun, Trans) — только если не режим «по элементам»
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
        header.setStretchLastSection(True)
                
'''
self.value_of_test = 1 # Тестовый режим с 4-мя вариантами ответов
self.value_of_test = 0 # стандартный тест
self.current_sheet # выбранный лист до нажатия "Далее"
self.shet_know = 0 # счетчик знаю или не знаю слово
self.known_clicked = False
self.per_element_clicked = False  # нажата кнопка по одному варианту (таблица)
self.unknown_words = []
self.current_word = None # текущее слово в виде словаря
self.showing_translation = True 
self.mnemonic_text=''
self.count_for_proc = []
self.len_of_count_for_proc = 0
self.current_word_test = None # текущее слово в виде строки
self.past_word = ''
self.current_table_rows = []  # строки таблицы для статистики (режим с несколькими ответами)
self.clicked_columns_for_current = set()  # какие колонки (On/Kun/Trans) отмечены для текущего слова
self.all_variations = {}
self.all_answers_variant = False  # вариант теста «со всеми ответами» (группа по кандзи/куну/ону)
self.answered_right_nums = set()  # Num строк, по которым нажали кнопку ответа (right)
self.answered_right_pairs = set()  # (Num, col) — по каким (строка, колонка) нажали (для кнопок по элементам)

self.property_choose # список выбранных свойств для теста (часть речи)
self.test_for_answer # список выбранных вариантов для теста (кандзи/кун/он)
self.current_column # выбранный столбец до нажатия "Далее"
self.past_word # предыдущее слово в виде словаря

'''
