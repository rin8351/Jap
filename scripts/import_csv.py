# -*- coding: utf-8 -*-
"""Append rows from a CSV file into Jp.db without deleting existing data."""
import argparse
import csv
import os
import sqlite3
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.stats_script import ensure_all_stats_tables

DB_NAME = 'Jp.db'

SUSH_OPTIONS = ('Noun', 'Adjective', 'Verb', 'Adverb')
INTEGER_COLUMNS = {'Num', 'Lesson'}
ENCODINGS = ('utf-8-sig', 'utf-8', 'cp1251')

# Dictionary tables: column order for CREATE TABLE, plus how to detect duplicates.
DICT_TABLES = {
    'Kanji': {
        'columns': ['Num', 'Lesson', 'Kanji', 'On', 'Kun', 'Trans', 'Sush', 'Mnem'],
        'identity': ('Kanji', 'On', 'Kun', 'Trans'),
        'required': ('Kanji',),
    },
    'Words': {
        'columns': ['Num', 'Lesson', 'Kanji', 'Read', 'Trans', 'Mnem'],
        'identity': ('Kanji', 'Read', 'Trans'),
        'required': ('Kanji',),
    },
    'Frazes': {
        'columns': ['Num', 'Lesson', 'Kanji', 'Read', 'Trans'],
        'identity': ('Kanji', 'Read', 'Trans'),
        'required': ('Kanji',),
    },
    'Kana': {
        'columns': ['Num', 'Lesson', 'Kun', 'Trans', 'Sush', 'Mnem'],
        'identity': ('Kun', 'Trans'),
        'required': ('Kun',),
    },
    'Name': {
        'columns': ['Num', 'Lesson', 'Kanji', 'Read'],
        'identity': ('Kanji', 'Read'),
        'required': ('Kanji',),
    },
}


def _quote_ident(name):
    return '"' + str(name).replace('"', '""') + '"'


def _detect_encoding(path):
    last_error = None
    for enc in ENCODINGS:
        try:
            with open(path, 'r', encoding=enc, newline='') as f:
                f.read()
            return enc
        except UnicodeDecodeError as e:
            last_error = e
    raise SystemExit(f'Could not decode {path} (tried {", ".join(ENCODINGS)}): {last_error}')


def _read_csv_rows(path):
    encoding = _detect_encoding(path)
    with open(path, 'r', encoding=encoding, newline='') as f:
        sample = f.read(8192)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(f, dialect=dialect)
        if not reader.fieldnames:
            raise SystemExit(f'{path} has no header row.')
        headers = [(h or '').strip() for h in reader.fieldnames]
        if any(not h for h in headers):
            raise SystemExit(f'{path}: empty column name in the header row.')
        rows = []
        for raw in reader:
            row = {}
            for key, value in raw.items():
                if key is None:
                    continue
                name = key.strip()
                if not name:
                    continue
                text = '' if value is None else str(value).strip()
                row[name] = text
            rows.append(row)
    return headers, rows, encoding


def _map_headers(csv_headers, db_columns):
    db_by_lower = {c.lower(): c for c in db_columns}
    mapping = {}
    ignored = []
    for header in csv_headers:
        match = db_by_lower.get(header.lower())
        if match:
            mapping[header] = match
        else:
            ignored.append(header)
    return mapping, ignored


def _table_exists(conn, table_name):
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    ).fetchone()
    return row is not None


def _ensure_dict_table(conn, table_name):
    if _table_exists(conn, table_name):
        return
    spec = DICT_TABLES[table_name]
    parts = []
    for col in spec['columns']:
        quoted = _quote_ident(col)
        if col in INTEGER_COLUMNS:
            parts.append(f'{quoted} INTEGER')
        elif col == 'Sush':
            parts.append(
                f"{quoted} TEXT CHECK({quoted} IN ('Noun', 'Adjective', 'Verb', 'Adverb'))"
            )
        else:
            parts.append(f'{quoted} TEXT')
    conn.execute(
        f'CREATE TABLE {_quote_ident(table_name)} ({", ".join(parts)})'
    )


def _db_columns(conn, table_name):
    return [r[1] for r in conn.execute(f'PRAGMA table_info({_quote_ident(table_name)})')]


def _to_int(value, column, row_no):
    if value is None or value == '':
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        raise SystemExit(f'Row {row_no}: column {column} must be a number, got {value!r}')


def _normalize_sush(value, row_no):
    if value is None or value == '':
        return 'Noun'
    if value in SUSH_OPTIONS:
        return value
    print(f'  warning: row {row_no}: Sush={value!r} is not one of {SUSH_OPTIONS}; using Noun')
    return 'Noun'


def _next_num(conn, table_name):
    max_num = conn.execute(
        f'SELECT MAX(Num) FROM {_quote_ident(table_name)}'
    ).fetchone()[0]
    return (max_num or 0) + 1


def _existing_nums(conn, table_name):
    return {
        row[0]
        for row in conn.execute(f'SELECT Num FROM {_quote_ident(table_name)}')
        if row[0] is not None
    }


def _identity_key(values, identity_cols):
    return tuple(values.get(col) or '' for col in identity_cols)


def _load_identity_keys(conn, table_name, identity_cols, db_columns):
    usable = [col for col in identity_cols if col in db_columns]
    if not usable:
        return set(), usable
    cols_sql = ', '.join(f"COALESCE({_quote_ident(col)}, '')" for col in usable)
    rows = conn.execute(f'SELECT {cols_sql} FROM {_quote_ident(table_name)}')
    return {tuple(row) for row in rows}, usable


def _prepare_row(raw, mapping, db_columns, spec, row_no):
    mapped = {}
    for csv_name, db_name in mapping.items():
        mapped[db_name] = raw.get(csv_name, '')

    for col in spec['required']:
        if col in db_columns and not mapped.get(col):
            return None, f'missing required column {col}'

    out = {}
    for col in db_columns:
        value = mapped.get(col, '')
        if col == 'Num':
            out[col] = _to_int(value, col, row_no)
        elif col == 'Lesson':
            number = _to_int(value, col, row_no)
            out[col] = 1 if number is None else number
        elif col == 'Sush':
            out[col] = _normalize_sush(value, row_no)
        else:
            out[col] = value
    return out, None


def import_csv(csv_path, table_name, db_path=None):
    if table_name not in DICT_TABLES:
        raise SystemExit(
            f'Unknown table {table_name!r}. Choose one of: {", ".join(DICT_TABLES)}'
        )
    if not os.path.isfile(csv_path):
        raise SystemExit(f'CSV file not found: {csv_path}')

    spec = DICT_TABLES[table_name]
    headers, rows, encoding = _read_csv_rows(csv_path)
    db_path = db_path or os.path.join(_ROOT, DB_NAME)

    conn = sqlite3.connect(db_path, timeout=10)
    try:
        _ensure_dict_table(conn, table_name)
        db_columns = _db_columns(conn, table_name)
        mapping, ignored = _map_headers(headers, db_columns)
        if not mapping:
            expected = ', '.join(spec['columns'])
            raise SystemExit(
                f'No CSV headers match columns of {table_name}.\n'
                f'CSV headers: {", ".join(headers)}\n'
                f'Expected names: {expected}'
            )

        missing_required = [col for col in spec['required'] if col not in mapping.values()]
        if missing_required:
            raise SystemExit(
                f'CSV is missing required column(s) for {table_name}: {", ".join(missing_required)}'
            )

        auto_filled = [c for c in db_columns if c not in mapping.values()]
        print(f'Table: {table_name}')
        print(f'File:  {csv_path} ({encoding})')
        print(f'DB:    {db_path}')
        print(f'Matched columns: {", ".join(mapping.values())}')
        if ignored:
            print(f'Ignored CSV columns (name does not match): {", ".join(ignored)}')
        if auto_filled:
            print(f'Not in CSV, filled automatically: {", ".join(auto_filled)}')

        used_nums = _existing_nums(conn, table_name)
        next_num = _next_num(conn, table_name)
        existing_keys, identity_cols = _load_identity_keys(
            conn, table_name, spec['identity'], db_columns
        )
        inserted = 0
        skipped_dup = 0
        skipped_empty = 0
        insert_cols = db_columns
        placeholders = ','.join('?' * len(insert_cols))
        insert_sql = (
            f'INSERT INTO {_quote_ident(table_name)} '
            f'({", ".join(_quote_ident(c) for c in insert_cols)}) VALUES ({placeholders})'
        )

        for i, raw in enumerate(rows, start=2):
            prepared, skip_reason = _prepare_row(raw, mapping, db_columns, spec, i)
            if prepared is None:
                skipped_empty += 1
                if skip_reason:
                    print(f'  skip row {i}: {skip_reason}')
                continue

            key = _identity_key(prepared, identity_cols)
            if identity_cols and key in existing_keys:
                skipped_dup += 1
                continue
            existing_keys.add(key)

            num = prepared.get('Num')
            if num is None or num in used_nums:
                if num in used_nums:
                    print(f'  row {i}: Num={num} already exists, assigning {next_num}')
                num = next_num
                next_num += 1
            prepared['Num'] = num
            used_nums.add(num)

            conn.execute(insert_sql, [prepared.get(col) for col in insert_cols])
            inserted += 1

        conn.commit()
        stats_added = ensure_all_stats_tables(conn, [table_name])
        conn.commit()
    finally:
        conn.close()

    print(f'Inserted: {inserted}')
    print(f'Skipped duplicates: {skipped_dup}')
    print(f'Skipped empty/invalid: {skipped_empty}')
    print(f'SRS stats rows added: {stats_added}')
    return inserted


def _infer_table(csv_path, explicit):
    if explicit:
        name = explicit.strip()
        key = {k.lower(): k for k in DICT_TABLES}.get(name.lower())
        if not key:
            raise SystemExit(
                f'Unknown table {explicit!r}. Choose one of: {", ".join(DICT_TABLES)}'
            )
        return key
    stem = os.path.splitext(os.path.basename(csv_path))[0]
    key = {k.lower(): k for k in DICT_TABLES}.get(stem.lower())
    if key:
        return key
    raise SystemExit(
        'Please pass --table with one of: ' + ', '.join(DICT_TABLES)
    )


def main():
    parser = argparse.ArgumentParser(
        description='Append CSV rows to Jp.db (does not delete existing words).'
    )
    parser.add_argument('csv_path', help='Path to the CSV file')
    parser.add_argument(
        '-t', '--table',
        help='Target table: Kanji, Words, Frazes, Kana, or Name. '
             'Optional if the file name is e.g. Kanji.csv',
    )
    parser.add_argument(
        '--db',
        help='Path to the SQLite database (default: Jp.db in the project root)',
    )
    args = parser.parse_args()
    table_name = _infer_table(args.csv_path, args.table)
    import_csv(args.csv_path, table_name, db_path=args.db)


if __name__ == '__main__':
    main()
