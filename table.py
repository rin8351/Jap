# -*- coding: utf-8 -*-
"""
Окно таблиц: источник данных — SQLite (Jp.db).
Виджет использует QTableView + QSqlTableModel (виртуализация: в памяти только видимые строки).
При первом запуске, если БД пуста, данные импортируются из Jp.xlsx.
"""
from PyQt5.QtWidgets import (
    QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QTableView, QHeaderView,
    QPushButton, QComboBox, QSpinBox, QLabel, QFrame, QMessageBox,
    QAbstractItemView, QApplication, QLineEdit, QStyledItemDelegate
)
from PyQt5.QtCore import Qt, QEvent, QIdentityProxyModel
from PyQt5.QtGui import QIcon, QBrush, QColor, QFont
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
import re
import pandas as pd
from others_scripts import resource_path
import styles as st
from table_logger import table_log, clear_table_log

SUSH_OPTIONS = ['Сущ', 'Прил', 'Глаг', 'Нар']
DB_PATH = 'Jp.db'
EXCEL_PATH = 'Jp.xlsx'
COLUMN_FONT_SIZES = {'Kanji': 14, 'On': 12, 'Kun': 12, 'Read': 12}
# Порядок вкладок: сначала листы из этого списка, остальные — после (в исходном порядке)
SHEET_DISPLAY_ORDER = ['Dictio', 'Words']


def _ensure_num_column(df):
    """Добавляет столбец Num если его нет (1, 2, 3, ...)."""
    if 'Num' not in df.columns:
        df.insert(0, 'Num', range(1, len(df) + 1))
    return df


def _sanitize_table_name(sheet_name):
    """Имя листа -> имя таблицы SQLite (без пробелов и спецсимволов)."""
    return re.sub(r'[^\w]', '_', str(sheet_name).strip()) or 'Sheet'


def _quote_ident(name):
    """Экранирование имени столбца для SQL."""
    return '"' + str(name).replace('"', '""') + '"'


# --- Инициализация БД ---

def get_connection():
    """Возвращает подключение к SQLite (коннект по имени 'tables')."""
    name = 'tables'
    if name not in QSqlDatabase.connectionNames():
        db = QSqlDatabase.addDatabase('QSQLITE', name)
        db.setDatabaseName(DB_PATH)
        if not db.open():
            return None
    db = QSqlDatabase.database(name)
    return db if db.isOpen() else None


# Схема по умолчанию, если при пустой БД нет Excel (имя_таблицы -> список столбцов)
_DEFAULT_SCHEMA = {
    'Dictio': ['Num', 'Lesson', 'Kanji', 'On', 'Kun', 'Trans', 'Sush', 'Mnem'],
    'Words': ['Num', 'Lesson', 'Kanji', 'On', 'Kun', 'Trans', 'Sush', 'Mnem'],
}


def _create_empty_table(q, table_name, columns):
    """Создаёт одну пустую таблицу с заданными столбцами."""
    SUSH_CHECK = "CHECK({col} IN ('Сущ', 'Прил', 'Глаг', 'Нар'))"
    parts = []
    for col in columns:
        col_quoted = _quote_ident(col)
        if col == 'Num' or col == 'Lesson':
            parts.append(f'{col_quoted} INTEGER')
        elif col == 'Sush':
            parts.append(f'{col_quoted} TEXT {SUSH_CHECK.format(col=col_quoted)}')
        else:
            parts.append(f'{col_quoted} TEXT')
    create_sql = f'CREATE TABLE {_quote_ident(table_name)} ({", ".join(parts)})'
    return q.exec_(create_sql)


def init_db():
    """
    Открывает Jp.db. Если БД пуста (нет таблиц), создаёт только структуру таблиц (без данных).
    Данные из Excel не подгружаются — база остаётся пустой для заполнения пользователем.
    Возвращает True при успехе.
    """
    db = get_connection()
    if not db or not db.isOpen():
        return False
    q = QSqlQuery(db)
    q.exec_("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    has_tables = q.next()
    if has_tables:
        return True
    # Пустая БД: создаём только структуру таблиц (без импорта данных из Excel)
    try:
        xl = pd.ExcelFile(EXCEL_PATH, engine='openpyxl')
    except Exception:
        try:
            xl = pd.ExcelFile(EXCEL_PATH)
        except Exception:
            xl = None
    if xl is not None and xl.sheet_names:
        for sheet_name in xl.sheet_names:
            try:
                df = xl.parse(sheet_name)
                df.columns = df.columns.astype(str).str.strip()
                df = _ensure_num_column(df.copy())
                table_name = _sanitize_table_name(sheet_name)
                if not _create_empty_table(q, table_name, list(df.columns)):
                    table_log('DB_INIT', error=f'CREATE TABLE {table_name}: {q.lastError().text()}')
            except Exception as e:
                table_log('DB_INIT', error=f'Sheet {sheet_name}: {e}')
    else:
        # Нет Excel или не удалось прочитать — создаём таблицы по умолчанию
        for table_name, columns in _DEFAULT_SCHEMA.items():
            if not _create_empty_table(q, table_name, columns):
                table_log('DB_INIT', error=f'CREATE TABLE {table_name}: {q.lastError().text()}')
    return True


def get_sheet_names():
    """Список имён листов (таблиц в БД). Имена таблиц возвращаем как есть (для отображения вкладок — маппинг table_name -> sheet_name не делаем, имена совпадают если в Excel без пробелов)."""
    db = get_connection()
    if not db or not db.isOpen():
        return []
    q = QSqlQuery(db)
    q.exec_("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    names = []
    while q.next():
        names.append(q.value(0))
    return names


def get_sheet_names_for_display():
    """Список имён листов в порядке отображения вкладок (см. SHEET_DISPLAY_ORDER)."""
    names = get_sheet_names()
    ordered = [n for n in SHEET_DISPLAY_ORDER if n in names]
    for n in names:
        if n not in SHEET_DISPLAY_ORDER:
            ordered.append(n)
    return ordered


def get_table_columns(table_name):
    """Список имён столбцов таблицы в БД."""
    db = get_connection()
    if not db or not db.isOpen():
        return []
    q = QSqlQuery(db)
    q.exec_(f'PRAGMA table_info({_quote_ident(table_name)})')
    cols = []
    while q.next():
        cols.append(q.value(1))
    return cols


# --- Делегаты для ячеек ---

class SushDelegate(QStyledItemDelegate):
    """Столбец Sush: выбор из списка Сущ/Прил/Глаг/Нар."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.options = SUSH_OPTIONS

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        for o in self.options:
            combo.addItem(o)
        return combo

    def setEditorData(self, editor, index):
        v = index.model().data(index, Qt.EditRole) or ''
        i = editor.findText(str(v).strip())
        editor.setCurrentIndex(i if i >= 0 else 0)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)


class LessonDelegate(QStyledItemDelegate):
    """Lesson: отображать целое число без .0."""
    def displayText(self, value, locale):
        if value is None or value == '':
            return ''
        try:
            v = float(value)
            if v == int(v):
                return str(int(v))
            return str(value)
        except (TypeError, ValueError):
            return str(value)


class ColumnFontDelegate(QStyledItemDelegate):
    """Делегат: задаёт размер шрифта для столбца по COLUMN_FONT_SIZES."""
    def __init__(self, column_name, parent=None):
        super().__init__(parent)
        self._column_name = column_name
        self._font_size = COLUMN_FONT_SIZES.get(column_name)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if self._font_size is not None:
            font = QFont(option.font)
            font.setPointSize(self._font_size)
            option.font = font


class HighlightProxyModel(QIdentityProxyModel):
    """Прокси-модель: подсвечивает строку поиска синим фоном (BackgroundRole)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._highlighted_row = -1

    def setHighlightedRow(self, row):
        if self._highlighted_row == row:
            return
        old = self._highlighted_row
        self._highlighted_row = row
        cols = self.columnCount()
        if cols <= 0:
            return
        if old >= 0:
            top_left = self.index(old, 0)
            bottom_right = self.index(old, cols - 1)
            self.dataChanged.emit(top_left, bottom_right)
        if row >= 0:
            top_left = self.index(row, 0)
            bottom_right = self.index(row, cols - 1)
            self.dataChanged.emit(top_left, bottom_right)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.BackgroundRole and index.isValid() and index.row() == self._highlighted_row:
            return QBrush(QColor(173, 216, 230))  # светло-синий
        return super().data(index, role)


# --- Виджет вкладки с таблицей (SQLite + виртуализация) ---

class SheetTableWidget(QWidget):
    """Одна вкладка: QTableView + QSqlTableModel, фильтры (SQL WHERE), поиск, добавление строк, сохранение в БД."""

    def __init__(self, sheet_name, parent=None):
        super().__init__(parent)
        self.sheet_name = sheet_name
        self._parent_window = parent
        self._table_name = _sanitize_table_name(sheet_name)
        self._columns = get_table_columns(self._table_name)
        if not self._columns:
            self._columns = ['Num', 'Lesson', 'Kanji', 'On', 'Kun', 'Trans', 'Sush', 'Mnem']
        self._display_columns = [c for c in self._columns if c != 'Num']
        self._has_lesson = 'Lesson' in self._columns
        self._has_sush = 'Sush' in self._columns
        self._search_text = ""
        self._search_row = -1
        self._search_col = -1
        self._highlighted_row = -1
        self._sort_column = None
        self._sort_ascending = True

        self._build_ui()
        self._apply_filters()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Фильтры
        filter_frame = QFrame()
        filter_layout = QHBoxLayout(filter_frame)
        self._filter_widgets = {}
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
                combo.addItem('0', 'zero')
                combo.addItem('Не 0', 'not_zero')
                combo.setCurrentIndex(0)
                col_layout.addWidget(combo)
                self._filter_widgets[col] = ('empty_not', combo)
            filter_layout.addWidget(col_frame)
        filter_layout.addStretch()
        layout.addWidget(filter_frame)

        # Модель и представление
        self._model = QSqlTableModel(self, get_connection())
        self._model.setTable(self._table_name)
        self._model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self._model.select()
        self._fetch_all()
        self._proxy = HighlightProxyModel(self)
        self._proxy.setSourceModel(self._model)
        self.table = QTableView()
        self.table.setModel(self._proxy)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(True)
        self.table.installEventFilter(self)
        # Делегаты (в т.ч. размер шрифта по COLUMN_FONT_SIZES)
        for c in range(self._model.columnCount()):
            col_name = self._columns[c] if c < len(self._columns) else ''
            if col_name == 'Sush':
                self.table.setItemDelegateForColumn(c, SushDelegate(self.table))
            elif col_name == 'Lesson':
                self.table.setItemDelegateForColumn(c, LessonDelegate(self.table))
            elif col_name in COLUMN_FONT_SIZES:
                self.table.setItemDelegateForColumn(c, ColumnFontDelegate(col_name, self.table))
        # Не показывать столбец Num
        if 'Num' in self._columns:
            self.table.setColumnHidden(self._columns.index('Num'), True)
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        layout.addWidget(self.table)

        # Поиск
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
        self.search_close_btn.clicked.connect(self._close_search)
        layout.addWidget(self.search_frame)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton('Сохранить')
        self.btn_save.setStyleSheet(st.btn_test)
        self.btn_save.clicked.connect(self._save_to_db)
        self.btn_add = QPushButton('Добавить 10 строк')
        self.btn_add.setStyleSheet(st.but_line_check)
        self.btn_add.clicked.connect(self._add_10_rows)
        self.rows_count_label = QLabel()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.rows_count_label)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self._connect_filter_signals()
        self._update_count()

    def _connect_filter_signals(self):
        for col, w in self._filter_widgets.items():
            if w[0] == 'lesson_range':
                w[1].valueChanged.connect(self._apply_filters)
                w[2].valueChanged.connect(self._apply_filters)
            else:
                w[1].currentIndexChanged.connect(self._apply_filters)

    def _build_where(self):
        """Собирает WHERE из виджетов фильтров."""
        conditions = []
        for col, w in self._filter_widgets.items():
            qcol = _quote_ident(col)
            if w[0] == 'lesson_range':
                _, from_spin, to_spin = w
                v_from = from_spin.value()
                v_to = to_spin.value()
                if v_from > -999999:
                    conditions.append(f'{qcol} >= {v_from}')
                if v_to < 999999:
                    conditions.append(f'{qcol} <= {v_to}')
            elif w[0] == 'sush':
                val = w[1].currentData()
                if val is not None:
                    escaped = str(val).replace("'", "''")
                    conditions.append(f"{qcol} = '{escaped}'")
            else:
                ef = w[1].currentData()
                if ef == 'empty':
                    conditions.append(f'({qcol} IS NULL OR {qcol} = \'\')')
                elif ef == 'not_empty':
                    conditions.append(f'({qcol} IS NOT NULL AND {qcol} != \'\')')
                elif ef == 'zero':
                    conditions.append(f'({qcol} = \'0\' OR {qcol} = \'0.0\')')
                elif ef == 'not_zero':
                    conditions.append(f'({qcol} IS NULL OR {qcol} = \'\' OR ({qcol} != \'0\' AND {qcol} != \'0.0\'))')
        if not conditions:
            return ''
        return ' AND '.join(conditions)

    def _apply_filters(self):
        self._model.submitAll()
        where = self._build_where()
        self._model.setFilter(where)
        self._do_select()
        table_log('FILTER', sheet=self.sheet_name)

    def _on_header_clicked(self, logical_index):
        if logical_index < 0 or logical_index >= len(self._columns):
            return
        col = self._columns[logical_index]
        if self._sort_column == col:
            self._sort_ascending = not self._sort_ascending
        else:
            self._sort_column = col
            self._sort_ascending = True
        order = Qt.AscendingOrder if self._sort_ascending else Qt.DescendingOrder
        self._model.submitAll()
        self._model.setSort(logical_index, order)
        self._do_select()
        table_log('SORT', sheet=self.sheet_name, column=col, ascending=self._sort_ascending)

    def _update_count(self):
        if hasattr(self, 'rows_count_label') and self.rows_count_label is not None:
            self.rows_count_label.setText(f'Строк: {self._model.rowCount()}')

    def _fetch_all(self):
        """Загружает все строки из БД (убирает ленивую подгрузку при прокрутке)."""
        while self._model.canFetchMore():
            self._model.fetchMore()

    def _save_view_state(self):
        """Запоминает позицию скролла и текущую ячейку."""
        idx = self.table.currentIndex()
        return (
            self.table.verticalScrollBar().value(),
            self.table.horizontalScrollBar().value(),
            idx.row(),
            idx.column(),
        )

    def _restore_view_state(self, state):
        """Восстанавливает позицию скролла и текущую ячейку."""
        vscroll, hscroll, row, col = state
        self.table.verticalScrollBar().setValue(vscroll)
        self.table.horizontalScrollBar().setValue(hscroll)
        if row >= 0:
            max_row = self._proxy.rowCount() - 1
            if max_row >= 0:
                r = min(row, max_row)
                c = max(0, col)
                idx = self._proxy.index(r, c)
                if idx.isValid():
                    self.table.setCurrentIndex(idx)

    def _do_select(self, keep_position=False):
        """select() + загрузка всех строк + обновление счётчика.
        keep_position=True сохраняет позицию скролла после перезагрузки."""
        state = self._save_view_state() if keep_position else None
        self._model.select()
        self._fetch_all()
        self._update_count()
        if state is not None:
            self._restore_view_state(state)

    def _save_to_db(self):
        if self._model.submitAll():
            table_log('SAVE', sheet=self.sheet_name, success=True)
            self._do_select(keep_position=True)
            QMessageBox.information(self, 'Сохранение', f'Данные листа "{self.sheet_name}" сохранены в БД.')
        else:
            err = self._model.lastError().text()
            table_log('SAVE', sheet=self.sheet_name, success=False, error=err)
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить: {err}')

    def _add_10_rows(self):
        db = get_connection()
        if not db or not db.isOpen():
            QMessageBox.warning(self, 'Добавление', 'Нет подключения к БД.')
            return
        q = QSqlQuery(db)
        # Текущий максимум Num
        q.exec_(f'SELECT COALESCE(MAX({_quote_ident("Num")}), 0) FROM {_quote_ident(self._table_name)}')
        max_num = 0
        if q.next():
            max_num = int(q.value(0)) if q.value(0) is not None else 0
        self._model.submitAll()
        for i in range(10):
            max_num += 1
            rec = self._model.record()
            for c, col in enumerate(self._columns):
                if col == 'Num':
                    rec.setValue(c, max_num)
                elif col == 'Lesson':
                    rec.setValue(c, None)
                elif col == 'Sush' and self._has_sush:
                    rec.setValue(c, 'Сущ')
                else:
                    rec.setValue(c, '')
            if not self._model.insertRecord(self._model.rowCount(), rec):
                table_log('ADD_ROWS', sheet=self.sheet_name, error=self._model.lastError().text())
                break
        self._model.submitAll()
        self._do_select()
        table_log('ADD_ROWS', sheet=self.sheet_name, count=10)

    def _cell_value(self, row, col):
        idx = self._model.index(row, col)
        v = self._model.data(idx, Qt.DisplayRole)
        if v is not None:
            return str(v).strip()
        return ''

    def _search_next(self):
        if not hasattr(self, 'search_edit'):
            return
        pattern = self.search_edit.text().strip()
        if not pattern:
            return
        pattern_lower = pattern.lower()
        rows = self._model.rowCount()
        cols = self._model.columnCount()
        if pattern != self._search_text:
            self._search_text = pattern
            self._search_row = -1
            self._search_col = -1
        start_r = self._search_row if self._search_row >= 0 else -1
        start_c = self._search_col + 1 if self._search_col >= 0 else 0

        def iterate(sr, sc):
            for r in range(sr, rows):
                for c in range(sc if r == sr else 0, cols):
                    if pattern_lower in self._cell_value(r, c).lower():
                        return r, c
            return None

        pos = iterate(start_r, start_c) if start_r >= 0 else None
        if pos is None:
            pos = iterate(0, 0)
        if pos is None:
            table_log('SEARCH', sheet=self.sheet_name, pattern=pattern, found=None)
            self._clear_highlight()
            QMessageBox.information(self, 'Поиск', 'Ничего не найдено.')
            return
        r, c = pos
        table_log('SEARCH', sheet=self.sheet_name, pattern=pattern, found=(r, c))
        self._search_row, self._search_col = r, c
        self.table.setCurrentIndex(self._proxy.index(r, c))
        self.table.scrollTo(self._proxy.index(r, c))
        self._highlight_row(r)

    def _close_search(self):
        self.search_frame.setVisible(False)
        self._clear_highlight()

    def _clear_highlight(self):
        self._highlighted_row = -1
        if hasattr(self, '_proxy'):
            self._proxy.setHighlightedRow(-1)

    def _highlight_row(self, row):
        self._highlighted_row = row
        if hasattr(self, '_proxy'):
            self._proxy.setHighlightedRow(row)

    def eventFilter(self, obj, event):
        if obj is self.table and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
                table_log('SEARCH_OPEN', sheet=self.sheet_name)
                if hasattr(self, 'search_frame'):
                    self.search_frame.setVisible(True)
                    self.search_edit.setFocus()
                return True
            if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
                self._copy_selection()
                return True
            if event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
                self._paste_selection()
                return True
            if event.key() == Qt.Key_Delete:
                if event.modifiers() & Qt.ControlModifier:
                    self._delete_selected_rows()
                else:
                    self._clear_selection()
                return True
        return super().eventFilter(obj, event)

    def _copy_selection(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            return
        sel = self.table.selectedIndexes()
        if not sel:
            text = self._cell_value(idx.row(), idx.column())
            QApplication.clipboard().setText(text)
            return
        rows = sorted(set(i.row() for i in sel))
        cols = sorted(set(i.column() for i in sel))
        lines = []
        for r in rows:
            line = [self._cell_value(r, c) for c in cols]
            lines.append('\t'.join(line))
        QApplication.clipboard().setText('\n'.join(lines))

    def _clear_selection(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            return
        sel = self.table.selectedIndexes()
        if not sel:
            self._model.setData(idx, '', Qt.EditRole)
            return
        for i in sel:
            self._model.setData(i, '', Qt.EditRole)

    def _delete_selected_rows(self):
        sel = self.table.selectedIndexes()
        if not sel:
            idx = self.table.currentIndex()
            if idx.isValid():
                self._model.removeRow(idx.row())
        else:
            rows = sorted(set(i.row() for i in sel), reverse=True)
            for r in rows:
                self._model.removeRow(r)
        self._model.submitAll()
        self._do_select(keep_position=True)
        table_log('DELETE_ROWS', sheet=self.sheet_name)

    def _paste_selection(self):
        text = QApplication.clipboard().text()
        if not text:
            return
        lines = [line.split('\t') for line in text.replace('\r\n', '\n').split('\n') if line.strip()]
        if not lines:
            return
        idx = self.table.currentIndex()
        row0 = idx.row() if idx.isValid() else 0
        col0 = idx.column() if idx.isValid() else 0
        max_row = self._model.rowCount() - 1
        max_col = self._model.columnCount() - 1
        for r_off, line in enumerate(lines):
            r = row0 + r_off
            if r > max_row:
                break
            for c_off, value in enumerate(line):
                c = col0 + c_off
                if c > max_col:
                    break
                self._model.setData(self._model.index(r, c), value.strip(), Qt.EditRole)


class Table_window(QTabWidget):
    """Окно таблиц: вкладки по листам из SQLite."""

    def __init__(self):
        super().__init__()
        if not init_db():
            QMessageBox.critical(self, 'Ошибка', 'Не удалось открыть или инициализировать БД ' + DB_PATH)
            return
        self.sheet_names = get_sheet_names_for_display()
        self._tabs = {}
        for sheet_name in self.sheet_names:
            w = SheetTableWidget(sheet_name, self)
            self._tabs[sheet_name] = w
            self.addTab(w, sheet_name)
        japanese_logo_path = resource_path('japanese_logo.png')
        self.setWindowIcon(QIcon(japanese_logo_path))
        self.setWindowTitle('Tables')
        table_log('TABLE_OPEN', sheets=self.sheet_names)

    def closeEvent(self, event):
        for w in self._tabs.values():
            if hasattr(w, '_model'):
                w._model.submitAll()
        clear_table_log()
        event.accept()
