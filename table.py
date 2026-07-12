# -*- coding: utf-8 -*-
"""
Tables window: data source is SQLite (Jp.db).
The widget uses QTableView + QSqlTableModel (virtualization: only visible rows in memory).
On first run, if the DB is empty, the default table structure is created.
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
import time
from others_scripts import resource_path
import styles as st
from table_logger import table_log, clear_table_log
from stats_script import SYNC_COLUMNS_BY_SOURCE, STATS_PREFIXES, ensure_all_stats_tables, stats_column_role

# Part-of-speech codes stored in the DB (Noun, Adjective, Verb, Adverb)
SUSH_OPTIONS = ['Сущ', 'Прил', 'Глаг', 'Нар']
DB_PATH = 'Jp.db'
COLUMN_FONT_SIZES = {'Kanji': 14, 'On': 12, 'Kun': 12, 'Read': 12}
# Tab order and list of tables to display (only these tables are shown)
TABLE_TAB_ORDER = ['Kanji', 'Words', 'Frazes', 'Name', 'Kana']


def _sanitize_table_name(name):
    """Normalizes an SQLite table name (no spaces or special characters)."""
    return re.sub(r'[^\w]', '_', str(name).strip()) or 'Table'


def _quote_ident(name):
    """Escapes a column name for SQL."""
    return '"' + str(name).replace('"', '""') + '"'


# --- Sync of dictionary fields into the stats tables (kanji_*, words_*, frazes_*, name_*, ...) ---

_SYNC_COLUMNS_BY_SOURCE = SYNC_COLUMNS_BY_SOURCE


def _get_stats_tables_for_column(db, column_in_name):
    """
    Returns a list of (table_name, 'value'|'answer') for the stats tables
    whose name contains column_in_name (trans, kanji, kun).
    If the table name is prefix_COLUMN_* the column maps to value, otherwise prefix_*_COLUMN to answer.
    """
    q = QSqlQuery(db)
    col_lower = column_in_name.lower()
    pattern = f'%{col_lower}%'
    prefix_conditions = ' OR '.join(
        f"(name LIKE '{prefix}_%' AND name LIKE '{pattern}')" for prefix in STATS_PREFIXES
    )
    sql = f"SELECT name FROM sqlite_master WHERE type='table' AND ({prefix_conditions})"
    if not q.exec_(sql):
        return []
    result = []
    while q.next():
        name = q.value(0)
        if name is None:
            continue
        result.append((name, stats_column_role(name, col_lower)))
    return result


def _create_sync_triggers_for_column(db, source_table, column_name, stats_list, q):
    """Creates one trigger: on UPDATE of column_name in source_table, updates stats_list by Num."""
    if not stats_list:
        return
    col_lower = column_name.lower()
    trigger_name = f'{source_table.lower()}_after_update_{col_lower}'
    q.exec_(f'DROP TRIGGER IF EXISTS {_quote_ident(trigger_name)}')
    updates = []
    for stat_table, stat_col in stats_list:
        qcol = _quote_ident(stat_col)
        qtable = _quote_ident(stat_table)
        updates.append(
            f'UPDATE {qtable} SET {qcol} = NEW.{_quote_ident(column_name)} WHERE num = CAST(NEW.Num AS TEXT)'
        )
    body = '; '.join(updates)
    sql = (
        f'CREATE TRIGGER {_quote_ident(trigger_name)} '
        f'AFTER UPDATE OF {_quote_ident(column_name)} ON {_quote_ident(source_table)} '
        f'FOR EACH ROW BEGIN {body}; END'
    )
    if not q.exec_(sql):
        table_log('SYNC_TRIGGER', error=f'{trigger_name}: {q.lastError().text()}')


def _ensure_stats_tables():
    """Creates and fills stats tables from the dictionaries (without overwriting existing progress)."""
    import sqlite3
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        ensure_all_stats_tables(conn)
    except Exception as e:
        table_log('STATS_POPULATE', error=str(e))
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


def _normalize_sush_columns(db):
    """Existing data: Sush=NULL/empty/not in the list -> 'Сущ' in all tables with the Sush column."""
    if not db or not db.isOpen():
        return
    q = QSqlQuery(db)
    allowed = ', '.join("'" + o.replace("'", "''") + "'" for o in SUSH_OPTIONS)
    for table_name in get_table_names():
        if 'Sush' not in get_table_columns(table_name):
            continue
        qtable = _quote_ident(table_name)
        qcol = _quote_ident('Sush')
        sql = f"UPDATE {qtable} SET {qcol} = 'Сущ' WHERE {qcol} IS NULL OR {qcol} NOT IN ({allowed})"
        if not q.exec_(sql):
            table_log('NORMALIZE_SUSH', error=f'{table_name}: {q.lastError().text()}')


def _create_sync_trans_triggers(db):
    """
    Creates triggers on the dictionary tables: on UPDATE of synced columns,
    value/answer in the stats tables are updated by Num.
    """
    if not db or not db.isOpen():
        return
    q = QSqlQuery(db)
    for source_table, columns in _SYNC_COLUMNS_BY_SOURCE.items():
        for column in columns:
            col_lower = column.lower()
            tables = _get_stats_tables_for_column(db, col_lower)
            prefix = source_table.lower() + '_'
            stats_list = [(t, c) for t, c in tables if str(t).lower().startswith(prefix)]
            _create_sync_triggers_for_column(db, source_table, column, stats_list, q)


# --- DB initialization ---

def get_connection():
    """Returns the SQLite connection (named connection 'tables')."""
    name = 'tables'
    if name not in QSqlDatabase.connectionNames():
        db = QSqlDatabase.addDatabase('QSQLITE', name)
        db.setDatabaseName(DB_PATH)
        if not db.open():
            return None
        # Wait up to 10 s on a lock when jap_wind_test (sqlite3) works concurrently
        q = QSqlQuery(db)
        q.exec_('PRAGMA busy_timeout=10000')
    db = QSqlDatabase.database(name)
    return db if db.isOpen() else None


# Empty DB schema: table name -> list of columns
_DEFAULT_SCHEMA = {
    'Kanji': ['Num', 'Lesson', 'Kanji', 'On', 'Kun', 'Trans', 'Sush', 'Mnem'],
    'Words': ['Num', 'Lesson', 'Kanji', 'On', 'Kun', 'Trans', 'Sush', 'Mnem'],
    'Frazes': ['Num', 'Lesson', 'Kanji', 'Read', 'Trans'],
    'Name': ['Num', 'Lesson', 'Kanji', 'Read'],
    'Kana': ['Num', 'Lesson', 'Kun', 'Trans', 'Sush', 'Mnem'],
}


def _create_empty_table(q, table_name, columns):
    """Creates a single empty table with the given columns."""
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
    Opens Jp.db. If the DB is empty (no tables), creates the table structure from _DEFAULT_SCHEMA (no rows).
    Returns True on success.
    """
    db = get_connection()
    if not db or not db.isOpen():
        return False
    q = QSqlQuery(db)
    # WAL: fewer locks when table.py and jap_wind_test work concurrently
    q.exec_('PRAGMA journal_mode=WAL')
    q.exec_("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    has_tables = q.next()
    if has_tables:
        _normalize_sush_columns(db)
        _ensure_stats_tables()
        _create_sync_trans_triggers(db)
        return True
    for table_name, columns in _DEFAULT_SCHEMA.items():
        if not _create_empty_table(q, table_name, columns):
            table_log('DB_INIT', error=f'CREATE TABLE {table_name}: {q.lastError().text()}')
    _normalize_sush_columns(db)
    _ensure_stats_tables()
    _create_sync_trans_triggers(db)
    return True


def get_table_names():
    """List of user table names in the DB (excluding sqlite_*)."""
    db = get_connection()
    if not db or not db.isOpen():
        return []
    q = QSqlQuery(db)
    q.exec_("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    names = []
    while q.next():
        names.append(q.value(0))
    return names


def get_table_names_for_display():
    """Table names in tab order. Only tables from TABLE_TAB_ORDER are shown."""
    names = get_table_names()
    return [n for n in TABLE_TAB_ORDER if n in names]


def get_table_columns(table_name):
    """List of column names of a table in the DB."""
    db = get_connection()
    if not db or not db.isOpen():
        return []
    q = QSqlQuery(db)
    q.exec_(f'PRAGMA table_info({_quote_ident(table_name)})')
    cols = []
    while q.next():
        cols.append(q.value(1))
    return cols


# --- Cell delegates ---

class SushDelegate(QStyledItemDelegate):
    """Sush column: choose from the part-of-speech list."""
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
    """Lesson: display an integer without the .0 suffix."""
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
    """Delegate: sets the font size for a column based on COLUMN_FONT_SIZES."""
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
    """Proxy model: highlights the search row with a blue background (BackgroundRole)."""
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
            return QBrush(QColor(173, 216, 230))  # light blue
        return super().data(index, role)


# --- Table tab widget (SQLite + virtualization) ---

class SheetTableWidget(QWidget):
    """One tab: QTableView + QSqlTableModel, filters (SQL WHERE), search, adding rows, saving to the DB."""

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

        # Filters
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
                from_spin.setSpecialValueText('from')
                to_spin = QSpinBox()
                to_spin.setRange(-999999, 999999)
                to_spin.setSpecialValueText('to')
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
                combo.addItem('(all)', None)
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
                combo.addItem('(all)', None)
                combo.addItem('Empty', 'empty')
                combo.addItem('Not empty', 'not_empty')
                combo.addItem('0', 'zero')
                combo.addItem('Not 0', 'not_zero')
                combo.setCurrentIndex(0)
                col_layout.addWidget(combo)
                self._filter_widgets[col] = ('empty_not', combo)
            filter_layout.addWidget(col_frame)
        filter_layout.addStretch()
        layout.addWidget(filter_frame)

        # Model and view
        self._model = QSqlTableModel(self, get_connection())
        self._model.setTable(self._table_name)
        self._model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self._model.select()
        self._model.dataChanged.connect(self._on_model_data_changed)
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
        # Delegates (including font size from COLUMN_FONT_SIZES)
        for c in range(self._model.columnCount()):
            col_name = self._columns[c] if c < len(self._columns) else ''
            if col_name == 'Sush':
                self.table.setItemDelegateForColumn(c, SushDelegate(self.table))
            elif col_name == 'Lesson':
                self.table.setItemDelegateForColumn(c, LessonDelegate(self.table))
            elif col_name in COLUMN_FONT_SIZES:
                self.table.setItemDelegateForColumn(c, ColumnFontDelegate(col_name, self.table))
        # Do not show the Num column
        if 'Num' in self._columns:
            self.table.setColumnHidden(self._columns.index('Num'), True)
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        layout.addWidget(self.table)

        # Search
        self.search_frame = QFrame()
        search_layout = QHBoxLayout(self.search_frame)
        search_layout.addWidget(QLabel("Search:"))
        self.search_edit = QLineEdit()
        search_layout.addWidget(self.search_edit)
        self.search_next_btn = QPushButton("Find next")
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

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton('Save')
        self.btn_save.setStyleSheet(st.btn_test)
        self.btn_save.clicked.connect(self._save_to_db)
        self.btn_add = QPushButton('Add 10 rows')
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
        """Builds the WHERE clause from the filter widgets."""
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
        self._submit_all_with_validation(show_message=False)
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
        self._submit_all_with_validation(show_message=False)
        self._model.setSort(logical_index, order)
        self._do_select()
        table_log('SORT', sheet=self.sheet_name, column=col, ascending=self._sort_ascending)

    def _update_count(self):
        if hasattr(self, 'rows_count_label') and self.rows_count_label is not None:
            self.rows_count_label.setText(f'Rows: {self._model.rowCount()}')

    def _fetch_all(self):
        """Loads all rows from the DB (disables lazy fetching while scrolling)."""
        while self._model.canFetchMore():
            self._model.fetchMore()

    def _save_view_state(self):
        """Remembers the scroll position and the current cell."""
        idx = self.table.currentIndex()
        return (
            self.table.verticalScrollBar().value(),
            self.table.horizontalScrollBar().value(),
            idx.row(),
            idx.column(),
        )

    def _restore_view_state(self, state):
        """Restores the scroll position and the current cell."""
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
        """select() + load all rows + update the counter.
        keep_position=True preserves the scroll position after a reload."""
        state = self._save_view_state() if keep_position else None
        self._model.select()
        self._fetch_all()
        self._update_count()
        if state is not None:
            self._restore_view_state(state)

    @staticmethod
    def _is_empty_value(value):
        if value is None:
            return True
        return str(value).strip() == ''

    def _row_has_meaningful_data(self, row):
        """Whether the row has content (besides Num/Lesson; Sush='Сущ' is treated as the default)."""
        for col_idx, col_name in enumerate(self._columns):
            if col_name in ('Num', 'Lesson'):
                continue
            idx = self._model.index(row, col_idx)
            value = self._model.data(idx, Qt.EditRole)
            text = '' if value is None else str(value).strip()
            if col_name == 'Sush' and text == 'Сущ':
                continue
            if text != '':
                return True
        return False

    def _validate_required_lesson(self, show_message=True):
        """
        Validation: if a row has data, Lesson is required.
        Returns (ok: bool, invalid_rows: list[(model_row, row_num)]).
        """
        if 'Lesson' not in self._columns:
            return True, []
        lesson_idx = self._columns.index('Lesson')
        num_idx = self._columns.index('Num') if 'Num' in self._columns else -1
        invalid_rows = []
        for row in range(self._model.rowCount()):
            if not self._row_has_meaningful_data(row):
                continue
            lesson_value = self._model.data(self._model.index(row, lesson_idx), Qt.EditRole)
            if self._is_empty_value(lesson_value):
                row_num = None
                if num_idx >= 0:
                    row_num = self._model.data(self._model.index(row, num_idx), Qt.DisplayRole)
                invalid_rows.append((row, row_num))
        if invalid_rows and show_message:
            shown = [str(rn) for _, rn in invalid_rows[:5] if rn not in (None, '')]
            if shown:
                details = ', '.join(shown)
                suffix = ' ...' if len(invalid_rows) > 5 else ''
                msg = f'Fill in Lesson for rows Num: {details}{suffix}'
            else:
                details = ', '.join(str(r + 1) for r, _ in invalid_rows[:5])
                suffix = ' ...' if len(invalid_rows) > 5 else ''
                msg = f'Fill in Lesson for rows: {details}{suffix}'
            QMessageBox.warning(self, 'Data validation', msg)
        return len(invalid_rows) == 0, invalid_rows

    def _sush_col_index(self):
        """Index of the Sush column in the model or -1 if it doesn't exist."""
        if not self._has_sush or 'Sush' not in self._columns:
            return -1
        return self._columns.index('Sush')

    def _normalize_sush_in_model(self):
        """Replaces empty/NULL/invalid value in the Sush column with 'Сущ' in all rows of the model."""
        sush_idx = self._sush_col_index()
        if sush_idx < 0:
            return
        for row in range(self._model.rowCount()):
            idx = self._model.index(row, sush_idx)
            value = self._model.data(idx, Qt.EditRole)
            text = '' if value is None else str(value).strip()
            if text not in SUSH_OPTIONS:
                self._model.setData(idx, 'Сущ', Qt.EditRole)

    @staticmethod
    def _is_locked_error(err):
        """Does the error message look like a temporary database lock?"""
        e = (err or '').lower()
        return 'locked' in e or 'is busy' in e or 'database is busy' in e


    def _submit_all_with_validation(self, show_message=True):
        """submitAll() with the required-Lesson check and retry on temporary database lock."""
        self._normalize_sush_in_model()
        """submitAll() with the required-Lesson check."""
        ok, invalid_rows = self._validate_required_lesson(show_message=show_message)
        if not ok:
            table_log('VALIDATE_LESSON', sheet=self.sheet_name, success=False, invalid_rows=invalid_rows)
            return False

        max_attempts = 5
        err = ''
        for attempt in range(max_attempts):
            if self._model.submitAll():
                return True
            err = self._model.lastError().text()
            if self._is_locked_error(err) and attempt < max_attempts - 1:
                QApplication.processEvents()
                time.sleep(0.4)
                continue
            break

        table_log('SAVE', sheet=self.sheet_name, success=False, error=err)
        if self._is_locked_error(err):
            QMessageBox.warning(
                self, 'Database is busy',
                'The database is currently busy with another window (e.g., a test).\n'
                'Your changes are not lost — close the other window and click "Save" again.'
            )
        else:
            QMessageBox.critical(self, 'Error', f'Failed to save: {err}')
        return False

    def _save_to_db(self):
        if self._submit_all_with_validation(show_message=True):
            table_log('SAVE', sheet=self.sheet_name, success=True)
            self._do_select(keep_position=True)
            QMessageBox.information(self, 'Save', f'Table "{self.sheet_name}" data saved to the DB.')

    def _get_numeric_max_num(self):
        """Returns the maximum valid Num (only non-negative integers)."""
        db = get_connection()
        if not db or not db.isOpen():
            return 0
        q = QSqlQuery(db)
        num_col = _quote_ident('Num')
        table = _quote_ident(self._table_name)
        num_text = f'TRIM(CAST({num_col} AS TEXT))'
        sql = (
            f'SELECT COALESCE(MAX(CASE WHEN {num_text} <> \'\' '
            f'AND {num_text} NOT GLOB \'*[^0-9]*\' '
            f'THEN CAST({num_col} AS INTEGER) END), 0) '
            f'FROM {table}'
        )
        if not q.exec_(sql):
            table_log('ADD_ROWS', sheet=self.sheet_name, error=f'MAX Num query failed: {q.lastError().text()}')
            return 0
        if not q.next():
            return 0
        try:
            return int(q.value(0) or 0)
        except (TypeError, ValueError):
            return 0

    def _on_model_data_changed(self, top_left, bottom_right, roles=None):
        """Logs cell edits in the model (including before Save is pressed)."""
        if roles and Qt.EditRole not in roles and Qt.DisplayRole not in roles:
            return
        num_col_idx = self._columns.index('Num') if 'Num' in self._columns else -1
        for row in range(top_left.row(), bottom_right.row() + 1):
            for col in range(top_left.column(), bottom_right.column() + 1):
                if col < 0 or col >= len(self._columns):
                    continue
                col_name = self._columns[col]
                idx = self._model.index(row, col)
                value = self._model.data(idx, Qt.EditRole)
                row_num = None
                if num_col_idx >= 0:
                    nidx = self._model.index(row, num_col_idx)
                    row_num = self._model.data(nidx, Qt.DisplayRole)
                table_log(
                    'CELL_EDIT',
                    sheet=self.sheet_name,
                    row=row,
                    row_num=row_num,
                    column=col_name,
                    value=value
                )

    def _add_10_rows(self):
        db = get_connection()
        if not db or not db.isOpen():
            QMessageBox.warning(self, 'Add rows', 'No DB connection.')
            return
        max_num = self._get_numeric_max_num()
        if not self._submit_all_with_validation(show_message=False):
            QMessageBox.warning(self, 'Add rows', 'First fill in the required Lesson in the already edited rows.')
            return
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
        self._submit_all_with_validation(show_message=False)
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
            QMessageBox.information(self, 'Search', 'Nothing found.')
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

    def _clear_value_for_column(self, col):
        """Value when clearing a cell: for Sush — 'Сущ', otherwise empty string."""
        sush_idx = self._sush_col_index()
        return 'Сущ' if (sush_idx >= 0 and col == sush_idx) else ''


    def _clear_selection(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            return
        sel = self.table.selectedIndexes()
        if not sel:
            self._model.setData(idx, self._clear_value_for_column(idx.column()), Qt.EditRole)
            return
        for i in sel:
            self._model.setData(i, self._clear_value_for_column(i.column()), Qt.EditRole)

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
        self._submit_all_with_validation(show_message=False)
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
        sush_idx = self._sush_col_index()
        for r_off, line in enumerate(lines):
            r = row0 + r_off
            if r > max_row:
                break
            for c_off, value in enumerate(line):
                c = col0 + c_off
                if c > max_col:
                    break
                text = value.strip()
                if c == sush_idx and text not in SUSH_OPTIONS:
                    text = 'Сущ'
                self._model.setData(self._model.index(r, c), text, Qt.EditRole)


class Table_window(QTabWidget):
    """Tables window: one tab per SQLite table."""

    def __init__(self):
        super().__init__()
        clear_table_log()
        if not init_db():
            QMessageBox.critical(self, 'Error', 'Failed to open or initialize the DB ' + DB_PATH)
            return
        self.sheet_names = get_table_names_for_display()
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
            if hasattr(w, '_submit_all_with_validation'):
                w._submit_all_with_validation(show_message=False)
            elif hasattr(w, '_model'):
                w._model.submitAll()
        event.accept()
