# Japanese Vocabulary Trainer

A desktop app (PyQt5) for studying and reviewing Japanese vocabulary with a
spaced-repetition system (SRS). It lets you edit your own dictionary tables,
run several test modes, track detailed progress, and optionally generate
example sentences via an AI API.

## Features

- **Dictionary editor** — multiple tables (`Dictio`, `Words`, `Frazes`, `Name`,
  `Kana`) backed by SQLite, with per-column filters, search (Ctrl+F),
  copy/paste, and inline editing.
- **Test modes**
  - Standard "show word / reveal answer" flow with `Know` / `Hard` / `Easy`
    grading.
  - Quiz mode with 4 answer choices.
  - "All answers" mode that groups entries by kanji/kun/on.
  - Repeat mode and "repeat unrecognized words".
- **Spaced repetition (SRS)** — per-direction statistics (e.g. Kanji→Trans),
  geometric review intervals, and difficulty transitions (hard ↔ normal ↔ easy).
- **Reports** — overview, breakdowns (by lesson / part of speech / direction),
  hardest/easiest words, the SRS due queue, stuck words, and direction
  asymmetry.
- **AI context (optional)** — generates an example sentence for the current
  word through an OpenAI-compatible chat API.

## Tech stack

- Python 3
- PyQt5 (GUI)
- SQLite (storage, via `sqlite3` and `QtSql`)
- pandas (data loading/filtering)

## Project structure

| File | Responsibility |
| --- | --- |
| `main.py` | App entry point and main menu |
| `jap_wind_test.py` | Test window and all test modes |
| `table.py` | Dictionary table editor (QTableView + QSqlTableModel) |
| `file_stats.py` | Reports window (UI) |
| `stats_reports.py` | Report calculations |
| `stats_script.py` | SRS logic and SQLite stats tables |
| `ai_settings.py` | AI credentials dialog + storage |
| `others_scripts.py` | Shared helpers |
| `styles.py` | Qt stylesheets |
| `table_logger.py` | Debug logging for the table window |

## Getting started

### Requirements

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

On first run, if `Jp.db` has no tables, the default table structure is created
automatically. You can then add rows in the table editor.

### AI context (optional)

Open **AI Settings** from the main menu and provide an API key, model name, and
an OpenAI-compatible chat completions URL. Credentials are stored locally in
`ai_secrets.py` (this file is not meant to be committed).

## Notes

- The dictionary content (the translations themselves) is stored in `Jp.db`.
- Part-of-speech codes are stored in the database in their original short form.
