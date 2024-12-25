from pandas import DataFrame, ExcelWriter
from PyQt5.QtWidgets import QTabWidget, QMessageBox,QGridLayout, QLabel, QLineEdit, QPushButton,QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QFont
import pandas as pd

class TabName(QTabWidget):

    def __init__(self,df_n,xl):
        super().__init__()

        # Load Excel file
        self.xl = xl
        self.sheet_names = self.xl.sheet_names
        self.df_name = df_n
        self.df_name['Num'] = self.df_name['Num'].astype(int)

        for i in range(len(self.df_name)):
            if self.df_name['Num'].duplicated()[i]:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f"Num {self.df_name['Num'].iloc[i]} is duplicated in the table 'Dictio'")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                retval = msg.exec_()

                # Закрыть приложение, если пользователь нажал OK
                if retval == QMessageBox.Ok:
                    self.close()

        self.sheets = {sheet_name: self.xl.parse(sheet_name) for sheet_name in self.sheet_names}
        self.setGeometry(0, 0, 850, 800)
        self.current_df = self.df_name

        self.last_search_text = ""

        layout_frame_up = QGridLayout() # изменено на QGridLayout

        self.label_lesson = QLabel('Lesson')
        self.Lesson_d = QLineEdit()
        self.kanji_label = QLabel('Kanji')
        self.Kanji_d = QLineEdit()
        self.read_label = QLabel('Read')
        self.read_d = QLineEdit()

        layout_frame_up.addWidget(self.label_lesson, 0, 0)
        layout_frame_up.addWidget(self.Lesson_d, 0, 1)
        layout_frame_up.addWidget(self.kanji_label, 0, 2)
        layout_frame_up.addWidget(self.Kanji_d, 0, 3)
        layout_frame_up.addWidget(self.read_label, 0, 4)
        layout_frame_up.addWidget(self.read_d, 0, 5)
        self.button_add = QPushButton('Add to table')
        self.button_add.setMaximumWidth(100)
        self.button_add.clicked.connect(self.add_data)
        layout_frame_up.addWidget(self.button_add, 2, 0)
        self.button_clear = QPushButton('Clear fields')
        self.button_clear.clicked.connect(self.clear_fields)
        self.button_clear.setMaximumWidth(100)
        layout_frame_up.addWidget(self.button_clear, 2, 1)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Lesson','Num','Kanj','Read'])
        self.table.setColumnHidden(1, True)  # Скрыть столбец 'Num'

        self.populate_table(self.df_name)

        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 500)

        self.set_table_font_size(16)

        layout_frame_up.addWidget(self.table, 3, 0, 1, 6)

        # Связываем сигнал sectionClicked с обработчиком сортировки таблицы
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        self.sort_order = 1
        search_button = QPushButton('Search')
        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("Search")
        search_button.clicked.connect(self.search_next)
        layout_frame_up.addWidget(search_button, 4, 2)
        layout_frame_up.addWidget(self.search_line, 4, 3)

        self.button_delete = QPushButton('Delete')
        layout_frame_up.addWidget(self.button_delete, 4, 0)
        self.button_delete.clicked.connect(self.delete_data)
        self.button_save = QPushButton('Save')
        self.undo_button = QPushButton('Undo')
        self.undo_button.clicked.connect(self.undo_data)
        self.button_save.clicked.connect(self.save_data)
        layout_frame_up.addWidget(self.button_save, 11, 0)
        layout_frame_up.addWidget(self.undo_button, 11, 1)

        label_lesson = QLabel('Lesson from:')
        self.edit_lesson_from = QLineEdit()
        self.edit_lesson_from.setMaximumWidth(50)
        self.edit_lesson_to = QLineEdit()
        label_lesson_to = QLabel('Lesson to:')
        self.edit_lesson_to.setMaximumWidth(50)
        layout_frame_up.addWidget(label_lesson, 6, 0)
        layout_frame_up.addWidget(self.edit_lesson_from, 6, 1)
        layout_frame_up.addWidget(label_lesson_to, 6, 2)
        layout_frame_up.addWidget(self.edit_lesson_to, 6, 3)

        # Фильтр по Kanj
        label_kanj = QLabel('Kanji filt:')
        self.edit_kanj = QLineEdit()
        layout_frame_up.addWidget(label_kanj, 8, 0)
        layout_frame_up.addWidget(self.edit_kanj, 8, 1)
        
        # Фильтр по On
        label_read = QLabel('Read filt:')
        self.edit_read = QLineEdit()
        layout_frame_up.addWidget(label_read, 8, 2)
        layout_frame_up.addWidget(self.edit_read, 8, 3)
        
        button_filter = QPushButton('Filter')
        button_filter.setMaximumWidth(100)
        button_filter.clicked.connect(self.filter)
        layout_frame_up.addWidget(button_filter, 10, 0)

        button_clear = QPushButton('Clear filters')
        button_clear.clicked.connect(self.clear_filters)
        button_clear.setMaximumWidth(100)
        layout_frame_up.addWidget(button_clear, 10, 1)

        self.setLayout(layout_frame_up)

        self.table.itemChanged.connect(self.update_data)


    def filter(self):
        df = self.df_name.copy()
        # Фильтр по Lesson от и до
        lesson_from = self.edit_lesson_from.text()
        lesson_to = self.edit_lesson_to.text()
        df['Kanji'] = df['Kanji'].astype(str)
        df['Read'] = df['Read'].astype(str)
        df['Lesson'] = df['Lesson'].astype(int)
        if lesson_from:
            df = df[df['Lesson'] >= int(lesson_from)]
        if lesson_to:
            df = df[df['Lesson'] <= int(lesson_to)]
        # Фильтр по остальным полям
        kanji = str(self.edit_kanj.text())
        if kanji:
            df = df[df['Kanji'].str.contains(kanji)]
        # Фильтр по On
        read = self.edit_read.text()
        if read:
            df = df[df['Read'].str.contains(read)]
        self.current_df = df
        self.populate_table(df)

    def clear_filters(self):
        self.edit_lesson_from.clear()
        self.edit_lesson_to.clear()
        self.edit_kanj.clear()
        self.edit_read.clear()
        self.current_df = self.df_name
        self.populate_table(self.df_name)

    def populate_table(self, df):
        df['Num'] = df['Num'].astype(int)
        df = df.sort_values(by='Num', ascending=False)
        self.table.setRowCount(0)  # Clear existing rows
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
        self.df_name['Num'] = pd.to_numeric(self.df_name['Num'], errors='coerce')
        matching_rows = self.df_name[self.df_name['Num'] == num]
        if matching_rows.empty:  # if no such row exists
            return  # exit the function
        index_in_df_name = matching_rows.index[0]
        self.df_name.loc[index_in_df_name, self.df_name.columns[col]] = new_value

    def add_data(self):
        lesson = self.Lesson_d.text()
        if lesson =='':
            QMessageBox.about(self, "Error", "Lesson is empty")
            return
        else:
            lesson = int(lesson)
            kanji = self.Kanji_d.text()
            read = self.read_d.text()
            if kanji =='':
                kanji='0'
            if read =='':
                read='0'
            # Find the highest 'Num' value and increment it by one
            if self.df_name['Num'].empty:
                new_num = 1
            else:
                self.df_name['Num'] = self.df_name['Num'].astype(int)
                last_num = int(self.df_name['Num'].max())
                new_num = last_num + 1

            new_data = DataFrame([[lesson, new_num, kanji, read]], columns=['Lesson', 'Num', 'Kanji','Read'])
            self.df_name = self.df_name.append(new_data, ignore_index=True)
            self.sheets['Name'] = self.df_name
            with ExcelWriter('J_e_all_my.xlsx', mode='w') as writer:
                for sheet_name, sheet_df in self.sheets.items():
                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
            self.populate_table(self.df_name)

    def delete_data(self):
        current_row = self.table.currentRow() # get the index of the selected row
        if current_row != -1: # if a row is selected
            num = int(self.table.item(current_row, 1).text()) # get the value of the 'Num' column of the selected row
            num = int(num) # Преобразовать значение в число
            for i in range(len(self.df_name)):
                if int(self.df_name['Num'].iloc[i]) == num:
                    self.current_row_for_delete = self.df_name.iloc[i] # save the row that will be deleted
                    self.df_name = self.df_name.drop([i])
                    break
            self.df_name = self.df_name.reset_index(drop=True) 
            self.sheets['Name'] = self.df_name 
            self.table.removeRow(current_row) # Remove the row from the table

    def undo_data(self):
        if self.current_row_for_delete is not None:
            self.df_name = self.df_name.append(self.current_row_for_delete, ignore_index=True)
            self.sheets['Name'] = self.df_name
            self.populate_table(self.df_name)

    def save_data(self):
        non_numeric_lessons = self.df_name[~self.df_name['Lesson'].astype(str).str.isnumeric()]['Lesson'].unique()
        if non_numeric_lessons:
            msg = f"Не допустиемое значение в столбце 'Lesson': {non_numeric_lessons}"
            QMessageBox.warning(self, 'Invalid Values', msg)
            return
        else:
            self.sheets['Name'] = self.df_name.copy() 
            with ExcelWriter('J_e_all_my.xlsx', mode='w') as writer:
                for sheet_name, sheet_df in self.sheets.items():
                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)

    def clear_fields(self):
        self.Lesson_d.clear()
        self.Kanji_d.clear()
        self.read_d.clear()

    def set_table_font_size(self, font_size):
        font = QFont()
        font.setPointSize(font_size)

        for row in range(self.table.rowCount()):
            for col in range(1, 4):
                item = self.table.item(row, col)
                if item is not None:
                    item.setFont(font)


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