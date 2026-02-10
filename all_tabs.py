# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (
    QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QComboBox, QCheckBox, QSpinBox, QLabel, QScrollArea,
    QFrame, QMessageBox, QAbstractItemView, QDoubleSpinBox, QApplication, QLineEdit
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon, QBrush, QColor
from pandas import ExcelFile, read_excel
import pandas as pd
from path_for_files import resource_path
import styles as st

SUSH_OPTIONS = ['Сущ', 'Прил', 'Глаг', 'Нар']
DEFAULT_ROWS = 1000
EXCEL_PATH = 'J_e_all_my.xlsx'


def _ensure_num_column(df):
    """Добавляет столбец Num если его нет (1, 2, 3, ...)."""
    if 'Num' not in df.columns:
        df.insert(0, 'Num', range(1, len(df) + 1))
    return df


class SheetTableWidget(QWidget):
    """Виджет одной вкладки: таблица + фильтры + кнопки."""

    def __init__(self, sheet_name, df, parent=None):
        super().__init__(parent)
        self.sheet_name = sheet_name
        self._parent_window = parent  # Table_window
        self._full_columns = list(df.columns)
        self._display_columns = [c for c in self._full_columns if c != 'Num']
        self._num_index = self._full_columns.index('Num') if 'Num' in self._full_columns else None
        self._num_values = []  # Num для каждой строки (включая добавленные)
        self._has_lesson = 'Lesson' in df.columns
        self._has_sush = 'Sush' in df.columns
        self._sush_col_index = self._display_columns.index('Sush') if 'Sush' in self._display_columns else None
        # поиск
        self._search_text = ""
        self._search_row = -1
        self._search_col = -1
        self._highlighted_row = -1
        # сортировка: при повторном клике по тому же столбцу — обратный порядок
        self._sort_column = None
        self._sort_ascending = True

        n = len(df)
        if 'Num' in df.columns:
            ser = pd.to_numeric(df['Num'], errors='coerce')
            self._num_values = []
            for i, v in enumerate(ser):
                if pd.isna(v):
                    self._num_values.append(i + 1)
                else:
                    try:
                        self._num_values.append(int(v))
                    except (TypeError, ValueError):
                        self._num_values.append(i + 1)
        else:
            self._num_values = list(range(1, n + 1)) if n else [1]
        # Добиваем до DEFAULT_ROWS пустыми строками (Num продолжаем)
        max_num = max(self._num_values) if self._num_values else 0
        for _ in range(n, DEFAULT_ROWS):
            max_num += 1
            self._num_values.append(max_num)

        self._build_ui(df)
        self._apply_filters()

    def _build_ui(self, df):
        layout = QVBoxLayout(self)

        # Фильтры: одна строка под заголовками
        filter_frame = QFrame()
        filter_layout = QHBoxLayout(filter_frame)
        self._filter_widgets = {}  # col_name -> widget(s)

        for col in self._display_columns:
            col_frame = QFrame()
            col_layout = QVBoxLayout(col_frame)
            col_layout.setContentsMargins(2, 2, 2, 2)
            if col == 'Lesson' and self._has_lesson:
                lab = QLabel('Lesson')
                col_layout.addWidget(lab)
                from_spin = QSpinBox()
                from_spin.setRange(-999999, 999999)
                from_spin.setSpecialValueText('от')
                to_spin = QSpinBox()
                to_spin.setRange(-999999, 999999)
                to_spin.setSpecialValueText('до')
                from_spin.setValue(-999999)
                to_spin.setValue(999999)
                row = QHBoxLayout()
                row.addWidget(from_spin)
                row.addWidget(QLabel('–'))
                row.addWidget(to_spin)
                col_layout.addLayout(row)
                self._filter_widgets[col] = ('lesson_range', from_spin, to_spin)
            elif col == 'Sush' and self._has_sush:
                lab = QLabel('Sush')
                col_layout.addWidget(lab)
                combo = QComboBox()
                combo.addItem('(все)', None)
                for v in SUSH_OPTIONS:
                    combo.addItem(v, v)
                combo.setCurrentIndex(0)
                col_layout.addWidget(combo)
                self._filter_widgets[col] = ('sush', combo)
            else:
                lab = QLabel(col[:8] + '…' if len(col) > 8 else col)
                lab.setToolTip(col)
                col_layout.addWidget(lab)
                combo = QComboBox()
                combo.addItem('(все)', None)
                combo.addItem('Пусто', 'empty')
                combo.addItem('Не пусто', 'not_empty')
                combo.addItem('0', 'zero')      # только нули
                combo.addItem('Не 0', 'not_zero')  # всё, что не ноль
                combo.setCurrentIndex(0)
                col_layout.addWidget(combo)
                self._filter_widgets[col] = ('empty_not', combo)
            filter_layout.addWidget(col_frame)

        filter_layout.addStretch()
        layout.addWidget(filter_frame)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(len(self._display_columns))
        self.table.setHorizontalHeaderLabels(self._display_columns)
        self.table.setRowCount(min(DEFAULT_ROWS, len(self._num_values)))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.table.setAlternatingRowColors(True)
        # показываем номера строк слева
        self.table.verticalHeader().setVisible(True)
        self.table.installEventFilter(self)

        # Заполняем из df
        n_data = len(df)
        for r in range(min(DEFAULT_ROWS, len(self._num_values))):
            for c, col in enumerate(self._display_columns):
                if col == 'Sush' and self._has_sush:
                    combo = QComboBox()
                    for v in SUSH_OPTIONS:
                        combo.addItem(v)
                    val = df.iloc[r][col] if r < n_data else ''
                    if pd.isna(val):
                        val = ''
                    val_str = str(val).strip()
                    idx = combo.findText(val_str) if val_str else -1
                    if idx >= 0:
                        combo.setCurrentIndex(idx)
                    else:
                        combo.setCurrentIndex(0)
                    self.table.setCellWidget(r, c, combo)
                else:
                    val = df.iloc[r][col] if r < n_data else ''
                    if pd.isna(val):
                        val = ''
                    item = QTableWidgetItem(str(val))
                    self.table.setItem(r, c, item)

        # Сортировка по клику на заголовок
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)

        layout.addWidget(self.table)

        # Панель поиска (Ctrl+F)
        self.search_frame = QFrame()
        search_layout = QHBoxLayout(self.search_frame)
        search_layout.addWidget(QLabel("Поиск:"))
        self.search_edit = QLineEdit()
        search_layout.addWidget(self.search_edit)
        self.search_next_btn = QPushButton("Найти далее")
        self.search_next_btn.setStyleSheet(st.but_line_check)
        search_layout.addWidget(self.search_next_btn)
        self.search_close_btn = QPushButton("X")
        self.search_close_btn.setFixedWidth(30)
        self.search_close_btn.setStyleSheet(st.but_line_check)
        search_layout.addWidget(self.search_close_btn)
        search_layout.addStretch()
        self.search_frame.setVisible(False)
        self.search_edit.returnPressed.connect(self._search_next)
        self.search_next_btn.clicked.connect(self._search_next)
        self.search_close_btn.clicked.connect(lambda: self.search_frame.setVisible(False))
        layout.addWidget(self.search_frame)

        # Кнопки + счётчик строк
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton('Сохранить')
        self.btn_save.setStyleSheet(st.btn_test)
        self.btn_save.clicked.connect(self._save_to_file)
        self.btn_add = QPushButton('Добавить 100 строк')
        self.btn_add.setStyleSheet(st.but_line_check)
        self.btn_add.clicked.connect(self._add_100_rows)
        self.rows_count_label = QLabel()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.rows_count_label)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def _is_row_empty(self, row_dict):
        """Строка считается пустой, если пусты все столбцы кроме Sush (в Sush часто стоит «Сущ» по умолчанию)."""
        for cname in self._display_columns:
            if cname == 'Sush':
                continue
            if str(row_dict.get(cname, '')).strip():
                return False
        return True

    def _on_header_clicked(self, logical_index):
        if logical_index < 0 or logical_index >= len(self._display_columns):
            return
        col = self._display_columns[logical_index]
        # Переключение направления при повторном клике по тому же столбцу
        if self._sort_column == col:
            self._sort_ascending = not self._sort_ascending
        else:
            self._sort_column = col
            self._sort_ascending = True
        # Собираем данные строк (с учётом виджетов)
        rows_data = []
        for r in range(self.table.rowCount()):
            row_dict = {}
            for c, cname in enumerate(self._display_columns):
                w = self.table.cellWidget(r, c)
                if w and isinstance(w, QComboBox):
                    row_dict[cname] = w.currentText()
                else:
                    it = self.table.item(r, c)
                    row_dict[cname] = it.text() if it else ''
            row_dict['_num'] = self._num_values[r] if r < len(self._num_values) else (r + 1)
            rows_data.append(row_dict)
        # Пустые строки (все ячейки пусты) — в конец таблицы, не участвуют в порядке сортировки
        non_empty = [x for x in rows_data if not self._is_row_empty(x)]
        empty_rows = [x for x in rows_data if self._is_row_empty(x)]
        try:
            if col == 'Lesson' and self._has_lesson:
                key_lesson = lambda x: (float(x.get(col, 0) or 0) if str(x.get(col, '')).strip() != '' else -1e9)
                non_empty.sort(key=key_lesson, reverse=not self._sort_ascending)
            else:
                key_text = lambda x: (str(x.get(col, '')).lower(), x['_num'])
                non_empty.sort(key=key_text, reverse=not self._sort_ascending)
        except Exception:
            key_text = lambda x: (str(x.get(col, '')).lower(), x['_num'])
            non_empty.sort(key=key_text, reverse=not self._sort_ascending)
        rows_data = non_empty + empty_rows
        self._num_values = [x['_num'] for x in rows_data]
        # Обновляем таблицу
        for r, row_dict in enumerate(rows_data):
            for c, cname in enumerate(self._display_columns):
                if cname == 'Sush' and self._has_sush:
                    w = self.table.cellWidget(r, c)
                    if w and isinstance(w, QComboBox):
                        idx = w.findText(str(row_dict.get(cname, '')))
                        w.setCurrentIndex(idx if idx >= 0 else 0)
                else:
                    it = self.table.item(r, c)
                    if it:
                        it.setText(str(row_dict.get(cname, '')))
        # после сортировки обновляем нумерацию и количество
        self._update_row_numbers_and_count()

    def _get_table_data(self):
        """Возвращает список dict по строкам (все столбцы включая Num)."""
        data = []
        for r in range(self.table.rowCount()):
            row = {}
            for i, col in enumerate(self._full_columns):
                if col == 'Num':
                    row[col] = self._num_values[r] if r < len(self._num_values) else (r + 1)
                    continue
                if col not in self._display_columns:
                    continue
                c = self._display_columns.index(col)
                w = self.table.cellWidget(r, c)
                if w and isinstance(w, QComboBox):
                    row[col] = w.currentText()
                else:
                    it = self.table.item(r, c)
                    row[col] = it.text() if it else ''
            data.append(row)
        return data

    def _apply_filters(self):
        lesson_from = lesson_to = None
        sush_val = None
        empty_filters = {}  # col -> 'empty' | 'not_empty' | 'zero' | 'not_zero' | None

        for col, w in self._filter_widgets.items():
            if w[0] == 'lesson_range':
                _, from_spin, to_spin = w
                lesson_from = from_spin.value() if from_spin.value() > -999999 else None
                lesson_to = to_spin.value() if to_spin.value() < 999999 else None
            elif w[0] == 'sush':
                sush_val = w[1].currentData()
            else:
                empty_filters[col] = w[1].currentData()

        for r in range(self.table.rowCount()):
            show = True
            for c, col in enumerate(self._display_columns):
                w = self.table.cellWidget(r, c)
                if w and isinstance(w, QComboBox):
                    val = w.currentText()
                else:
                    it = self.table.item(r, c)
                    val = (it.text() if it else '').strip()
                if col == 'Lesson' and self._has_lesson:
                    if lesson_from is not None or lesson_to is not None:
                        try:
                            v = float(val) if val else -1e9
                            if lesson_from is not None and v < lesson_from:
                                show = False
                                break
                            if lesson_to is not None and v > lesson_to:
                                show = False
                                break
                        except ValueError:
                            show = False
                            break
                elif col == 'Sush' and self._has_sush:
                    if sush_val is not None and val != sush_val:
                        show = False
                        break
                else:
                    ef = empty_filters.get(col)
                    if ef == 'empty' and val != '':
                        show = False
                        break
                    if ef == 'not_empty' and val == '':
                        show = False
                        break
                    if ef == 'zero':
                        # нули: строка '0' или '0.0'
                        if val not in ('0', '0.0'):
                            show = False
                            break
                    if ef == 'not_zero':
                        # всё, кроме нулей
                        if val in ('0', '0.0'):
                            show = False
                            break
            self.table.setRowHidden(r, not show)
        # после применения фильтров обновляем нумерацию и количество
        self._update_row_numbers_and_count()

    def _update_row_numbers_and_count(self):
        """Обновить порядковые номера видимых строк и счётчик."""
        count = 0
        for r in range(self.table.rowCount()):
            hidden = self.table.isRowHidden(r)
            if not hidden:
                count += 1
                self.table.setVerticalHeaderItem(r, QTableWidgetItem(str(count)))
            else:
                self.table.setVerticalHeaderItem(r, QTableWidgetItem(''))
        if hasattr(self, "rows_count_label") and self.rows_count_label is not None:
            self.rows_count_label.setText(f'Строк: {count}')

    def _connect_filter_signals(self):
        for col, w in self._filter_widgets.items():
            if w[0] == 'lesson_range':
                w[1].valueChanged.connect(self._apply_filters)
                w[2].valueChanged.connect(self._apply_filters)
            else:
                w[1].currentIndexChanged.connect(self._apply_filters)

    def eventFilter(self, obj, event):
        if obj is self.table and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
                self._copy_selection()
                return True
            if event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
                self._paste_selection()
                return True
            if event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
                # показать строку поиска
                if hasattr(self, "search_frame"):
                    self.search_frame.setVisible(True)
                    self.search_edit.setFocus()
                    # не сбрасываем текст, чтобы можно было повторять поиск
                return True
            if event.key() == Qt.Key_Delete:
                # Ctrl+Delete — удалить строки, просто Delete — очистить ячейки
                if event.modifiers() & Qt.ControlModifier:
                    self._delete_selected_rows()
                else:
                    self._clear_selection()
                return True
        return super().eventFilter(obj, event)

    def _cell_text(self, row, col):
        """Текст ячейки (для обычной ячейки или комбобокса Sush)."""
        w = self.table.cellWidget(row, col)
        if w and isinstance(w, QComboBox):
            return w.currentText()
        it = self.table.item(row, col)
        return it.text() if it else ''

    def _set_cell_text(self, row, col, text):
        """Установить текст ячейки."""
        col_name = self._display_columns[col] if col < len(self._display_columns) else None
        if col_name == 'Sush' and self._has_sush:
            w = self.table.cellWidget(row, col)
            if w and isinstance(w, QComboBox):
                idx = w.findText(str(text).strip())
                w.setCurrentIndex(idx if idx >= 0 else 0)
        else:
            it = self.table.item(row, col)
            if it:
                it.setText(str(text))
            else:
                self.table.setItem(row, col, QTableWidgetItem(str(text)))

    def _copy_selection(self):
        ranges = self.table.selectedRanges()
        if not ranges:
            r, c = self.table.currentRow(), self.table.currentColumn()
            if r >= 0 and c >= 0:
                text = self._cell_text(r, c)
                QApplication.clipboard().setText(text)
            return
        lines = []
        for rng in ranges:
            for row in range(rng.topRow(), rng.bottomRow() + 1):
                line = []
                for col in range(rng.leftColumn(), rng.rightColumn() + 1):
                    line.append(self._cell_text(row, col))
                lines.append('\t'.join(line))
        QApplication.clipboard().setText('\n'.join(lines))

    def _clear_selection(self):
        """Очистить содержимое выделенных ячеек (клавиша Delete)."""
        ranges = self.table.selectedRanges()
        if not ranges:
            r, c = self.table.currentRow(), self.table.currentColumn()
            if r >= 0 and c >= 0:
                self._set_cell_text(r, c, '')
            return
        for rng in ranges:
            for row in range(rng.topRow(), rng.bottomRow() + 1):
                for col in range(rng.leftColumn(), rng.rightColumn() + 1):
                    self._set_cell_text(row, col, '')

    def _delete_selected_rows(self):
        """Удалить выделенные строки (Ctrl+Delete)."""
        ranges = self.table.selectedRanges()
        rows = set()
        for rng in ranges:
            rows.update(range(rng.topRow(), rng.bottomRow() + 1))
        if not rows:
            r = self.table.currentRow()
            if r >= 0:
                rows.add(r)
        if not rows:
            return
        for r in sorted(rows, reverse=True):
            if 0 <= r < self.table.rowCount():
                self.table.removeRow(r)
                if 0 <= r < len(self._num_values):
                    del self._num_values[r]
        self._update_row_numbers_and_count()

    def _paste_selection(self):
        text = QApplication.clipboard().text()
        if not text:
            return
        lines = [line.split('\t') for line in text.replace('\r\n', '\n').split('\n') if line.strip()]
        if not lines:
            return
        row0, col0 = self.table.currentRow(), self.table.currentColumn()
        if row0 < 0:
            row0 = 0
        if col0 < 0:
            col0 = 0
        max_row = self.table.rowCount() - 1
        max_col = len(self._display_columns) - 1
        for r_offset, line in enumerate(lines):
            r = row0 + r_offset
            if r > max_row:
                break
            for c_offset, value in enumerate(line):
                c = col0 + c_offset
                if c > max_col:
                    break
                self._set_cell_text(r, c, value.strip())

    def _search_next(self):
        """Найти следующее вхождение текста из строки поиска."""
        if not hasattr(self, "search_edit"):
            return
        pattern = self.search_edit.text().strip()
        if not pattern:
            return
        # регистронезависимый поиск
        pattern_lower = pattern.lower()
        rows = self.table.rowCount()
        cols = len(self._display_columns)
        # если текст изменился — начинаем с начала
        if pattern != self._search_text:
            self._search_text = pattern
            self._search_row = -1
            self._search_col = -1
        start_row = self._search_row if self._search_row >= 0 else -1
        start_col = self._search_col + 1 if self._search_col >= 0 else 0

        # один проход от текущей позиции до конца, затем от начала
        def iterate(start_r, start_c):
            for r in range(start_r, rows):
                for c in range(start_c if r == start_r else 0, cols):
                    if self.table.isRowHidden(r):
                        continue
                    val = self._cell_text(r, c)
                    if pattern_lower in str(val).lower():
                        return r, c
            return None

        pos = None
        if start_row >= 0:
            pos = iterate(start_row, start_col)
        if pos is None:
            pos = iterate(0, 0)
        if pos is None:
            QMessageBox.information(self, "Поиск", "Ничего не найдено.")
            return
        r, c = pos
        self._search_row, self._search_col = r, c
        self.table.setCurrentCell(r, c)
        self._highlight_row(r)

    def _clear_highlight(self):
        """Снять подсветку с ранее найденной строки."""
        if self._highlighted_row < 0 or self._highlighted_row >= self.table.rowCount():
            self._highlighted_row = -1
            return
        row = self._highlighted_row
        palette = self.table.palette()
        base_brush = palette.base()
        alt_brush = palette.alternateBase()
        brush = base_brush if row % 2 == 0 else alt_brush
        for c in range(len(self._display_columns)):
            # не трогаем ячейки с виджетами (например, комбобокс Sush)
            if self.table.cellWidget(row, c) is not None:
                continue
            item = self.table.item(row, c)
            if item:
                item.setBackground(brush)
        self._highlighted_row = -1

    def _highlight_row(self, row):
        """Подсветить найденную строку синим цветом."""
        self._clear_highlight()
        if row < 0 or row >= self.table.rowCount():
            return
        highlight_brush = QBrush(QColor(135, 206, 250))  # светло-синий
        for c in range(len(self._display_columns)):
            # не трогаем ячейки с виджетами (например, комбобокс Sush)
            if self.table.cellWidget(row, c) is not None:
                continue
            item = self.table.item(row, c)
            if not item:
                # создаём item, чтобы можно было покрасить фон
                item = QTableWidgetItem(self._cell_text(row, c))
                self.table.setItem(row, c, item)
            item.setBackground(highlight_brush)
        self._highlighted_row = row

    def _add_100_rows(self):
        start = self.table.rowCount()
        max_num = max(self._num_values) if self._num_values else 0
        for i in range(100):
            r = start + i
            max_num += 1
            self._num_values.append(max_num)
            self.table.insertRow(r)
            for c, col in enumerate(self._display_columns):
                if col == 'Sush' and self._has_sush:
                    combo = QComboBox()
                    for v in SUSH_OPTIONS:
                        combo.addItem(v)
                    self.table.setCellWidget(r, c, combo)
                else:
                    self.table.setItem(r, c, QTableWidgetItem(''))
        # после добавления строк обновляем нумерацию и количество
        self._update_row_numbers_and_count()

    def _save_to_file(self):
        data = self._get_table_data()
        if not data:
            QMessageBox.information(self, 'Сохранение', 'Нет данных для сохранения.')
            return
        try:
            df_new = pd.DataFrame(data, columns=self._full_columns)
            # Приводим Num и Lesson к числовым типам для совместимости с jap_wind_test
            if 'Num' in df_new.columns:
                df_new['Num'] = pd.to_numeric(df_new['Num'], errors='coerce').fillna(0).astype(int)
            if 'Lesson' in df_new.columns:
                df_new['Lesson'] = pd.to_numeric(df_new['Lesson'], errors='coerce')
            xl = pd.ExcelFile(EXCEL_PATH, engine='openpyxl')
            sheets_dict = {name: xl.parse(name) for name in xl.sheet_names}
            sheets_dict[self.sheet_name] = df_new
            with pd.ExcelWriter(EXCEL_PATH, engine='openpyxl') as writer:
                for name, d in sheets_dict.items():
                    d.to_excel(writer, sheet_name=name, index=False)
            QMessageBox.information(self, 'Сохранение', f'Лист "{self.sheet_name}" сохранён в {EXCEL_PATH}.')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить: {e}')


class Table_window(QTabWidget):
    def __init__(self):
        super().__init__()
        try:
            self.xl = ExcelFile(EXCEL_PATH, engine='openpyxl')
        except Exception:
            self.xl = ExcelFile(EXCEL_PATH)
        self.sheet_names = self.xl.sheet_names
        self._tabs = {}

        for sheet_name in self.sheet_names:
            df = self.xl.parse(sheet_name)
            df = _ensure_num_column(df.copy())
            w = SheetTableWidget(sheet_name, df, self)
            w._connect_filter_signals()
            self._tabs[sheet_name] = w
            self.addTab(w, sheet_name)

        japanese_logo_path = resource_path('japanese_logo.png')
        self.setWindowIcon(QIcon(japanese_logo_path))
        self.setWindowTitle('Таблицы — ' + EXCEL_PATH)
