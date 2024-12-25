from PyQt5.QtWidgets import QMainWindow, QFrame, QLabel,QApplication,QPushButton,QHBoxLayout,QVBoxLayout,QCheckBox
from PyQt5.QtGui import QIcon,QFont
from path_for_files import resource_path
import styles as st
import random
from PyQt5.QtCore import Qt
from filling import lists_words
from filling import list_lessons
from fill_num import lists_words_num
from fill_suff import lists_words_suff
from fill_desu import lists_words_desu
from te_form import lists_teform
from ta_form_past import lists_taform

class GrammarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        japanese_logo_path = resource_path('japanese_logo.png')
        self.setWindowIcon(QIcon(japanese_logo_path)) # иконка окна
        self.setWindowTitle('Grammar test')
        QApplication.setFont(QFont("Roboto  ", 10))
        self.setGeometry(0, 0, 1000,600)
        self.setStyleSheet(st.minimalizm)
        self.frame_main = QFrame()
        self.main()
        self.list_lessons = list_lessons

    def main(self):
        self.frame_main.deleteLater()
        self.frame_main = QFrame()
        self.showing_answer= True
        self.button_grammar = QPushButton('Тест на грамматику- предложения со словами')
        self.button_copula = QPushButton('Тест на связки, время и вежливый/формальный стиль')
        self.button_numerals = QPushButton('Номерные суффиксы')
        self.button_suffixes = QPushButton('Суффиксы- смыслообразующие')
        self.button_teform = QPushButton('Те-формы, деепричастия')
        self.button_taform = QPushButton('Та-формы, прошй, простая форма')
        self.button_grammar.clicked.connect(self.grammar_t)
        self.button_numerals.clicked.connect(self.numerals_t)
        self.button_suffixes.clicked.connect(self.suffixes_t)
        self.button_copula.clicked.connect(self.copula_t)
        self.button_teform.clicked.connect(self.teform_t)
        self.button_taform.clicked.connect(self.taform_t)
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.button_grammar)
        layout.addWidget(self.button_copula)
        layout.addWidget(self.button_numerals)
        layout.addWidget(self.button_suffixes)
        layout.addWidget(self.button_teform)
        layout.addWidget(self.button_taform)
        layout.addStretch()
        self.frame_main.setLayout(layout)
        self.setCentralWidget(self.frame_main)
        
    def suffixes_t(self):
        self.spisok_all= lists_words_suff()
        self.test_style = 'suffixes'
        self.choose_language()

    def copula_t(self):
        self.spisok_all= lists_words_desu()
        self.test_style = 'copula'
        self.choose_language()

    def numerals_t(self):
        self.spisok_all= lists_words_num()
        self.test_style = 'numerals'
        self.choose_language()

    def grammar_t(self):
        self.spisok = lists_words()
        self.test_style = 'grammar'
        self.choose_language()

    def teform_t(self):
        self.spisok_all= lists_teform()
        self.test_style = 'teform'
        self.choose_language()

    def taform_t(self):
        self.spisok_all= lists_taform()
        self.test_style = 'taform'
        self.choose_language()

    def choose_language(self):
        self.frame_main.deleteLater()
        self.frame_main = QFrame()
        self.label = QLabel('Choose test')
        self.button_jap = QPushButton('From Japanese')
        self.button_russ = QPushButton('From Russian')
        self.button_back = QPushButton('Back')
        self.button_jap.clicked.connect(self.start_jap_test)
        self.button_russ.clicked.connect(self.start_russ_test)
        self.button_back.clicked.connect(self.main)
        self.hiragana_choose_checkbox = QCheckBox("Показывать хирагану")
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addStretch()
        main_layout.addWidget(self.button_jap)
        main_layout.addWidget(self.button_russ)
        main_layout.addWidget(self.button_back)
        main_layout.addWidget(self.hiragana_choose_checkbox)
        if self.test_style == 'grammar':
            label = QLabel('Lessons')
            main_layout.addWidget(label)
            self.list_checks = []
            for i in range(len(self.list_lessons)):
                self.list_checks.append(QCheckBox(self.list_lessons[i]))
                self.list_checks[i].setChecked(True)
                main_layout.addWidget(self.list_checks[i])
        main_layout.addStretch()
        self.frame_main.setLayout(main_layout)
        self.setCentralWidget(self.frame_main)

    def start_jap_test(self):
        self.type_test = 'japanesse'
        self.start_test()

    def start_russ_test(self):
        self.type_test = 'russian'
        self.start_test()

    def start_test(self):
        if self.test_style == 'grammar':
            self.spisok_all=[]
            self.checked_lesson = []
            for rb in self.list_checks:
                if rb.isChecked():
                    self.checked_lesson.append(rb.text())
            for i in self.checked_lesson:
                for j in self.spisok[i]:
                    self.spisok_all.append(j)
        self.frame_main.deleteLater()
        self.frame_main = QFrame()
        layout = QVBoxLayout()
        self.label_question = QLabel('')
        self.label_hiragana = QLabel('')
        self.label_answer = QLabel('')
        self.label_question.setWordWrap(True)
        self.label_hiragana.setWordWrap(True)
        self.label_answer.setWordWrap(True)
        layout.addWidget(self.label_question)
        layout.addWidget(self.label_hiragana)
        layout.addWidget(self.label_answer)
        buttons_layout = QHBoxLayout()
        self.button_next = QPushButton('Next')
        self.button_back = QPushButton('Back')
        self.button_next.clicked.connect(self.next_question)
        self.button_back.clicked.connect(self.main)
        buttons_layout.addWidget(self.button_back)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.button_next)
        layout.addLayout(buttons_layout)
        self.frame_main.setLayout(layout)
        self.setCentralWidget(self.frame_main)
        if self.hiragana_choose_checkbox.isChecked():
            self.hiragana_choose = 1
        else:
            self.hiragana_choose = 0
        self.next_question()

    def next_question(self):
        if self.showing_answer:
            if not self.spisok_all:
                self.label_question.setText('Test is completed')
                if self.test_style == 'grammar':
                    self.spisok= lists_words()
                    self.spisok_all=[]
                    for i in self.checked_lesson:
                        for j in self.spisok[i]:
                            self.spisok_all.append(j)
                elif self.test_style == 'numerals':
                    self.spisok_all= lists_words_num()
                elif self.test_style == 'suffixes':
                    self.spisok_all= lists_words_suff()
                elif self.test_style == 'copula':
                    self.spisok_all= lists_words_desu()
                elif self.test_style == 'teform':
                    self.spisok_all= lists_teform()
                elif self.test_style == 'taform':
                    self.spisok_all= lists_taform()
                self.label_answer.setText('')
                self.label_hiragana.setText('')
            else:
                self.current_question = random.choice(self.spisok_all)
                if self.type_test == 'japanesse':
                    self.label_question.setText(self.current_question[0])
                    self.current_answer = self.current_question[2]
                else:
                    self.label_question.setText(self.current_question[2])
                    self.current_answer = self.current_question[0]
                self.spisok_all.remove(self.current_question)
                self.label_answer.setText('')
                if self.hiragana_choose==1 and self.type_test == 'japanesse':
                    self.label_hiragana.setText(self.current_question[1])
                else:
                    self.label_hiragana.setText('')
                self.button_next.setEnabled(True)
                self.showing_answer= False
        else:
            if self.hiragana_choose==1 and self.type_test == 'japanesse':
                self.label_hiragana.setText(self.current_question[1])
            else:
                self.label_hiragana.setText('')
            self.showing_answer= True
            self.label_hiragana.setText(self.current_question[1])
            self.label_answer.setText(self.current_answer)

    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.next_question()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = GrammarWindow()
    ex.show()
    sys.exit(app.exec_())
        