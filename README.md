# Japanese Vocabulary Trainer

A desktop app (PyQt5) for studying and reviewing Japanese vocabulary with a
spaced-repetition system (SRS). It lets you edit your own dictionary tables,
run several test modes, track detailed progress, and optionally generate
example sentences via an AI API.

## Features

- **Dictionary editor** — multiple tables (`Kanji`, `Words`, `Frazes`, `Name`,
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

```
.
├── main.py              # App entry point and main menu
├── Jp.db                # SQLite dictionary + SRS stats
├── ai_secrets.py        # Local AI credentials (gitignored)
├── requirements.txt
├── README.md
├── TEST_AND_SRS.md      # Test modes and SRS statistics guide
├── media/               # Images and icons
├── app/                 # Application modules
│   ├── jap_wind_test.py # Test window and all test modes
│   ├── table.py         # Dictionary table editor
│   ├── file_stats.py    # Reports window (UI)
│   ├── stats_reports.py # Report calculations
│   ├── stats_script.py  # SRS logic and SQLite stats tables
│   ├── ai_settings.py   # AI credentials dialog + storage
│   ├── others_scripts.py# Shared helpers / paths
│   ├── styles.py        # Qt stylesheets
│   └── table_logger.py  # Debug logging for the table window
└── scripts/
    └── seed_demo_db.py  # Optional demo DB seeder
```

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

## Documentation

- [Test modes and SRS statistics](TEST_AND_SRS.md) — how the review test works and how
  spaced-repetition progress is recorded.

## Notes

- The dictionary content (the translations themselves) is stored in `Jp.db`.
- Part-of-speech codes are stored in the database in their original short form.
