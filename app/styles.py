but_line_check = """
            QLineEdit, QCheckBox {
                background-color: white;
                border: 2px solid #A52A2A;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #A52A2A;
                color: white;
            }
            QPushButton:hover {
                background-color: #FF7373;
            }
        """

btn_test = """
            QPushButton {
                background-color: #FF4040;
                color: #FFFFFF;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FF7373;
                color: white;
                border: 2px solid white;
                border-radius: 5px;
            }
        """

checkbox = '''
                QCheckBox {
                    background-color: #FFFFFF;
                    border: 2px solid #A52A2A;
                    padding: 10px;
                    color: #A52A2A;
                }
            '''

radios = '''
                QRadioButton {
                    background-color: #FFFFFF;
                    border: 2px solid #A52A2A;
                    padding: 10px;
                    color: #A52A2A;
                }
            '''

context_menu = """
            QMenu {
                background-color: #f8f8f8;
                border: 1px solid #FF69B4;
            }
            QMenu::item {
                padding: 8px 36px 8px 36px;
            }
            QMenu::item:selected {
                background-color: #FF69B4;
                color: #FFFFFF;
            }
            """

button_style =  """
                QPushButton {
                    font: bold 12pt Arial;
                    color: #A52A2A;
                    background-color: transparent;
                    border: 1px solid white;
                    border-radius: 5px;
                    padding: 5px 10px;
                    text-align: left;
                }
                
                QPushButton:hover {
                    background-color: #CD5C5C;
                    color: #FFFFFF;
                }
            """

label_style = """
            QLabel {
                font: bold 12pt Arial;
                color: #A52A2A;
                background-color: transparent;
                border: none;
                border-radius: 5px;
                padding: 2px;
            }
        """

combobox = '''
            QComboBox {
                color: #A52A2A;
                background-color: white;
                border: 2px solid #A52A2A;
                border-radius: 5px;
                padding: 5px;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
            }
        '''

scroll = """QScrollBar:vertical {
        background-color: #F5F5F5;
        border: 1px solid #E8E8E8;
        width: 25px;
        margin: 15px 0 15px 0;
    }

    QScrollBar::handle:vertical {
        background-color: #800000;
        min-height: 20px;
    }

    QScrollBar::add-line:vertical {
        border: none;
        background-color: #E8E8E8;
        height: 15px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QScrollBar::sub-line:vertical {
        border: none;
        background-color: #E8E8E8;
        height: 15px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        border: none;
        background-color: #F5F5F5;
        height: 10px;
        width: 10px;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background-color: none;
    }"""

lb_err = """
            QLabel {
                font: bold 12pt Arial;
                color: #FF0000;
                background-color: transparent;
                border: none;
                border-radius: 5px;
                padding: 2px;
            }   
        """
table = """
    QTableWidget {
        background-color: white;
        gridline-color: #808080;
    }
    QHeaderView::section {
        background-color: #D3D3D3;
        padding: 4px;
        border: 1px solid #808080;
        font-weight: bold;
    }
    QTableCornerButton::section {
        background-color: #D3D3D3;
        border: 1px solid #808080;
    }
"""

main_style = """
        QPushButton {
            background-color: #FFBFBF;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: #FFBFBF;
            font: bold 14px;
            min-width: 4em;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #FFA7A7;
            border-color: #FFA7A7;
        }
        QWidget {
            background-color: #FFEEEB;
        }

        QTableView {
            background-color: #FFFFFF;
            font-size: 12pt;
            color: #7D7D7D;
        }

        QLabel {
            color: #7D7D7D;
            font-size: 12pt;
            font-weight: bold;
        }

        QComboBox {
            border: 2px solid #FFC8C8;
            border-radius: 10px;
            padding: 6px;
            font-size: 12pt;
            background-color: #FFF1F1;
            color: #7D7D7D;
        }

        QComboBox:hover {
            border: 2px solid #FF8F8F;
            background-color: #FFF6F6;
        }

        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left-width: 0px;
            border-left-color: rgba(255, 255, 255, 0);
            border-left-style: solid;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            background-color: #FFBFBF;
        }

        QComboBox QAbstractItemView {
            border: 2px solid #FFC8C8;
            selection-background-color: #FFBFBF;
            background-color: #FFF1F1;
            font-size: 12pt;
            color: #7D7D7D;
        }

        QLineEdit {
            border: 2px solid #FFC8C8;
            border-radius: 10px;
            padding: 6px;
            font-size: 12pt;
            background-color: #FFFFFF;
            color: #7D7D7D;
        }

        QLineEdit:focus {
            border: 2px solid #FF8F8F;
            background-color: #FFF6F6;
        }
        QCheckBox {
        color: #7D7D7D;
        font-size: 12pt;
        font-weight: bold; }

       QCheckBox::indicator {
        border: 2px solid #FFC8C8;
        border-radius: 4px;
        background-color: #FFFFFF;
        width: 20px;
        height: 20px;
    }

    QCheckBox::indicator:unchecked {
        background-color: #FFFFFF;
    }

    QCheckBox::indicator:checked {
        background-color: #FFBFBF;
    }

    QCheckBox::indicator:hover {
        border: 2px solid #FF8F8F;
    }
        """
tab_widget_style = """
        QTabWidget::pane {
            border: 2px solid gray;
            border-radius: 10px;
            margin-top: 6px;
        }

        QTabWidget::tab-bar {
            left: 5px;
        }

        QTabBar::tab {
            min-width: 150px;
            background-color: #FFBFBF;
            color: black;
            font-size: 12pt;
            font-weight: bold;
            border: 2px solid gray;
            border-radius: 10px;
            padding: 6px;
            margin-top: 6px;
            margin-bottom: -1px;
        }

        QTabBar::tab:selected {
            background-color: #FFA7A7;
            border-color: #FFA7A7;
        }
        """
minimalizm = """
            QPushButton {
                border: none;
                background-color: transparent;
                color: #555;
                font-size: 16px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                color: #000;
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 24px;
                margin-bottom: 20px;
            }
        """