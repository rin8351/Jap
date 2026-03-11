# -*- coding: utf-8 -*-
import os
import csv
import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

# Путь к списку дзёё кандзи (2136 необходимых для жизни в Японии)
JYOUYOU_CSV = os.path.join(os.path.dirname(__file__), 'Jyouyou_kanji.csv')


def load_jyouyou_kanji(csv_path=JYOUYOU_CSV):
    """Загружает множество кандзи из Jyouyou_kanji.csv (столбец Kanji)."""
    jyouyou = set()
    with open(csv_path, 'r', encoding='utf-8') as f:
        next(f)  # пропуск пустой первой строки
        reader = csv.DictReader(f, skipinitialspace=True)
        for row in reader:
            kanji = (row.get('Kanji') or '').strip()
            if kanji:
                jyouyou.add(kanji)
    return jyouyou


def get_unique_kanji_count(db_path):
    """
    Таблица Dictio, столбец Kanji.
    Берём все непустые и не нулевые значения, считаем уникальные.
    Возвращает (список уникальных кандзи, количество).
    """
    conn = sqlite3.connect(db_path)
    cur = conn.execute(
        'SELECT DISTINCT "Kanji" FROM Dictio '
        'WHERE "Kanji" IS NOT NULL AND TRIM("Kanji") != \'\''
    )
    unique_kanji = [row[0] for row in cur.fetchall()]
    conn.close()
    return unique_kanji, len(unique_kanji)


def get_all_kanji_chars_from_db(db_path):
    """Все уникальные символы кандзи, встречающиеся в Dictio.Kanji (каждый иероглиф отдельно)."""
    conn = sqlite3.connect(db_path)
    cur = conn.execute(
        'SELECT "Kanji" FROM Dictio '
        'WHERE "Kanji" IS NOT NULL AND TRIM("Kanji") != \'\''
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
    Количество слов в Dictio, у которых в столбце Kanji стоит 0 или "0"
    (слова только на хирагане/катакане без кандзи).
    """
    conn = sqlite3.connect(db_path)
    cur = conn.execute(
        'SELECT COUNT(*) FROM Dictio '
        'WHERE "Kanji" = 0 OR TRIM(COALESCE(CAST("Kanji" AS TEXT), \'\')) = \'0\''
    )
    count = cur.fetchone()[0]
    conn.close()
    return count


def kanji_not_in_jyouyou(db_path, jyouyou_csv_path=JYOUYOU_CSV):
    """
    Кандзи из БД (каждый символ), которых нет в списке дзёё (Jyouyou_kanji.csv).
    Возвращает отсортированный список.
    """
    jyouyou = load_jyouyou_kanji(jyouyou_csv_path)
    db_chars = get_all_kanji_chars_from_db(db_path)
    missing = sorted(db_chars - jyouyou)
    return missing


class StatsWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        db_path = os.path.join(os.path.dirname(__file__), 'Jp.db')
        unique_kanji, count = get_unique_kanji_count(db_path)

        print('Уникальные кандзи в Dictio (состав):', unique_kanji)

        # Проверка: кандзи из БД, которых нет в списке дзёё (2136 необходимых)
        not_in_jyouyou = kanji_not_in_jyouyou(db_path)
        not_in_jyouyou = [x for x in not_in_jyouyou if x != '0']
        if not_in_jyouyou:
            print('Кандзи из БД, которых НЕТ в списке дзёё (Jyouyou):', not_in_jyouyou)
            print('Всего таких:', len(not_in_jyouyou))
        else:
            print('Все кандзи из БД есть в списке дзёё.')

        self.kanji_count_label = QLabel(f'Кандзи в БД (уникальных): {count}')
        layout.addWidget(self.kanji_count_label)

        words_without_kanji = get_words_without_kanji_count(db_path)
        self.words_no_kanji_label = QLabel(
            f'Слов без кандзи (только хирагана/катакана): {words_without_kanji}'
        )
        layout.addWidget(self.words_no_kanji_label)

        self.setWindowTitle('Stats')
        self.resize(350, 180)