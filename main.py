from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon

from pandas import ExcelFile

from others_scripts import resource_path
import styles
from jap_wind_test import Rand_window
from table import Table_window
from grammar import GrammarWindow
from file_stats import StatsWindow

    
class Jap_app(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Jap_app, self).__init__(parent)
        
        xl = ExcelFile('Jp.xlsx')
        words = xl.parse('Words')
        words.columns = words.columns.astype(str).str.strip()
        if 'Lesson' in words.columns:
            words = words[words['Lesson'].notna()]
        dictionar = xl.parse('Dictio')
        dictionar.columns = dictionar.columns.astype(str).str.strip()
        if 'Kanji' not in dictionar.columns:
            raise KeyError(
                f"В листе 'Dictio' не найден столбец 'Kanji'. "
                f"Столбцы в файле: {list(dictionar.columns)}"
            )
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
            st_full = str(i.get('Kanji', ''))
            if not st_full:
                continue
            st = st_full[0]
            if st != 0 and st != '0' and st not in alls_d2 and st not in hiragana:
                alls_d2.append(st)
        alls_d3 = []
        for i in alls_d:
            st2 = 5
            st = str(i.get('Kanji', ''))
            sush = i.get('Sush', '')
            for j in range(len(st)):
                if st[j] in hiragana and (sush == 'Глаг' and sush == 'Прил'):
                    st2 = 0
                    break
            if st == 0 or st == '0' or st2 == 0:
                alls_d3.append(i.get('Trans', ''))

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
        self.setWindowTitle('Menu')
        
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

        self.btn4 = QtWidgets.QPushButton('Stats',clicked = self.stats_window)
        self.btn4.setStyleSheet(self.button_style)
        self.frame_UP_main_layout.addWidget(self.btn4)

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
            
    def jap_rand_window(self):
        self.new_window = Rand_window()
        self.new_window.show()

    def stats_window(self):
        self.new_window4 = StatsWindow()
        self.new_window4.show()
          
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Jap_app()
    window.show()
    app.exec_()
