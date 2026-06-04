# -*- coding: utf-8 -*-
import os
import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


def get_unique_kanji_count(db_path):
    """
    Таблица Dictio, столбец Kanji.
    Берём все непустые и не нулевые значения, считаем уникальные.
    Возвращает (список уникальных кандзи, количество).
    """
    conn = sqlite3.connect(db_path)
    cur = conn.execute(
        'SELECT DISTINCT "Kanji" FROM Dictio '
        'WHERE "Kanji" IS NOT NULL AND TRIM("Kanji") != \'\' '
        'AND "Kanji" != 0 AND TRIM(CAST("Kanji" AS TEXT)) NOT IN (\'0\', \'0.0\')'
    )
    unique_kanji = [row[0] for row in cur.fetchall()]
    conn.close()
    return len(unique_kanji)


def get_all_kanji_chars_from_db(db_path):
    """Все уникальные символы кандзи, встречающиеся в Dictio.Kanji (каждый иероглиф отдельно)."""
    conn = sqlite3.connect(db_path)
    cur = conn.execute(
        'SELECT "Kanji" FROM Dictio '
        'WHERE "Kanji" IS NOT NULL AND TRIM("Kanji") != \'\' '
        'AND "Kanji" != 0 AND TRIM(CAST("Kanji" AS TEXT)) NOT IN (\'0\', \'0.0\')'
    )
    chars = set()
    for (cell,) in cur.fetchall():
        for ch in (cell or ''):
            if ch.strip():
                chars.add(ch)
    conn.close()
    return chars


def get_words_without_kanji_count(db_path):
    """
    Количество слов в таблице Kana (хирагана/катакана без кандзи).
    """
    conn = sqlite3.connect(db_path)
    try:
        count = conn.execute('SELECT COUNT(*) FROM Kana').fetchone()[0]
    except sqlite3.OperationalError:
        count = 0
    conn.close()
    return count


class StatsWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        db_path = os.path.join(os.path.dirname(__file__), 'Jp.db')
        count = get_unique_kanji_count(db_path)

        self.kanji_count_label = QLabel(f'Кандзи в БД (уникальных): {count}')
        layout.addWidget(self.kanji_count_label)

        words_without_kanji = get_words_without_kanji_count(db_path)
        self.words_no_kanji_label = QLabel(
            f'Слов в таблице Kana (хирагана/катакана): {words_without_kanji}'
        )
        layout.addWidget(self.words_no_kanji_label)

        self.setWindowTitle('Stats')
        self.resize(350, 180)