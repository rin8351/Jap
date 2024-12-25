from copy import deepcopy
from PyQt5.QtWidgets import QMainWindow, QFrame, QTableWidgetItem,QTextEdit,QTableWidget, QScrollArea, QLabel, QComboBox, QLineEdit,QCheckBox, QRadioButton, QVBoxLayout, QHBoxLayout, QPushButton,QMenu,QAction,QApplication,QMessageBox
from PyQt5.QtCore import Qt,QRect
from PyQt5.QtGui import QPixmap,QIcon,QFont,QPainter
from pandas import ExcelFile, read_excel
import styles as st
from json import dump, load
from ast import literal_eval
from random import choice
import os
from path_for_files import resource_path

class Rand_window(QMainWindow):
    def __init__(self):
        super().__init__()
        japanese_logo_path = resource_path('japanese_logo.png')
        self.setWindowIcon(QIcon(japanese_logo_path)) # иконка окна
        self.setWindowTitle('Japannese test')
        QApplication.setFont(QFont("Roboto  ", 10))
        self.data_from_xls()
        self.check_new_words_for_stat()
        self.all_of_lessons=[]
        for x in self.alls_dict:
            if x['Lesson'] not in self.all_of_lessons:
                self.all_of_lessons.append(x['Lesson'])
        self.all_of_lessons.sort()
        self.len_of_words = max(self.all_of_lessons)
        self.all_of_lessons.insert(0,'Выбрать один урок')
        self.options_for_zero()
        self.main()

    def data_from_xls(self):
        self.xl = ExcelFile('J_e_all_my.xlsx')
        self.df = self.xl.parse('Dictio')
        self.alls_dict  = self.df.reset_index().to_dict('records')
        self.sheet_names = self.xl.sheet_names # self.sp_vib in other file
        self.chast_rechi = self.df['Sush'].unique().tolist()
        self.df_w = self.xl.parse('Words')
        self.alls_words  = self.df_w.reset_index().to_dict('records')

    def options_for_zero(self):
        self.shet_know = 0 # счетчик знаю или не знаю слово
        self.unknown_words = []
        self.known_clicked = False
        self.current_word = None
        self.showing_translation = True
        self.mnemonic_text=''
        self.count_for_proc = []
        self.len_of_count_for_proc = 0
        self.current_word_test = None
        self.past_word = ''

    def main(self):
        self.setGeometry(300, 300, 480, 560)

        self.frame_main = QFrame()
        self.frame_main.setStyleSheet("background-color: transparent;")
        self.frame_up = QFrame()
        nbur = self.len_of_words
        self.lb_start = QLabel('Первый урок')
        self.ent_less = QLineEdit(text='1')
        self.ent_less.setStyleSheet(st.but_line_check)
        self.lb_end = QLabel('Последний урок')
        self.ent_less_end = QLineEdit(text=str(nbur))

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
        self.check_r_or_st = QCheckBox('Показывать слова рандомно')

        self.context_menu = QMenu(self)
        self.sheets_dict = {}

        self.menu_button = QPushButton("Выберите лист", self)
        self.menu_button.setStyleSheet(st.btn_test)
        self.menu_button.setFixedSize(400, 40)  # изменить ширину на 400
        self.menu_button.setMenu(self.context_menu)

        for sheet_name in self.sheet_names:
            df = self.xl.parse(sheet_name)
            columns = [col for col in df.columns if col not in ['Lesson', 'Num','Sush']]
            self.sheets_dict[sheet_name] = columns
            action = QAction(sheet_name, self)
            # Связываем обработчик нажатия на действие
            action.triggered.connect(lambda checked, sheet_name=sheet_name: self.on_sheet_selected(sheet_name))
            self.context_menu.addAction(action)
        # Устанавливаем контекстное меню для главного окна
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda pos: self.context_menu.exec_(self.mapToGlobal(pos)))

        self.btn3 = QPushButton("Включить тест")
        self.btn3.setVisible(False)
        self.btn3.setStyleSheet(st.btn_test)
        self.btn3.setFixedSize(400, 50)  # изменить ширину на 150, высоту на 50
        self.btn_witn_zero = QPushButton("Пройти тест с нуля")
        self.but_contin = QPushButton("Продолжить\n сохраненный тест")
        self.but_contin.setStyleSheet(st.but_line_check)
        self.clear_save = QPushButton("Очистить\n сохраненный тест")
        self.clear_save.setStyleSheet(st.but_line_check)
        self.btn_witn_zero.setStyleSheet(st.but_line_check)
        self.clear_save.setVisible(False)
        self.but_contin.setVisible(False)
        self.btn_witn_zero.setVisible(False)
        if not self.is_file_empty('test_progress.json'):
            self.but_contin.setVisible(True)
            self.clear_save.setVisible(True)
        self.choose_lang = QLabel('Выберите предмет теста')
        self.choose_lang.setVisible(False)
        layout_frame_up = QVBoxLayout()
        layout_frame_up.addWidget(self.lb_start)
        layout_frame_up.addWidget(self.ent_less)
        layout_frame_up.addWidget(self.lb_end)
        layout_frame_up.addWidget(self.ent_less_end)
        layout_frame_up.addWidget(self.choose_one_lesson)
        layout_frame_up.addWidget(self.lb_max_ur)
        layout_frame_up.addWidget(self.check_r_or_st)
        layout_frame_up.addWidget(self.menu_button)
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
        layout_frame_down.addWidget(self.btn_witn_zero)
        layout_frame_down.addWidget(self.but_contin)
        layout_frame_down.addWidget(self.clear_save)
        self.frame_down.setLayout(layout_frame_down)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.frame_up)
        main_layout.addWidget(self.frame_center)
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.frame_center2)
        main_layout.addWidget(self.frame_for_options1)
        main_layout.addWidget(self.frame_for_options2)
        main_layout.addWidget(self.frame_down)
        self.frame_main.setLayout(main_layout)
        self.scroll_with_backgr()
        self.btn3.clicked.connect(self.checks)
        self.but_contin.clicked.connect(self.load_progress)
        self.clear_save.clicked.connect(self.clear_progress)

    def scroll_with_backgr(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        background_image_path2 = resource_path('japanese_background2.png')
        self.scroll_area = BackgroundScrollArea(background_image_path2)
        self.scroll_area.setWidget(self.frame_main)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(st.scroll)
        self.setCentralWidget(self.scroll_area)

    def on_sheet_selected(self,sheet_name):
        # Получаем столбцы для выбранного листа
        self.menu_button.setText(sheet_name)
        self.current_sheet = sheet_name
        columns = self.get_filtered_columns(self.xl, sheet_name)
        # Очищаем текущий слой с радиокнопками и галочками
        self.clear_layout(self.layout_frame_centr1)
        self.clear_layout(self.layout_frame_centr2)
        self.choose_lang.setVisible(True)
        self.label.setVisible(False)
        self.btn3.setVisible(False)
        # Добавляем радиокнопки для каждого столбца
        for column in columns:
            radio_button = QRadioButton(column, self)
            radio_button.setStyleSheet(st.radios)
            radio_button.clicked.connect(lambda checked, column=column: self.on_column_selected(column))
            self.layout_frame_centr1.addWidget(radio_button)
        if sheet_name == 'Dictio':
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
        excluded_columns = ['Lesson', 'Num','Sush']
        return [col for col in columns if col not in excluded_columns]

    def on_column_selected(self, column):
        # Очищаем текущий слой с галочками
        self.clear_layout(self.layout_frame_centr2)
        self.label.setVisible(True)
        self.btn3.setVisible(True)
        self.current_column = column
        # Получаем список всех уникальных значений в выбранном столбце
        values = self.get_unique_values(self.current_sheet, column)
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
        if column == 'Kun' or column == 'Trans':
            self.clear_layout(self.layout_options2)  
            menu_op = 'Все слова', 'Только слова с кандзи', 'Слова без кандзи'
            self.menu_button2 = QComboBox()
            for i in menu_op:
                self.menu_button2.addItem(i)
            self.menu_button2.setCurrentText(menu_op[0])
            self.menu_button2.setStyleSheet(st.combobox)
            self.layout_options2.addWidget(self.menu_button2)   
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

    def checks(self):
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
            self.lb_err.setText('')
            self.df2 = self.xl.parse(self.current_sheet)
            self.alls  = self.df2.reset_index().to_dict('records')
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
            if self.current_column == 'Kun' or self.current_column=='Trans':
                if self.menu_button2.currentText() == 'Только слова с кандзи':
                    self.alls = [i for i in self.alls if i['Kanji'] != '0' and i['Kanji'] != 0]
                elif self.menu_button2.currentText() == 'Слова без кандзи':
                    self.alls = [i for i in self.alls if i['Kanji'] == '0' or i['Kanji'] == 0]
                else:
                    self.alls = [i for i in self.alls]
        if len(self.test_for_answer) == 1:
            self.alls_for_copy = [i for i in self.alls if str(i[self.test_for_answer[0]]) != '0' and str(i[self.current_column]) != '0']
        else:
            self.alls_for_copy = [i for i in self.alls if str(i[self.current_column]) != '0']
        self.alls = deepcopy(self.alls_for_copy)
        self.count_for_proc_funk()
        if self.check_r_or_st.isChecked():
            self.rand_check = 1
        else:
            self.rand_check = 0
        self.min_score()
        if self.current_sheet=='Dictio' and self.current_column=='Kanji' and len(self.test_for_answer) == 1 and self.test_for_answer[0] == 'Trans':
                keys_to_keep = set(item['Kanji'] for item in self.alls)
                self.stat2_t = {k: v for k, v in self.stat2_t.items() if k in keys_to_keep}
        self.main2()

    def check_new_words_for_stat(self): # Проверка и сравнение текстового файла Words и словаря в файле stat.txt
        df2 = read_excel('J_e_all_my.xlsx', sheet_name='Dictio')  # Блок для статистики2 и проверки новых слов
        with open('stat2.txt',encoding='utf-8') as f:
            data2 = f.read()
        self.stat2 = literal_eval(data2)
        if self.stat2 == {}:
            self.stat2 = dict.fromkeys(df2['Kanji'].values, 0)
        new_keys = df2['Kanji'].values
        for key in new_keys:
            if key not in self.stat2:
                self.stat2[key] = 0
        with open('stat2.txt', 'w+', encoding='utf-8') as file: # Сохраняем обновленную статистику в файл
            dump(self.stat2, file, indent='    ', ensure_ascii=False)
        self.stat2_t = deepcopy(self.stat2)
        new_stat = {name: {} for name in self.sheet_names} # Блок для статистики остальных слов
        self.alls_all_sheet = {}
        for i in new_stat:
            df_l = self.xl.parse(i)
            self.alls_all_sheet[i] = df_l.reset_index().to_dict('records')

        with open('stat.txt',encoding='utf-8') as f:
            data = f.read()
        self.stat = literal_eval(data)

        if self.stat == {}:
            self.stat = {name: {} for name in self.sheet_names}
        alls_coly = self.alls_all_sheet.copy()
        for s in alls_coly:
            for i in alls_coly[s]:
                j_dict = {}
                for j in i:
                    if j != 'Lesson' and j!='Num' and j!='Sush' and type(i[j]) != int and i[j] != '0':
                        j_dict[i[j]] = 0
                num_str = str(i['Num'])
                new_stat[s][num_str] = j_dict

        for k in new_stat:
            for i in new_stat[k]:
                if i not in self.stat[k]:
                    self.stat[k][i] = {}
                if self.stat[k][i] != new_stat[k][i]:
                    new_line = {}
                    for f in new_stat[k][i]:
                        if f not in self.stat[k][i]:
                            self.stat[k][i][f] = 0
                        stat_copy = self.stat[k].copy()
                        new_line[f] = stat_copy[i][f]
                        self.stat[k][i].pop(f)
                    self.stat[k][i] = new_line
        stat_copy = self.stat.copy()
        for i in stat_copy:
            copy_3 = stat_copy[i].copy()
            for j in copy_3:
                if j not in new_stat[i]:
                    del self.stat[i][j]
        with open('stat.txt', 'w+', encoding='utf-8') as fle:
            dump(self.stat, fle, indent='    ', ensure_ascii=False)

    def main2(self):
        self.frame_main.deleteLater()
        self.setGeometry(300, 300, 700, 600)
        self.frame_main = QFrame()
        self.frame_main.setStyleSheet("background-color: transparent;")

        self.frame_up2 = QFrame()
        self.frame_down2 = QFrame()
        self.frame_know = QFrame()
        self.btn_back = QPushButton("В начальное меню")
        self.btn_back.setStyleSheet(st.but_line_check)
        self.btn_save = QPushButton("Сохранить")
        self.btn_save.setStyleSheet(st.but_line_check)

        layout_frame_up2 = QHBoxLayout()
        layout_frame_up2.addWidget(self.btn_back)
        layout_frame_up2.addWidget(self.btn_save)
        self.frame_up2.setLayout(layout_frame_up2)

        self.btn_continue = QPushButton("Начать тест")
        self.btn_continue.setStyleSheet(st.btn_test) 
        self.btn_continue.setFixedHeight(40)
        self.btn_continue.setFixedWidth(400)
        self.label_stat = QLabel("Статистика слова")
        self.label_total = QLabel("Всего слов")
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
        layout_frame_down2.addWidget(self.label_stat)
        layout_frame_down2.addWidget(self.label_total)
        layout_frame_down2.addWidget(self.label_question)
        layout_frame_down2.addWidget(self.where_in_words_label)
        self.frame_down2.setLayout(layout_frame_down2)

        layout_frame_know = QVBoxLayout()
        self.but_know = QPushButton("Знаю")
        self.but_know.setVisible(False)
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(QRect(100, 150, 400, 400))
        self.table_widget.setStyleSheet(st.table)
        if len(self.test_for_answer) == 1:
            self.table_widget.setVisible(False)
        layout_frame_know.addWidget(self.but_know)
        layout_frame_know.addWidget(self.table_widget)
        layout_frame_know.addWidget(self.label_answer)
        self.frame_know.setLayout(layout_frame_know)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.frame_up2)
        self.main_layout.addWidget(self.frame_down2)
        self.main_layout.addWidget(self.frame_know)
        self.frame_main.setLayout(self.main_layout)
        self.scroll_with_backgr()
        self.btn_continue.clicked.connect(self.show_next_word)
        self.but_know.clicked.connect(self.know)
        self.btn_back.clicked.connect(self.back)
        self.btn_save.clicked.connect(self.save_progress)

    def repeat_frame(self):
        self.frame_repeat = QFrame()
        self.layout_frame_repeat = QVBoxLayout()  # Блок для повтора, статистики вернух слов и кнопки "Повторить"
        self.label_end = QLabel("")
        self.label_count_right = QLabel("")
        self.again_but = QPushButton("Повторить с нуля")
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
        self.layout_frame_repeat.addWidget(self.label_end)
        self.layout_frame_repeat.addWidget(self.label_count_right)
        self.layout_frame_repeat.addWidget(self.again_but)
        self.layout_frame_repeat.addWidget(self.again_label)
        self.layout_frame_repeat.addWidget(self.again_unknow)
        self.again_but.clicked.connect(self.reset_test)
        self.again_unknow.clicked.connect(self.retry_unknown_words)
        self.frame_repeat.setLayout(self.layout_frame_repeat)
        self.main_layout.addWidget(self.frame_repeat)

    def keyPressEvent(self, event):
            if event.key() == Qt.Key_Space:
                self.show_next_word()
            if event.key() == Qt.Key_Return:
                self.know()

    def show_next_word(self):
        self.btn_continue.setText("Следующее слово")
        if self.showing_translation:
            self.table_widget.clearContents()
            self.label_question.setStyleSheet('QTextEdit {color: black;}')
            self.label_question.setToolTip('')
            self.but_know.setVisible(True)
            self.but_know.setDisabled(True)
            self.but_know.setStyleSheet('QPushButton {background-color: red; color: white;}')
            self.showing_translation = False
            if self.past_word !='':
                if self.known_clicked == True:
                    self.known_clicked = False
                else:
                    self.unknown_words.append(self.past_word)
            
            if not self.alls: #Если все слова закончились
                self.label_question.setText("Тест завершен.")
                self.table_widget.setVisible(False)
                self.label_total.setText('')
                self.label_stat.setText('')
                self.label_answer.setText("")
                self.repeat_frame()
                self.again_but.setVisible(True)
                self.btn_continue.setVisible(False)
                self.btn_save.setVisible(False)
                self.but_know.setVisible(False)
                self.where_in_words_label.setText('')
                if self.unknown_words:
                    self.again_unknow.setVisible(True)
                if self.len_of_count_for_proc == 0:
                    self.label_count_right.setText('Нет слов для теста.')
                else:
                    prots = int(round((100 / self.len_of_count_for_proc * self.shet_know), 2))
                    self.label_count_right.setText(f'Общее число={self.len_of_count_for_proc}, Верно={self.shet_know}, процент верных = {prots}.')
                return
            if self.rand_check==1: #Если слова идут в случайном порядке
                self.current_word = choice(self.alls)
                self.current_word_test = self.current_word[self.current_column]
                if self.current_column == 'Kanji' or self.current_column=='Trans':
                    for i in self.alls:
                        if (self.current_column == 'Kanji' or self.current_column=='Trans') and self.current_sheet=='Dictio':
                            if i['Mnem']!=0 and i['Mnem']!='0':
                                self.label_stat.setText('есть мнемоника')
                                self.label_stat.setToolTip(i['Mnem'])
                            else:
                                self.label_stat.setText('')
                                self.label_stat.setToolTip('')
            else:
                if self.current_sheet=='Dictio' and self.current_column=='Kanji' and len(self.test_for_answer) == 1 and self.test_for_answer[0] == 'Trans':
                    if self.current_word_test != None:
                        del self.stat2_t[self.current_word_test]
                    self.current_word_test = min(self.stat2_t, key=self.stat2_t.get)
                    for i in self.alls:
                        if i['Kanji'] == self.current_word_test:
                            self.current_word = i
                    c_test = self.stat2_t[self.current_word_test]
                else:
                    rand_num = choice([key for key in self.stat_min_score if
                                self.stat_min_score[key] == min(self.stat_min_score.values())])
                    c_test = min(self.stat_min_score.values())
                    r = 'n'
                    for i in self.alls:
                        if i['Num'] == int(rand_num):
                            self.current_word = i
                            r = i[self.current_column]
                        if r != 'n':
                            break
                    self.current_word_test = r
                if (self.current_column == 'Kanji' or self.current_column=='Trans') and self.current_sheet=='Dictio': # для установки мнеоники
                    for i in self.alls:
                        if i[self.current_column] == self.current_word_test:
                            if i['Mnem']!=0 and i['Mnem']!='0':
                                self.mnemonic_text=', есть мнемоника'
                                self.label_stat.setToolTip(i['Mnem'])
                            else:
                                self.mnemonic_text=''
                                self.label_stat.setToolTip('')
                self.label_stat.setText('Статистика слова: ' + str(c_test)+str(self.mnemonic_text))
                if self.current_sheet=='Dictio' and self.current_column=='Kanji':
                    pass
                else:
                    del self.stat_min_score[rand_num]
            self.past_word = self.current_word
            t = f'Количество слов= {len(self.count_for_proc)}'
            self.label_total.setText(t)
            if self.current_sheet == 'Dictio' and self.current_column == 'Kanji':
                lines = []
                text=''
                for i in self.alls_words:
                    if self.current_word_test in i['Kanji'] and len(lines)<=5:
                        lines.append(i['Trans'])
                    if len(lines)>=1:
                        text = "Встречаются в словах:\n"+"\n".join(lines)
                        self.label_question.setToolTip(text)
                        self.label_question.setStyleSheet('QTextEdit {color: #8B0000;}')
            elif self.current_sheet == 'Dictio' and self.current_column =='Trans': #для нахождения встречающихся слов с переводом
                lines = []
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
            self.but_know.setDisabled(False)
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
            if len(self.test_for_answer) == 1:
                lines_translations=[]
                lines_for_delete =[]
                for i in self.alls:
                    if i[self.current_column]==self.current_word_test:
                        lines_translations.append(i[self.test_for_answer[0]])
                        lines_for_delete.append(i)
                self.translations = "\n".join(lines_translations)
                self.label_answer.setText(self.translations)
                for i in lines_for_delete:
                    self.alls.remove(i) 
                    self.min_score()
            else:
                self.translations = [self.current_word[prop] for prop in self.test_for_answer]
                self.update_table(self.translations,self.current_word_test)
            
    def reset_test(self):
        self.alls = deepcopy(self.alls_for_copy)
        self.stat2_t = deepcopy(self.stat2)
        self.count_for_proc_funk()
        self.unknown_words = []
        self.options_for_again()

    def retry_unknown_words(self):
        self.shet_know = 0
        self.alls = self.unknown_words
        self.stat2_t = deepcopy(self.stat2)
        self.count_for_proc_funk()
        self.unknown_words = []
        self.options_for_again()

    def count_for_proc_funk(self):
        for i in self.alls:
            if i[self.current_column] not in self.count_for_proc:
                self.count_for_proc.append(i[self.current_column])
        self.len_of_count_for_proc = len(self.count_for_proc)

    def options_for_again(self):
        self.btn_save.setVisible(True)
        self.min_score()
        if len(self.test_for_answer)==1:
            self.table_widget.setVisible(False)
        else:
            self.table_widget.setVisible(True)
        if self.current_sheet=='Dictio' and self.current_column=='Kanji':
            keys_to_keep = set(item['Kanji'] for item in self.alls)
            self.stat2_t = {k: v for k, v in self.stat2_t.items() if k in keys_to_keep}
        self.current_word = None
        self.current_word_test = None
        self.showing_translation = True
        self.label_question.setText("")
        self.label_answer.setText("")
        self.label_count_right.setText('')
        self.again_but.setVisible(False)
        self.btn_continue.setVisible(True)
        self.again_unknow.setVisible(False)
        self.frame_repeat.deleteLater()
        self.show_next_word()

    def know(self):
        if self.showing_translation:  # Обновляем статистику только если показано слово, а не перевод
            if self.known_clicked == False:
                self.shet_know += 1
                self.but_know.setStyleSheet('QPushButton {background-color: lime; color: white;}')
                if self.current_sheet=='Dictio' and self.current_column=='Kanji':
                    self.stat2[self.current_word_test] += 1
                    self.known_clicked = True
                    with open('stat2.txt', 'w+', encoding='utf-8') as file: # Сохраняем обновленную статистику в файл
                        dump(self.stat2, file, indent='    ', ensure_ascii=False)
                else:
                    for i in self.stat[self.current_sheet]:
                        if self.current_word_test in self.stat[self.current_sheet][i]:
                            self.stat[self.current_sheet][i][self.current_word_test] += 1
                            self.known_clicked = True
                            with open('stat.txt', 'w+', encoding='utf-8') as file: # Сохраняем обновленную статистику в файл
                                dump(self.stat, file, indent='    ', ensure_ascii=False)
                            break

    def min_score(self):
        self.stat_min_score = {}  # Второй сбор Словаря всех слов для теста (уже без нулевых значений)
        for i in self.alls:
            num_str = str(i['Num'])
            ku = i[self.current_column]
            self.stat_min_score[num_str] = {}
            self.stat_min_score[num_str] = self.stat[self.current_sheet][num_str][ku]

    def back(self):
        self.data_from_xls()
        self.options_for_zero()
        self.frame_main.deleteLater()
        self.main()

    def save_progress(self):
        data = {
            "test_type": self.current_column,
            "test_for_answer": self.test_for_answer,
            "remaining_words": self.alls,
            "checking_random": self.rand_check,
            "stat_min_score": self.stat_min_score,
            "current_sheet": self.current_sheet,
            "alls_for_copy": self.alls_for_copy,
            "count_for_proc":self.count_for_proc,
            "len_of_count_for_proc": self.len_of_count_for_proc,
            "stat2_t": self.stat2_t,
            "stat2": self.stat2,
            'stat': self.stat,
        }
        with open('test_progress.json', "w", encoding="utf-8") as file:
            dump(data, file, ensure_ascii=False, indent=4)
        QMessageBox.information(self, "Сохранение", "Прогресс сохранен. Напоминание- если у последнего элемента не посмотрели перевод, его в следующем тесте не будет")

    def is_file_empty(self,file_path):
        try:
            return os.stat(file_path).st_size == 0
        except FileNotFoundError:
            return False
        
    def load_progress(self):
        with open('test_progress.json', "r", encoding="utf-8") as file:
            data = load(file)
        self.current_column = data["test_type"]
        self.test_for_answer = data["test_for_answer"]
        self.alls = data["remaining_words"]
        self.stat_min_score = data["stat_min_score"]
        self.rand_check = data["checking_random"]
        self.current_sheet = data['current_sheet']
        self.alls_for_copy = data['alls_for_copy']
        self.count_for_proc = data['count_for_proc']
        self.len_of_count_for_proc = data['len_of_count_for_proc']
        self.stat2_t = data['stat2_t']
        self.stat2 = data['stat2']
        self.stat = data['stat']
        if self.current_sheet=='Dictio' and self.current_column=='Kanji' and len(self.test_for_answer) == 1 and self.test_for_answer[0] == 'Trans':
            keys_to_keep = set(item['Kanji'] for item in self.alls)
            self.stat2_t = {k: v for k, v in self.stat2_t.items() if k in keys_to_keep}
        self.main2()

    def clear_progress(self):
        with open(self.json_path, "w") as file:
            file.write("")
        self.but_contin.setVisible(False)
        self.clear_save.setVisible(False)

    def update_table(self,translations,current_word):
        # Удаление всех строк таблицы
        self.table_widget.setRowCount(0)
        
        # Установка количества столбцов
        self.table_widget.setColumnCount(len(self.test_for_answer) + 1)
        
        # Установка заголовков столбцов
        headers = [self.current_column]
        for i in self.test_for_answer:
            headers.append(i)
        self.table_widget.setHorizontalHeaderLabels(headers)

        header_font = QFont()
        header_font.setPointSize(18)  # Установите нужный размер шрифта
        header_font.setBold(True)
        #set font size for text in table
        font = QFont()
        font.setPointSize(18)
        self.table_widget.setFont(font)
        self.table_widget.horizontalHeader().setFont(header_font)
        self.table_widget.verticalHeader().setFont(header_font)
        
        filtered_words = []
        # Найти все строки, соответствующие критериям
        for i in self.alls:
            if i[self.current_column] == current_word:
                filtered_words.append(i)

        for word in filtered_words:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            
            # Вставить Кандзи
            item = QTableWidgetItem(word[self.current_column])
            self.table_widget.setItem(row, 0, item)
            
            # Вставить свойства из self.test_for_answer
            for i, prop in enumerate(self.test_for_answer, 1):
                item = QTableWidgetItem(word[prop])
                self.table_widget.setItem(row, i, item)
        for i in filtered_words:
            self.alls.remove(i) 
            self.min_score()

        header = self.table_widget.horizontalHeader()
        header.setStretchLastSection(True)
                
class BackgroundScrollArea(QScrollArea):
    def __init__(self, background_image_path, *args, **kwargs):
        super(BackgroundScrollArea, self).__init__(*args, **kwargs)
        self.background_image = QPixmap(background_image_path)

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.drawPixmap(0, 0, self.viewport().width(), self.viewport().height(), self.background_image)
        super(BackgroundScrollArea, self).paintEvent(event)