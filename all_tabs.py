from PyQt5.QtWidgets import QTabWidget, QVBoxLayout
from tab_dictio import TabDictio
from tab_name import TabName
from tab_words import TabWords
from tab_frazes import TabFraze
from pandas import ExcelFile
from PyQt5.QtGui import QPalette, QColor,QIcon
import styles as st
from path_for_files import resource_path

class Table_window(QTabWidget):
    def __init__(self):
        super().__init__()

        # Load Excel file
        self.xl = ExcelFile('J_e_all_my.xlsx')
        self.df_dict = self.xl.parse('Dictio')
        self.df_n = self.xl.parse('Name')
        self.df_w = self.xl.parse('Words')
        self.df_fraz = self.xl.parse('Frazes')

        self.tabs = QTabWidget()
        self.tab1 = TabDictio(self.df_dict,self.xl,self)
        self.tab2 = TabWords(self.df_w,self.xl,self)
        self.tab3 = TabName(self.df_n,self.xl)
        self.tab4 = TabFraze(self.df_fraz,self.xl)
        self.setGeometry(0, 0, 1000, 800)
        japanese_logo_path = resource_path('japanese_logo.png')
        self.setWindowIcon(QIcon(japanese_logo_path)) 
        self.setWindowTitle("Tables")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 223, 223))  # Фоновый цвет окна
        palette.setColor(QPalette.Button, QColor(255, 191, 191))  # Цвет кнопок
        palette.setColor(QPalette.ButtonText, QColor(255, 0, 0))  # Цвет текста на кнопках
        palette.setColor(QPalette.Base, QColor(255, 223, 223))  # Цвет фона для таблицы и полей
        palette.setColor(QPalette.Text, QColor(0, 0, 0))  # Цвет текста для таблицы и полей

        self.setPalette(palette)
        self.setStyleSheet(st.main_style)
        self.tabs.setPalette(palette)
        self.tabs.setStyleSheet(st.tab_widget_style)

        self.tabs.addTab(self.tab1, "Dictio")
        self.tabs.addTab(self.tab2, "Words")
        self.tabs.addTab(self.tab3, "Name")
        self.tabs.addTab(self.tab4, "Frazes")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
