from pandas import DataFrame, ExcelWriter, concat
from PyQt5.QtWidgets import QTabWidget, QMessageBox,QGridLayout, QLabel, QCheckBox,QComboBox, QLineEdit, QPushButton,QTableWidget,QTableWidgetItem,QDialog, QVBoxLayout
from PyQt5.QtGui import QFont
import pandas as pd
from PyQt5.QtCore import QTimer

class TabDictio(QTabWidget):

    def __init__(self, df_dict, xl,parent=None):
        super().__init__(parent)
        self.parent = parent
        self.xl = xl
        self.sheet_names = self.xl.sheet_names
       # Задаем правильные типы данных при первой загрузке
        self.df_dict = self.prepare_dataframe(df_dict)

        # Добавляем таймер для автосохранения
        self.save_pending = False
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.auto_save)
        self.autosave_timer.start(30000)  # Автосохранение каждые 30 секунд
        
        # Проверка на дубликаты
        duplicated_nums = self.df_dict[self.df_dict['Num'].duplicated()]['Num'].tolist()
        if duplicated_nums:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Num {duplicated_nums} is duplicated in the table 'Dictio'")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            if msg.exec_() == QMessageBox.Ok:
                self.close()
                return

        self.sheets = {sheet_name: self.xl.parse(sheet_name) for sheet_name in self.sheet_names}
        self.chast_rechi = ['Сущ', 'Глаг', 'Прил', 'Нар']
        self.chast_rechi_for_filter = ['All','Сущ', 'Глаг', 'Прил', 'Нар']
        self.current_df = self.df_dict

        self.last_search_text = ""
        self.current_row_for_delete = None

        layout_frame_up = QGridLayout() # изменено на QGridLayout

        self.label_lesson = QLabel('Lesson')
        self.Lesson_d = QLineEdit()
        self.kanji_label = QLabel('Kanji')
        self.Kanji_d = QLineEdit()
        self.kun_label = QLabel('Kun')
        self.kun_d = QLineEdit()
        self.on_label = QLabel('On')
        self.on_d = QLineEdit()
        self.trans_label = QLabel('Trans')
        self.trans_d = QLineEdit()
        self.mnem_label = QLabel('Mnem')
        self.mnem_d = QLineEdit()
        self.sush = QComboBox()
        self.sush_label = QLabel('Sush')
        for i in self.chast_rechi:
            self.sush.addItem(i)

        layout_frame_up.addWidget(self.label_lesson, 0, 0)
        layout_frame_up.addWidget(self.Lesson_d, 0, 1)
        layout_frame_up.addWidget(self.kanji_label, 0, 2)
        layout_frame_up.addWidget(self.Kanji_d, 0, 3)
        layout_frame_up.addWidget(self.kun_label, 0, 4)
        layout_frame_up.addWidget(self.kun_d, 0, 5)
        layout_frame_up.addWidget(self.on_label,0,6)
        layout_frame_up.addWidget(self.on_d,0,7)
        layout_frame_up.addWidget(self.trans_label, 1, 0)
        layout_frame_up.addWidget(self.trans_d, 1, 1, 1, 3)
        layout_frame_up.addWidget(self.mnem_label, 1, 4)
        layout_frame_up.addWidget(self.mnem_d, 1, 5, 1, 7)
        layout_frame_up.addWidget(self.sush_label, 0, 8)
        layout_frame_up.addWidget(self.sush, 0, 9)
        self.button_add = QPushButton('Add to table')
        self.button_add.clicked.connect(self.add_data)
        layout_frame_up.addWidget(self.button_add, 3, 0)
        self.button_clear = QPushButton('Clear fields')
        self.button_clear.clicked.connect(self.clear_fields)
        layout_frame_up.addWidget(self.button_clear, 3, 2)
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['Lesson','Num','Kanj','On','Kun','Trans','Sush','Mnem'])
        self.table.setColumnHidden(1, True)  # Скрыть столбец 'Num'

        self.populate_table(self.df_dict)

        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 350)
        self.table.setColumnWidth(6, 100)

        self.set_table_font_size(16)

        layout_frame_up.addWidget(self.table, 4, 0, 1, 10)

        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        self.sort_order = 1
        search_button = QPushButton('Search')
        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("Search")
        self.search_line.setMaximumWidth(200)
        search_button.clicked.connect(self.search_next)
        layout_frame_up.addWidget(search_button, 5, 3)
        layout_frame_up.addWidget(self.search_line, 5, 4, 1, 2)

        self.button_delete = QPushButton('Delete')
        layout_frame_up.addWidget(self.button_delete, 5, 0)
        self.button_delete.clicked.connect(self.delete_data)
        self.undo_button = QPushButton('Undo')
        self.button_save = QPushButton('Save')
        self.button_save.clicked.connect(self.save_data)
        self.undo_button.clicked.connect(self.undo_data)
        layout_frame_up.addWidget(self.button_save, 12, 0)
        layout_frame_up.addWidget(self.undo_button, 12, 1)
        self.transfer_button = QPushButton('Transfer')
        self.transfer_button.clicked.connect(self.transfer_data)
        layout_frame_up.addWidget(self.transfer_button, 5, 1)
        self.transfer_button.setMaximumWidth(250)

        label_lesson = QLabel('Lesson from:')
        self.edit_lesson_from = QLineEdit()
        self.edit_lesson_to = QLineEdit()
        label_lesson_to = QLabel('Lesson to:')
        layout_frame_up.addWidget(label_lesson, 7, 0)
        layout_frame_up.addWidget(self.edit_lesson_from, 7, 1)
        layout_frame_up.addWidget(label_lesson_to, 7, 2)
        layout_frame_up.addWidget(self.edit_lesson_to, 7, 3)
        
        # Фильтр по Sush
        label_sush = QLabel('Sush filt:')
        self.combo_sush = QComboBox()
        self.combo_sush.addItems(self.chast_rechi_for_filter)
        self.combo_sush.setCurrentIndex(self.chast_rechi_for_filter.index('All'))
        layout_frame_up.addWidget(label_sush, 7, 4)
        layout_frame_up.addWidget(self.combo_sush, 7, 5)

        # Фильтр по Kanj
        label_kanj = QLabel('Kanji filt:')
        self.edit_kanj = QLineEdit()
        layout_frame_up.addWidget(label_kanj, 9, 0)
        layout_frame_up.addWidget(self.edit_kanj, 9, 1)
        
        # Фильтр по On
        label_on = QLabel('On filt:')
        self.edit_on = QLineEdit()
        layout_frame_up.addWidget(label_on, 9, 3)
        layout_frame_up.addWidget(self.edit_on, 9, 4)
        
        # Фильтр по Kun
        label_kun = QLabel('Kun filt:')
        self.edit_kun = QLineEdit()
        layout_frame_up.addWidget(label_kun, 10, 0)
        layout_frame_up.addWidget(self.edit_kun, 10, 1)

        self.kanji_without_zero = QCheckBox('!= 0')
        self.on_without_zero = QCheckBox('!= 0')
        self.kun_without_zero = QCheckBox('!= 0')

        layout_frame_up.addWidget(self.kanji_without_zero, 9, 2)
        layout_frame_up.addWidget(self.on_without_zero, 9, 5)
        layout_frame_up.addWidget(self.kun_without_zero, 10, 2)
        
        # Фильтр по Trans
        label_trans = QLabel('Trans filt:')
        self.edit_trans = QLineEdit()
        self.edit_trans.setMaximumWidth(200)
        layout_frame_up.addWidget(label_trans, 10, 3)
        layout_frame_up.addWidget(self.edit_trans, 10, 4,1,3)
        
        button_filter = QPushButton('Filter')
        button_filter.clicked.connect(self.filter)
        layout_frame_up.addWidget(button_filter, 11, 0)

        button_clear = QPushButton('Clear filter')
        button_clear.clicked.connect(self.clear_filters)
        layout_frame_up.addWidget(button_clear, 11, 2)

        button_show_duplicates = QPushButton('Duplicates')
        button_show_duplicates.clicked.connect(self.show_duplicates)
        layout_frame_up.addWidget(button_show_duplicates, 11, 3)

        self.setLayout(layout_frame_up)
        self.table.itemChanged.connect(self.update_data)

    def prepare_dataframe(self, df):
        """Подготовка DataFrame с правильными типами данных"""
        # Создаем копию, чтобы не изменять оригинал
        df = df.copy()
        
        # Определяем типы данных для каждого столбца
        dtype_dict = {
            'Lesson': 'int32',     # целые числа для уроков
            'Num': 'int32',        # целые числа для номеров
            'Kanji': 'string',     # строки для кандзи
            'On': 'string',        # строки для онов
            'Kun': 'string',       # строки для кунов
            'Trans': 'string',     # строки для переводов
            'Sush': 'string',      # строки для частей речи
            'Mnem': 'string'       # строки для мнемоники
        }
        
        # Заменяем пустые значения на '0' для строковых полей
        str_columns = ['Kanji', 'On', 'Kun', 'Mnem']
        for col in str_columns:
            df[col] = df[col].fillna('0')
        
        # Конвертируем типы данных
        for col, dtype in dtype_dict.items():
            if dtype == 'int32':
                # Для числовых столбцов сначала убеждаемся, что все значения числовые
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(dtype)
            else:
                df[col] = df[col].astype(dtype)
        
        return df

    def show_duplicates(self):
        duplicates = self.find_duplicates(self.df_dict)
        if duplicates:
            dlg = DuplicatesDialog(duplicates, self)
            dlg.exec_()
        else:
            QMessageBox.information(self, "Information", "No duplicates found.")
            
    def filter(self):
        df = self.df_dict.copy()
        # Фильтр по Lesson от и до
        lesson_from = self.edit_lesson_from.text()
        lesson_to = self.edit_lesson_to.text()

        if lesson_from:
            df = df[df['Lesson'] >= int(lesson_from)]
        if lesson_to:
            df = df[df['Lesson'] <= int(lesson_to)]

        # Фильтр по Sush
        sush = self.combo_sush.currentText()
        if sush != 'All':
            df = df[df['Sush'] == sush]

        # Все поля уже в string формате, не нужно преобразовывать
        if self.edit_kanj.text():
            df = df[df['Kanji'].str.contains(self.edit_kanj.text(), na=False)]
        
        if self.edit_on.text():
            df = df[df['On'].str.contains(self.edit_on.text(), na=False)]
        
        if self.edit_kun.text():
            df = df[df['Kun'].str.contains(self.edit_kun.text(), na=False)]
            
        if self.edit_trans.text():
            df = df[df['Trans'].str.contains(self.edit_trans.text(), na=False)]
       
        # Фильтры исключения нулей
        if self.kanji_without_zero.isChecked():
            df = df[df['Kanji'] != '0']
        if self.on_without_zero.isChecked():
            df = df[df['On'] != '0']
        if self.kun_without_zero.isChecked():
            df = df[df['Kun'] != '0']
            
        self.current_df = df
        self.populate_table(df)

    def clear_filters(self):
        self.edit_lesson_from.clear()
        self.edit_lesson_to.clear()
        self.combo_sush.setCurrentIndex(self.chast_rechi_for_filter.index('All'))
        self.edit_kanj.clear()
        self.edit_on.clear()
        self.edit_kun.clear()
        self.edit_trans.clear()
        self.kanji_without_zero.setChecked(False)
        self.on_without_zero.setChecked(False)
        self.kun_without_zero.setChecked(False)
        self.current_df = self.df_dict
        self.populate_table(self.df_dict)

    def set_table_font_size(self, font_size):
        font = QFont()
        font.setPointSize(font_size)

        for row in range(self.table.rowCount()):
            for col in range(1, 5):
                item = self.table.item(row, col)
                if item is not None:
                    item.setFont(font)

    def populate_table(self, df):
        """Заполнение таблицы данными"""
        df = df.sort_values(by='Num', ascending=False)
        
        self.table.setRowCount(0)
        for i, row_data in enumerate(df.values):
            self.table.insertRow(i)
            for j, cell_data in enumerate(row_data):
                self.table.setItem(i, j, QTableWidgetItem(str(cell_data)))
        self.set_table_font_size(16)

    def on_header_clicked(self, logical_index):
        if self.sort_order == 1:
            self.sort_order = 0
        else:
            self.sort_order = 1

        # Check if the clicked column is the 'Lesson' column
        if logical_index == 0:
            # Sort the DataFrame based on the numeric values of the 'Lesson' column
            self.current_df.sort_values(by='Lesson', ascending=self.sort_order, inplace=True, key=lambda col: col.astype(int))

            # Update the table with the sorted DataFrame
            for i, row_data in enumerate(self.current_df.values):
                for j, cell_data in enumerate(row_data):
                    self.table.setItem(i, j, QTableWidgetItem(str(cell_data)))
        else:
            # Sort the other columns using the default sorting method
            self.table.sortItems(logical_index, self.sort_order)
        self.set_table_font_size(16)

    def update_data(self, item):
        table_row = item.row()
        col = item.column()
        new_value = item.text()
        
        if not self.table.item(table_row, 1):
            return
            
        num = int(self.table.item(table_row, 1).text())
        matching_rows = self.df_dict[self.df_dict['Num'] == num]
        
        if matching_rows.empty:
            return
            
        index_in_df_dict = matching_rows.index[0]
        column_name = self.df_dict.columns[col]
        
        # Преобразуем значение в правильный тип данных
        try:
            if column_name in ['Lesson', 'Num']:
                new_value = int(new_value)
            else:
                new_value = str(new_value)
                
            self.df_dict.at[index_in_df_dict, column_name] = new_value
            self.save_pending = True
            self.button_save.setText("Save*")
        except ValueError:
            QMessageBox.warning(self, "Error", f"Invalid value for {column_name}")
            # Восстанавливаем предыдущее значение в ячейке
            item.setText(str(self.df_dict.at[index_in_df_dict, column_name]))

    def add_data(self):
        lesson = self.Lesson_d.text()
        trans = self.trans_d.text()
        
        if not trans.strip():
            QMessageBox.warning(self, "Error", "Translation is required")
            return
            
        if not lesson:
            QMessageBox.warning(self, "Error", "Lesson is required")
            return
        
        try:
            lesson = int(lesson)
        except ValueError:
            QMessageBox.warning(self, "Error", "Lesson must be a number")
            return
        
        new_num = self.df_dict['Num'].max() + 1 if not self.df_dict['Num'].empty else 1
        
        # Создаем словарь с новыми данными и явно указываем типы
        new_row = {
            'Lesson': int(lesson),
            'Num': int(new_num),
            'Kanji': str(self.Kanji_d.text() or '0'),
            'On': str(self.on_d.text() or '0'),
            'Kun': str(self.kun_d.text() or '0'),
            'Trans': str(trans),
            'Sush': str(self.sush.currentText()),
            'Mnem': str(self.mnem_d.text() or '0')
        }
        
        # Создаем новый DataFrame с одной строкой и правильными типами данных
        new_df = DataFrame([new_row])
        new_df = self.prepare_dataframe(new_df)
        
        # Добавляем строку в основной DataFrame
        self.df_dict = concat([self.df_dict, new_df], ignore_index=True)
        
        # Сортируем DataFrame
        self.df_dict = self.df_dict.sort_values(by='Num', ascending=False)
        
        # Обновляем всю таблицу
        self.populate_table(self.df_dict)
        
        # Очищаем поля ввода
        self.clear_fields()
        self.Lesson_d.clear()
        
        # Устанавливаем флаг несохраненных изменений
        self.save_pending = True
        self.button_save.setText("Save*")

    def transfer_data(self):
        current_row = self.table.currentRow()
        if current_row != -1:
            # Получить выбранную строку
            row_data = [self.table.item(current_row, col).text() for col in range(self.table.columnCount())]

            # Удалить эту строку из таблицы Dictio и из датафрейма self.df_dict
            num = int(row_data[1])
            for i in range(len(self.df_dict)):
                if int(self.df_dict['Num'].iloc[i]) == num:
                    self.df_dict = self.df_dict.drop([i])
                    break
            self.populate_table(self.df_dict)

            # Добавить эту строку в таблицу Words и в датафрейм self.df_w
            columns = ['Lesson', 'Num', 'Kanji', 'Read', 'Trans']
            row_data_words = [row_data[0], row_data[1], row_data[2], row_data[4], row_data[5]]
            new_data = DataFrame([row_data_words], columns=columns)
            self.parent.tab2.df_w = concat([self.parent.tab2.df_w, new_data], ignore_index=True)
            self.parent.tab2.populate_table(self.parent.tab2.df_w)

            # Сохранить изменения в файле эксель
            self.sheets['Dictio'] = self.df_dict
            self.sheets['Words'] = self.parent.tab2.df_w
            with ExcelWriter('J_e_all_my.xlsx', mode='w') as writer:
                for sheet_name, sheet_df in self.sheets.items():
                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)

    def delete_data(self):
        current_row = self.table.currentRow() # get the index of the selected row
        if current_row != -1: # if a row is selected
            num = int(self.table.item(current_row, 1).text()) # get the value of the 'Num' column of the selected row
            num = int(num) # Преобразовать значение в число
            for i in range(len(self.df_dict)):
                if int(self.df_dict['Num'].iloc[i]) == num:
                    self.current_row_for_delete = self.df_dict.iloc[i] # save the row that will be deleted
                    self.df_dict = self.df_dict.drop([i])
                    break
            self.df_dict = self.df_dict.reset_index(drop=True) # reset the index of the DataFrame
            self.sheets['Dictio'] = self.df_dict # update the 'Dictio' sheet in the sheets dictionary
            self.table.removeRow(current_row) # Remove the row from the table

    def undo_data(self):
        if self.current_row_for_delete is not None:
            self.df_dict = concat([self.df_dict, DataFrame([self.current_row_for_delete])], ignore_index=True)
            self.sheets['Dictio'] = self.df_dict
            self.populate_table(self.df_dict)

    def save_data(self):
        """Сохранение данных в Excel"""
        try:
            non_numeric_lessons = self.df_dict[~self.df_dict['Lesson'].astype(str).str.isnumeric()]['Lesson'].unique()
            if non_numeric_lessons.size > 0:
                msg = f"Недопустимое значение в столбце 'Lesson': {non_numeric_lessons}"
                QMessageBox.warning(self, 'Invalid Values', msg)
                return

            invalid_values = set(self.df_dict['Sush'].unique()) - set(self.chast_rechi)
            if invalid_values:
                msg = f"Недопустимое значение в столбце 'Сущ': {invalid_values}"
                QMessageBox.warning(self, 'Invalid Values', msg)
                return

            self.sheets['Dictio'] = self.df_dict.copy()
            with ExcelWriter('J_e_all_my.xlsx', mode='w') as writer:
                for sheet_name, sheet_df in self.sheets.items():
                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            self.save_pending = False  # Сбрасываем флаг несохраненных изменений
            self.button_save.setText("Save")  # Возвращаем обычный текст кнопки
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save data: {str(e)}")

    def clear_fields(self):
        self.Kanji_d.clear()
        self.kun_d.clear()
        self.on_d.clear()
        self.trans_d.clear()

    def search_next(self):
        search_text = self.search_line.text()

        # Find the next item after the current selection that matches the search text
        current_row = self.table.currentRow()
        current_col = self.table.currentColumn()
        for row in range(current_row, self.table.rowCount()):
            for col in range(current_col+1 if row == current_row else 0, self.table.columnCount()):
                item = self.table.item(row, col)
                if item is not None and search_text.lower() in item.text().lower():
                    self.table.setCurrentCell(row, col)
                    return

        # If no matches were found after the current selection, wrap around to the beginning of the table
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item is not None and search_text.lower() in item.text().lower():
                    self.table.setCurrentCell(row, col)
                    return

    # If no matches were found, display a warning message
        QMessageBox.warning(self, "Search", f"No more results found for '{search_text}'")

    def find_duplicates(self, df):
        duplicates = []

        # Удаляем строки, где Kun или Trans равны нулю
        df_filtered = df[(df['Kun'] != '0') & (df['Trans'] != '0')]

        # Ищем дубликаты по Kun
        kun_duplicates = df_filtered[df_filtered.duplicated(['Kun'], keep=False)]
        for index, row in kun_duplicates.iterrows():
            duplicates.append((row['Kun'], ''))

        # Ищем дубликаты по Trans
        trans_duplicates = df_filtered[df_filtered.duplicated(['Trans'], keep=False)]
        for index, row in trans_duplicates.iterrows():
            duplicates.append(('', row['Trans']))

        return duplicates
    
    def auto_save(self):
        """Автоматическое сохранение при наличии изменений"""
        if self.save_pending:
            self.save_data()

    def closeEvent(self, event):
        if self.save_pending:
            reply = QMessageBox.question(
                self, 'Save Changes',
                'You have unsaved changes. Would you like to save them?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            
            if reply == QMessageBox.Save:
                self.save_data()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()




class DuplicatesDialog(QDialog):
    def __init__(self, duplicates, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Duplicate Entries")
        layout = QVBoxLayout(self)
        # set size of the window
        self.resize(500, 300)

        # Создаем таблицу для отображения дубликатов
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)  # Два столбца: один для Kun, один для Trans
        self.table.setHorizontalHeaderLabels(['Kun', 'Trans'])
        self.populate_table(duplicates)

        layout.addWidget(self.table)

    def populate_table(self, duplicates):
        self.table.setRowCount(len(duplicates))
        for i, (kun, trans) in enumerate(duplicates):
            self.table.setItem(i, 0, QTableWidgetItem(kun))
            self.table.setItem(i, 1, QTableWidgetItem(trans))