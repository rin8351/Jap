"""One-time migration: rename Dictio -> Kanji and dictio_* stats tables -> kanji_*."""
import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), 'Jp.db')
conn = sqlite3.connect(DB)
cur = conn.cursor()

if cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='Dictio'").fetchone():
    cur.execute('ALTER TABLE "Dictio" RENAME TO "Kanji"')
    print('Renamed table Dictio -> Kanji')

for (name,) in cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'dictio_%'"
).fetchall():
    new_name = 'kanji_' + name[len('dictio_'):]
    cur.execute(f'ALTER TABLE "{name}" RENAME TO "{new_name}"')
    print(f'Renamed {name} -> {new_name}')

for (name,) in cur.execute(
    "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'dictio_%'"
).fetchall():
    cur.execute(f'DROP TRIGGER IF EXISTS "{name}"')
    print(f'Dropped trigger {name}')

conn.commit()
conn.close()
print('Migration done.')

# Recreate sync triggers (requires stats_script only, no PyQt)
from stats_script import SYNC_COLUMNS_BY_SOURCE, STATS_PREFIXES, stats_column_role

def _quote_ident(name):
    return '"' + str(name).replace('"', '""') + '"'

def _get_stats_tables_for_column(conn, column_in_name):
    col_lower = column_in_name.lower()
    pattern = f'%{col_lower}%'
    prefix_conditions = ' OR '.join(
        f"(name LIKE '{prefix}_%' AND name LIKE '{pattern}')" for prefix in STATS_PREFIXES
    )
    sql = f"SELECT name FROM sqlite_master WHERE type='table' AND ({prefix_conditions})"
    rows = conn.execute(sql).fetchall()
    return [(r[0], stats_column_role(r[0], col_lower)) for r in rows if r[0]]

conn = sqlite3.connect(DB)
for source_table, columns in SYNC_COLUMNS_BY_SOURCE.items():
    prefix = source_table.lower() + '_'
    for column in columns:
        col_lower = column.lower()
        tables = _get_stats_tables_for_column(conn, col_lower)
        stats_list = [(t, c) for t, c in tables if str(t).lower().startswith(prefix)]
        if not stats_list:
            continue
        trigger_name = f'{source_table.lower()}_after_update_{col_lower}'
        conn.execute(f'DROP TRIGGER IF EXISTS {_quote_ident(trigger_name)}')
        updates = []
        for stat_table, stat_col in stats_list:
            updates.append(
                f'UPDATE {_quote_ident(stat_table)} SET {_quote_ident(stat_col)} = '
                f'NEW.{_quote_ident(column)} WHERE num = CAST(NEW.Num AS TEXT)'
            )
        body = '; '.join(updates)
        conn.execute(
            f'CREATE TRIGGER {_quote_ident(trigger_name)} '
            f'AFTER UPDATE OF {_quote_ident(column)} ON {_quote_ident(source_table)} '
            f'FOR EACH ROW BEGIN {body}; END'
        )
        print(f'Created trigger {trigger_name}')
conn.commit()
conn.close()
print('Triggers recreated.')
