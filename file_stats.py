# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget,
    QComboBox, QTableWidget, QTableWidgetItem, QSpinBox, QHeaderView,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt

import styles
from stats_script import STATS_SOURCES
from stats_reports import (
    get_db_path,
    open_db,
    overview_all_sources,
    lesson_breakdown,
    sush_breakdown,
    direction_breakdown,
    word_rankings,
    stuck_words,
    srs_due_words,
    direction_asymmetry,
    format_pct,
    get_unique_kanji_count,
    get_words_without_kanji_count,
    MIN_ATTEMPTS_DEFAULT,
    SOURCES_WITH_SUSH,
)

SOURCE_LIST = list(STATS_SOURCES.keys())

WORD_TABLE_HEADERS = [
    'Lesson', 'Word', 'Eff.', 'Attempts', 'Right', 'Wrong', 'Hard',
]

WORDS_TAB_HEADERS = [
    'Lesson', 'Word', 'Eff.', 'Attempts', 'Right', 'Wrong', 'Hard',
]

_READ_ONLY_FLAGS = Qt.ItemIsSelectable | Qt.ItemIsEnabled


def _configure_report_table(table):
    """View-only: cell edits are not saved to the DB."""
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setSelectionMode(QAbstractItemView.SingleSelection)


def _fill_table(table, headers, rows, formatters=None):
    formatters = formatters or {}
    # The table must not be filled while sorting is enabled: Qt reorders
    # rows during setItem, which leaves some cells empty.
    sorting_was_enabled = table.isSortingEnabled()
    table.setSortingEnabled(False)
    table.clear()
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.setRowCount(len(rows))
    for r_idx, row in enumerate(rows):
        for c_idx, key in enumerate(headers):
            raw = row.get(key, '')
            fmt = formatters.get(key)
            text = fmt(raw, row) if fmt else ('' if raw is None else str(raw))
            item = QTableWidgetItem(text)
            item.setFlags(_READ_ONLY_FLAGS)
            sort_val = row.get(f'_{key}_sort')
            if sort_val is not None:
                item.setData(Qt.UserRole, sort_val)
            table.setItem(r_idx, c_idx, item)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    table.horizontalHeader().setStretchLastSection(True)
    table.setSortingEnabled(sorting_was_enabled)


class StatsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db_path = get_db_path()
        self.setWindowTitle('Reports')
        self.setStyleSheet(styles.main_style + styles.tab_widget_style + styles.table)
        self.resize(1050, 720)

        layout = QVBoxLayout(self)
        kanji_count = get_unique_kanji_count(self.db_path)
        kana_count = get_words_without_kanji_count(self.db_path)
        header = QLabel(
            f'Unique kanji in Kanji table: {kanji_count}   |   '
            f'Records in Kana: {kana_count}'
        )
        layout.addWidget(header)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self._build_overview_tab()
        self._build_slices_tab()
        self._build_words_tab()
        self._build_srs_tab()
        self._build_stuck_tab()
        self._build_directions_tab()

        self.refresh_all()

    def _source_combo(self, with_all=False):
        combo = QComboBox()
        if with_all:
            combo.addItem('All tables', None)
        for name in SOURCE_LIST:
            combo.addItem(name, name)
        combo.setStyleSheet(styles.combobox)
        return combo

    def _build_overview_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        self.overview_table = QTableWidget()
        _configure_report_table(self.overview_table)
        self.overview_table.setSortingEnabled(True)
        lay.addWidget(self.overview_table)
        self.tabs.addTab(w, 'Overview')

    def _build_slices_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        bar = QHBoxLayout()
        self.slice_source = self._source_combo()
        self.slice_source.setCurrentText('Kanji')
        self.slice_type = QComboBox()
        self.slice_type.addItem('By lesson', 'lesson')
        self.slice_type.addItem('By part of speech', 'sush')
        self.slice_type.addItem('By direction', 'direction')
        self.slice_type.setStyleSheet(styles.combobox)
        bar.addWidget(QLabel('Table:'))
        bar.addWidget(self.slice_source)
        bar.addWidget(QLabel('Breakdown:'))
        bar.addWidget(self.slice_type)
        bar.addStretch()
        lay.addLayout(bar)
        self.slice_table = QTableWidget()
        _configure_report_table(self.slice_table)
        self.slice_table.setSortingEnabled(True)
        lay.addWidget(self.slice_table)
        self.slice_source.currentIndexChanged.connect(self._on_slice_source_changed)
        self.slice_type.currentIndexChanged.connect(self.refresh_slices)
        self.slice_source.currentIndexChanged.connect(self.refresh_slices)
        self.tabs.addTab(w, 'Breakdowns')

    def _build_words_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        bar = QHBoxLayout()
        self.words_source = self._source_combo()
        self.words_source.setCurrentText('Kanji')
        self.words_sort = QComboBox()
        self.words_sort.addItem('Hardest', True)
        self.words_sort.addItem('Easiest', False)
        self.words_sort.setStyleSheet(styles.combobox)
        self.words_min_attempts = QSpinBox()
        self.words_min_attempts.setRange(1, 100)
        self.words_min_attempts.setValue(MIN_ATTEMPTS_DEFAULT)
        bar.addWidget(QLabel('Table:'))
        bar.addWidget(self.words_source)
        bar.addWidget(QLabel('Sort:'))
        bar.addWidget(self.words_sort)
        bar.addWidget(QLabel('Min attempts:'))
        bar.addWidget(self.words_min_attempts)
        bar.addStretch()
        lay.addLayout(bar)
        self.words_table = QTableWidget()
        _configure_report_table(self.words_table)
        self.words_table.setSortingEnabled(True)
        lay.addWidget(self.words_table)
        for ctrl in (self.words_source, self.words_sort):
            ctrl.currentIndexChanged.connect(self.refresh_words)
        self.words_min_attempts.valueChanged.connect(self.refresh_words)
        self.tabs.addTab(w, 'Words')

    def _build_srs_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        bar = QHBoxLayout()
        self.srs_source = self._source_combo()
        self.srs_source.setCurrentText('Kanji')
        bar.addWidget(QLabel('Table:'))
        bar.addWidget(self.srs_source)
        bar.addStretch()
        lay.addLayout(bar)
        self.srs_summary = QLabel()
        lay.addWidget(self.srs_summary)
        self.srs_table = QTableWidget()
        _configure_report_table(self.srs_table)
        self.srs_table.setSortingEnabled(True)
        lay.addWidget(self.srs_table)
        self.srs_source.currentIndexChanged.connect(self.refresh_srs)
        self.tabs.addTab(w, 'SRS queue')

    def _build_stuck_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        bar = QHBoxLayout()
        self.stuck_source = self._source_combo()
        self.stuck_source.setCurrentText('Kanji')
        bar.addWidget(QLabel('Table:'))
        bar.addWidget(self.stuck_source)
        bar.addStretch()
        lay.addLayout(bar)
        self.stuck_table = QTableWidget()
        _configure_report_table(self.stuck_table)
        self.stuck_table.setSortingEnabled(True)
        lay.addWidget(self.stuck_table)
        self.stuck_source.currentIndexChanged.connect(self.refresh_stuck)
        self.tabs.addTab(w, 'Stuck')

    def _build_directions_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        bar = QHBoxLayout()
        self.asym_source = self._source_combo()
        self.asym_source.setCurrentText('Kanji')
        self.asym_min_attempts = QSpinBox()
        self.asym_min_attempts.setRange(1, 100)
        self.asym_min_attempts.setValue(MIN_ATTEMPTS_DEFAULT)
        bar.addWidget(QLabel('Table:'))
        bar.addWidget(self.asym_source)
        bar.addWidget(QLabel('Min attempts per direction:'))
        bar.addWidget(self.asym_min_attempts)
        bar.addStretch()
        lay.addLayout(bar)
        self.asym_table = QTableWidget()
        _configure_report_table(self.asym_table)
        self.asym_table.setSortingEnabled(True)
        lay.addWidget(self.asym_table)
        self.asym_source.currentIndexChanged.connect(self.refresh_asymmetry)
        self.asym_min_attempts.valueChanged.connect(self.refresh_asymmetry)
        self.tabs.addTab(w, 'Directions')

    def _on_slice_source_changed(self):
        source = self.slice_source.currentData()
        is_sush = source in SOURCES_WITH_SUSH
        idx = self.slice_type.findData('sush')
        if idx >= 0:
            item = self.slice_type.model().item(idx)
            item.setEnabled(is_sush)
        if not is_sush and self.slice_type.currentData() == 'sush':
            self.slice_type.setCurrentIndex(self.slice_type.findData('lesson'))

    def _current_source(self, combo):
        return combo.currentData()

    def refresh_all(self):
        self.refresh_overview()
        self._on_slice_source_changed()
        self.refresh_slices()
        self.refresh_words()
        self.refresh_srs()
        self.refresh_stuck()
        self.refresh_asymmetry()

    def refresh_overview(self):
        conn = open_db(self.db_path)
        try:
            data = overview_all_sources(conn)
        finally:
            conn.close()
        rows = []
        for d in data:
            rows.append({
                'Table': d['source'],
                'Total': d['total'],
                'Tested': d['tested'],
                'Untested': d['never'],
                'Due today': d['due'],
                'Hard': d['hard'],
                'Orphans': d['orphaned'],
                'Tested %': f"{d['pct_tested']:.1f}%",
                'Avg eff.': format_pct(d['avg_efficiency']),
                '_Total_sort': d['total'],
                '_Due today_sort': d['due'],
            })
        _fill_table(
            self.overview_table,
            ['Table', 'Total', 'Tested', 'Untested', 'Due today', 'Hard', 'Orphans', 'Tested %', 'Avg eff.'],
            rows,
        )

    def refresh_slices(self):
        source = self._current_source(self.slice_source)
        if not source:
            return
        slice_type = self.slice_type.currentData()
        conn = open_db(self.db_path)
        try:
            if slice_type == 'lesson':
                data = lesson_breakdown(conn, source)
                rows = [{
                    'Lesson': x['lesson'],
                    'Words': x['total'],
                    'Tested %': f"{x['tested_pct']:.1f}%",
                    'Due': x['due'],
                    'Hard': x['hard'],
                    'Avg eff.': format_pct(x['avg_efficiency']),
                    'Days since': x['days_since'] if x['days_since'] is not None else '—',
                    'Attempts': x['attempts'],
                    '_Words_sort': x['total'],
                    '_Days since_sort': x['days_since'] if x['days_since'] is not None else 99999,
                } for x in data]
                headers = ['Lesson', 'Words', 'Tested %', 'Due', 'Hard', 'Avg eff.', 'Days since', 'Attempts']
            elif slice_type == 'sush':
                data = sush_breakdown(conn, source)
                rows = [{
                    'Part of speech': x['sush'],
                    'Words': x['total'],
                    'Tested %': f"{x['tested_pct']:.1f}%",
                    'Due': x['due'],
                    'Hard': x['hard'],
                    'Avg eff.': format_pct(x['avg_efficiency']),
                    'Attempts': x['attempts'],
                    '_Words_sort': x['total'],
                } for x in data]
                headers = ['Part of speech', 'Words', 'Tested %', 'Due', 'Hard', 'Avg eff.', 'Attempts']
            else:
                data = direction_breakdown(conn, source)
                rows = [{
                    'Direction': x['direction'],
                    'Records': x['total'],
                    'Due': x['due'],
                    'Hard': x['hard'],
                    'Avg eff.': format_pct(x['avg_efficiency']),
                    'Attempts': x['attempts'],
                    '_Records_sort': x['total'],
                    '_Avg eff._sort': x['avg_efficiency'] if x['avg_efficiency'] is not None else -1,
                } for x in data]
                headers = ['Direction', 'Records', 'Due', 'Hard', 'Avg eff.', 'Attempts']
        finally:
            conn.close()
        _fill_table(self.slice_table, headers, rows)

    def _word_rows(self, items):
        rows = []
        for x in items:
            lesson = x.get('lesson')
            rows.append({
                'Lesson': lesson if lesson is not None else '—',
                'Word': x['label'],
                'Eff.': format_pct(x['efficiency']),
                'Attempts': x['attempts'],
                'Right': x['total_right'],
                'Wrong': x['total_wrong'],
                'Hard': 'yes' if x['hard'] else '',
                'Due': 'yes' if x['due'] else '',
                '_Eff._sort': x['efficiency'] if x['efficiency'] is not None else -1,
                '_Attempts_sort': x['attempts'],
            })
        return rows

    def refresh_words(self):
        source = self._current_source(self.words_source)
        hardest = self.words_sort.currentData()
        min_att = self.words_min_attempts.value()
        conn = open_db(self.db_path)
        try:
            data = word_rankings(conn, source, min_attempts=min_att, hardest=hardest)
        finally:
            conn.close()
        rows = self._word_rows(data)
        _fill_table(self.words_table, WORDS_TAB_HEADERS, rows)

    def refresh_srs(self):
        source = self._current_source(self.srs_source)
        conn = open_db(self.db_path)
        try:
            data = srs_due_words(conn, source)
            overview = overview_all_sources(conn)
            row = next((x for x in overview if x['source'] == source), None)
        finally:
            conn.close()
        total_due = len(data)
        if row:
            self.srs_summary.setText(
                f'Due today: {total_due} words (of {row["total"]}, '
                f'untested: {row["never"]}, hard: {row["hard"]})'
            )
        else:
            self.srs_summary.setText(f'Due today: {total_due} words')
        rows = self._word_rows(data)
        _fill_table(self.srs_table, WORD_TABLE_HEADERS, rows)

    def refresh_stuck(self):
        source = self._current_source(self.stuck_source)
        conn = open_db(self.db_path)
        try:
            data = stuck_words(conn, source)
        finally:
            conn.close()
        rows = []
        for x in data:
            rows.append({
                'Lesson': x.get('lesson') if x.get('lesson') is not None else '—',
                'Word': x['label'],
                'Reason': x['reasons'],
                'Eff.': format_pct(x['efficiency']),
                'Total wrong': x['total_wrong'],
                'Session wrong': int(x['directions'] and max(
                    (int(s.get('wrong', 0) or 0) for s in x['directions'].values()), default=0
                )),
                '_Total wrong_sort': x['total_wrong'],
            })
        _fill_table(
            self.stuck_table,
            ['Lesson', 'Word', 'Reason', 'Eff.', 'Total wrong', 'Session wrong'],
            rows,
        )

    def refresh_asymmetry(self):
        source = self._current_source(self.asym_source)
        min_att = self.asym_min_attempts.value()
        conn = open_db(self.db_path)
        try:
            data = direction_asymmetry(conn, source, min_attempts=min_att)
        finally:
            conn.close()
        rows = []
        for x in data:
            rows.append({
                'Lesson': x.get('lesson') if x.get('lesson') is not None else '—',
                'Word': x['label'],
                'Spread': format_pct(x['spread']),
                'Weaker': f"{x['worst_dir']} ({format_pct(x['worst_eff'])})",
                'Better': f"{x['best_dir']} ({format_pct(x['best_eff'])})",
                'All directions': x['dir_detail'],
                '_Spread_sort': x['spread'],
            })
        _fill_table(
            self.asym_table,
            ['Lesson', 'Word', 'Spread', 'Weaker', 'Better', 'All directions'],
            rows,
        )
