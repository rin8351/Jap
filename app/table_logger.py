# -*- coding: utf-8 -*-
"""
Logging of actions in the table window (table.py) for debugging.
The log file is cleared when the table window is opened again.
"""
from datetime import datetime
import os
import json

from app.others_scripts import PROJECT_ROOT

# Log file at the project root (gitignored)
LOG_FILE = os.path.join(PROJECT_ROOT, 'table_debug.log')


def _timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def table_log(action, **kwargs):
    """Write one log entry: timestamp, action, and optional fields."""
    try:
        row = {'time': _timestamp(), 'action': action}
        for k, v in kwargs.items():
            if isinstance(v, (list, dict)):
                row[k] = v
            else:
                row[k] = v
        line = json.dumps(row, ensure_ascii=False) + '\n'
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line)
    except Exception as e:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(_timestamp() + ' [LOGGER ERROR] ' + str(e) + '\n')


def clear_table_log():
    """Clear the log file (call when the table window is open)."""
    try:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write('')
    except Exception:
        pass
