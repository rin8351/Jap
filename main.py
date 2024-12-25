from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon
from pandas import ExcelFile
import os
import sys
import styles
from jap_wind_test import Rand_window
from all_tabs import Table_window
from grammar import GrammarWindow


def resource_path(relative_path):
    """Get the absolute path to a resource in the bundled app or the local filesystem."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
class Jap_app(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Jap_app, self).__init__(parent)
        
        xl = ExcelFile('J_e_all_my.xlsx')
        words = xl.parse('Words')
        dictionar = xl.parse('Dictio')
        alls_w = words.reset_index().to_dict('records')
        alls_d = dictionar.reset_index().to_dict('records')
        self.alur=alls_d
       
        # блок для подсчета слов, кандзи и вывода на главный экран
        alls_d2 = []
        hiragana = ['ぱ', 'ば', 'だ', 'ざ', 'が', 'ん', 'わ', 'ら', 'や', 'ま', 'は', 'な', 'た', 'さ', 'か', 'あ', 'ぴ', 'び', 'ぢ', 'じ',
                    'ぎ', 'り', 'み', 'ひ', 'に', 'ち', 'し', 'き', 'い', 'ぷ', 'ぶ', 'づ', 'ず', 'ぐ', 'る', 'ゆ', 'む', 'ふ', 'ぬ', 'っ',
                    'す', 'く', 'う', 'ぺ', 'べ', 'で', 'ぜ', 'げ', 'れ', 'め', 'へ', 'ね', 'て', 'せ', 'け', 'え', 'ぽ', 'ぼ', 'ど', 'ぞ',
                    'ご', 'を', 'ろ', 'よ', 'も', 'ほ', 'の', 'と', 'そ', 'こ', 'お']
        
        for i in alls_d:
            st_full = str(i['Kanji'])
            st = st_full[0]
            if st != 0 and st != '0' and st not in alls_d2 and st not in hiragana:
                alls_d2.append(st)
        alls_d3 = []
        for i in alls_d:
            st2 = 5
            st = str(i['Kanji'])
            for j in range(len(st)):
                if st[j] in hiragana and (i['Sush'] == 'Глаг' and i['Sush'] == 'Прил'):
                    st2 = 0
                    break
            if st == 0 or st == '0' or st2 == 0:
                alls_d3.append(i['Trans'])

        # Устанавливаем прозрачный фон
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # Создаем фоновое изображение
        background_image_path = resource_path('japanese_background.png')
        japanese_logo_path = resource_path('japanese_logo.png')
        self.background_image = QtGui.QPixmap(background_image_path)
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setPixmap(self.background_image)
        self.background_label.setGeometry(0, 0, self.background_image.width(), self.background_image.height())
        self.setWindowIcon(QIcon(japanese_logo_path)) 
        self.setWindowTitle('Japannese apps')
        
        # Создаем контейнер для всех виджетов
        self.container = QtWidgets.QWidget(self)
        self.container.setStyleSheet('background-color: transparent')
        self.setCentralWidget(self.container)

        # Создаем стиль для кнопок
        self.button_style = styles.button_style
        self.setStyleSheet(self.button_style)
        
        # Создаем стиль для лейбла с количеством слов
        self.label_style = styles.label_style
        
        self.container.setStyleSheet(self.label_style)

        # Создаем рамку с кнопками и лейблом
        self.frame_UP_main = QtWidgets.QFrame(self.container)
        self.frame_UP_main.setStyleSheet('background-color: rgba(255, 255, 255, 0.2); border-radius: 5px; padding: 10px')
        self.frame_UP_main_layout = QtWidgets.QVBoxLayout(self.frame_UP_main)

        self.btn1 = QtWidgets.QPushButton("Open_table", clicked=self.table_excel)
        self.btn1.setStyleSheet(self.button_style)
        self.frame_UP_main_layout.addWidget(self.btn1)

        self.btn1_1 = QtWidgets.QPushButton("Table", clicked=self.to_table_excel)
        self.btn1_1.setStyleSheet(self.button_style)
        self.frame_UP_main_layout.addWidget(self.btn1_1)

        self.btn2 = QtWidgets.QPushButton("Test random", clicked=self.jap_rand_window)
        self.btn2.setStyleSheet(self.button_style)
        self.frame_UP_main_layout.addWidget(self.btn2)

        self.btn3 = QtWidgets.QPushButton('Grammar',clicked = self.grammar_test)
        #self.btn3.setDisabled(True)
        self.btn3.setStyleSheet(self.button_style)
        self.frame_UP_main_layout.addWidget(self.btn3)

        t = f'Kanji = {len(alls_d2)},\nWords = {len(alls_w)},\ntrans_words = {len(alls_d3)}.'
        self.lb_count = QtWidgets.QLabel(t)
        self.frame_UP_main_layout.addWidget(self.lb_count)
        self.lb_count.setStyleSheet(self.label_style)

        self.container_layout = QtWidgets.QVBoxLayout(self.container)
        self.container_layout.addWidget(self.frame_UP_main)
    
        self.resize(450, 450)

    def grammar_test(self):
        self.new_window3 = GrammarWindow()
        self.new_window3.show()

    def to_table_excel(self):
        self.new_window2 = Table_window()
        self.new_window2.show()
        
    def table_excel(self):
        self.file_path = 'J_e_all_my.xlsx'
        os.system("start "+self.file_path)
    
    def jap_rand_window(self):
        self.new_window = Rand_window()
        self.new_window.show()
          
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Jap_app()
    window.show()
    app.exec_()
