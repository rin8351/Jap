from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon

from others_scripts import resource_path
import styles
from jap_wind_test import Rand_window
from table import Table_window
from file_stats import StatsWindow
from ai_settings import AISettingsWindow

    
class Jap_app(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Jap_app, self).__init__(parent)
        
        # Transparent background
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # Background image
        background_image_path = resource_path('japanese_background.png')
        japanese_logo_path = resource_path('japanese_logo.png')
        self.background_image = QtGui.QPixmap(background_image_path)
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setPixmap(self.background_image)
        self.background_label.setGeometry(0, 0, self.background_image.width(), self.background_image.height())
        self.setWindowIcon(QIcon(japanese_logo_path)) 
        self.setWindowTitle('Menu')
        
        # Container for all widgets
        self.container = QtWidgets.QWidget(self)
        self.container.setStyleSheet('background-color: transparent')
        self.setCentralWidget(self.container)

        # Button style
        self.button_style = styles.button_style
        self.setStyleSheet(self.button_style)
        
        # Style for the word-count label
        self.label_style = styles.label_style
        
        self.container.setStyleSheet(self.label_style)

        # Frame with buttons and label
        self.frame_UP_main = QtWidgets.QFrame(self.container)
        self.frame_UP_main.setStyleSheet('background-color: rgba(255, 255, 255, 0.2); border-radius: 5px; padding: 10px')
        self.frame_UP_main_layout = QtWidgets.QVBoxLayout(self.frame_UP_main)

        self.btn1_1 = QtWidgets.QPushButton("Table", clicked=self.open_table_window)
        self.btn1_1.setStyleSheet(self.button_style)
        self.frame_UP_main_layout.addWidget(self.btn1_1)

        self.btn2 = QtWidgets.QPushButton("Test random", clicked=self.jap_rand_window)
        self.btn2.setStyleSheet(self.button_style)
        self.frame_UP_main_layout.addWidget(self.btn2)

        self.btn4 = QtWidgets.QPushButton('Stats',clicked = self.stats_window)
        self.btn4.setStyleSheet(self.button_style)
        self.frame_UP_main_layout.addWidget(self.btn4)

        self.btn_ai = QtWidgets.QPushButton("AI Settings", clicked=self.ai_settings_window)
        self.btn_ai.setStyleSheet(self.button_style)
        self.frame_UP_main_layout.addWidget(self.btn_ai)

        self.container_layout = QtWidgets.QVBoxLayout(self.container)
        self.container_layout.addWidget(self.frame_UP_main)
    
        self.setFixedSize(450, 450)

    def open_table_window(self):
        self.new_window2 = Table_window()
        self.new_window2.show()
            
    def jap_rand_window(self):
        self.new_window = Rand_window()
        self.new_window.show()

    def stats_window(self):
        self.new_window4 = StatsWindow()
        self.new_window4.show()

    def ai_settings_window(self):
        dialog = AISettingsWindow(self)
        dialog.exec_()
          
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Jap_app()
    window.show()
    app.exec_()
