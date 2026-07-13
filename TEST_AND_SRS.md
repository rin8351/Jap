# Japanese vocabulary review — guide

The review module (`app/jap_wind_test.py`) is a trainer for Japanese vocabulary with a
spaced-repetition system (SRS). The program decides which words to show and how often:
words you know reliably gradually move to **easy** and appear less often, while hard and
new words appear more often.

All statistics are stored in `Jp.db` (SQLite). The scoring and scheduling logic lives in
`app/stats_script.py`.

---

## 1. Database contents

Words are split across several tables (chosen with the menu button at the top of the test window):

| Table    | What you train | Question / answer fields |
|----------|----------------|--------------------------|
| `Kanji`  | Kanji          | `Kanji`, `On`, `Kun`, `Trans` (translation) |
| `Words`  | Words          | `Kanji`, `Read` (reading), `Trans` |
| `Kana`   | Kana           | `Kun`, `Trans` |
| `Frazes` | Phrases        | `Kanji`, `Read`, `Trans` |
| `Name`   | Names          | `Kanji`, `Read` |

Extra fields:

- **`Lesson`** — lesson number. Used by the lesson filter.
- **`Sush`** — part of speech (noun, verb, adjective, adverb). Present on `Kanji` and
  `Kana`; you can filter the test by it.
- **`Mnem`** — mnemonic / usage example (see “Mnemonics”).

---

## 2. Test setup

All test parameters are chosen in the starting window.

### Test type

- **Standard (default).** A question is shown; you recall the answer, press
  **Show answer**, and the correct answer appears below. Then you grade yourself with
  **Know** / **Hard** / **Easy**. This mode **updates statistics**.
- **Repeat mode (normal + easy only)** — checkbox `Repeat mode (normal + easy only)`.
  Only words that already have stats and difficulty `normal` or `easy` are included
  (see difficulty levels below). New and **hard** words are excluded. Useful when you
  want to review only what you already know reasonably well.
- **4-choice quiz** — checkbox for quiz mode with four answer options.
  **Does not update statistics.** That is intentional: picking one of four (especially
  by elimination) is too easy and does not reflect real recall. Use it to drill words
  without affecting SRS. Requires exactly one answer column.
- **All-answers variant** — checkbox `All-answers variant` (Kanji table only).
  Needed when the database has several rows with the same tested element but different
  answers — for example two `生` kanji with different kun readings `なま` and `いきる`
  on separate rows. In this mode the test shows all answers for that element as a list.
  By default (without the checkbox) such rows are shown one at a time.

> The “4-choice” and “All answers” checkboxes are mutually exclusive; “Repeat mode” and
> “4-choice” also cannot be enabled together.

### Lesson selection

- **Lesson range** — “First lesson” and “Last lesson” fields.
- **Single lesson** — “Select one lesson” dropdown (overrides the range).
- **All words without filtering** — checkbox. Disables the SRS filter: every word in
  the selected range is included regardless of stats. Use this when you want to drill a
  word many times even though its schedule would only show it in a few days.

### Subject and direction

- **“Select the test subject”** — what to show as the question (e.g. for kanji: `Kanji`,
  `On`, `Kun`, `Trans`).
- **“Select what to test”** — what to show as the answer. You can select several columns
  (an answer table appears), but 4-choice and All-answers modes allow only one.

> **Important:** statistics are tracked **per direction**. For example “kanji → kun” and
> “kun → kanji” are two independent records, each with its own progress and intervals.

### Part of speech

For `Kanji` and `Kana`, part-of-speech checkboxes appear (Noun, Verb, Adj, etc.) so you
can limit the test to selected parts of speech.

---

## 3. Taking the test

1. A question is shown (word / kanji / reading).
2. Press **Show answer** — the answer appears below.
3. Grade yourself:
   - **Know** — you got it right. Records a correct answer (`right`).
     The system relies on honesty: in standard mode the program cannot verify whether
     you really knew the answer.
   - **Hard** — mark the word as difficult (available after the answer is shown).
   - **Easy** — mark the word as easy. **Only available after Know**, and only if the
     word is not already `hard`.
4. If you **did not press Know** and moved to the next word, a wrong answer (`wrong`)
   is recorded.

Also:

- **Context** — asks the AI for an example sentence with the current word. Shown only if
  AI settings are filled in (`ai_secrets.py`) and the test has both a translation and a
  reading/kanji.
- At the end of the test you see the correct-answer percentage and, if there were
  mistakes, **Repeat unrecognized words**.

### Mnemonics

You can store a mnemonic (or usage example) in `Mnem` for any word. During the test, a
**“has mnemonic”** label appears above the word — hovering shows the mnemonic tooltip.
The label is visible **only** when a mnemonic is actually stored for that word.

---

## 4. How statistics work (SRS)

For each word (in each test direction) the following are stored:

- **`difficulty`** — level: `hard`, `normal`, or `easy`;
- **`right`** — streak of correct answers in a row (reset on error);
- **`wrong`** — streak of errors in a row (reset on a correct answer);
- **`last_right`** — date of the last correct answer;
- **`interval_days`** — how many days until the word is due again;
- **`right_all` / `wrong_all`** — lifetime totals.

### 4.1. Which words enter the test (filter)

In a normal test (without “All words without filtering”), a word is included if:

- it is **new** (no stats record yet); **or**
- its level is **`hard`** (hard words are always included; if a hard word has
  `wrong ≥ 3`, it is added to the test **twice**); **or**
- it has outstanding errors (**`wrong > 0`**); **or**
- it is `normal`/`easy` and the **review date has arrived** (`interval_days` days have
  passed since `last_right`).

Words with the same `Num` are not duplicated in the test (except the hard doubling above).

### 4.2. Word order (sorting)

Within a test, words are ordered as follows:

1. **New** words (not yet in stats) — in random order.
2. Then words that have stats, **by difficulty**: **`hard`**, then **`normal`**, then
   **`easy`**.
3. Within each level — by descending error count (`wrong`): more errors come earlier.

> Clarification: words with errors (`wrong > 0`) are **not** a separate group right after
> new words. They are sorted **within their difficulty level**. So after new words come
> all `hard` (sorted by errors), then all `normal`, then all `easy`.

### 4.3. Difficulty changes

Difficulty changes in two ways — manually (**Easy** / **Hard** buttons) and automatically:

**Correct answers in a row (Know):**

- `hard` → `normal` — after **3** correct answers in a row;
- `normal` → `easy` — after **4** correct answers in a row.

**Errors in a row (did not press Know):**

- `normal` → `hard` — after **3** errors in a row;
- `easy` → `normal` — after **3** errors in a row;
- `hard` with 3 errors stays `hard`, but starts appearing twice in the test.

**Manual:**

- **Hard** sets difficulty to `hard`.
- **Easy** sets difficulty to `easy` (and resets the interval to the initial easy value).

### 4.4. Review intervals (constants near the top of `app/stats_script.py`)

Base constants:

| Constant | Value | Meaning |
|----------|-------|---------|
| `NORMAL_DAYS_INITIAL` | `2` | starting interval base for `normal` |
| `EASY_DAYS_INITIAL`   | `4` | starting interval base for `easy` (also used when promoting to easy) |
| `NORMAL_INTERVAL_MULTIPLIER` | `2.0` | how much the `normal` interval grows per correct answer |
| `EASY_INTERVAL_MULTIPLIER`   | `2.5` | how much the `easy` interval grows |
| `MAX_INTERVAL_DAYS`   | `190` | maximum interval (cap) |

Rule: on each correct answer (except when promoting to a new level), the interval is
multiplied by the multiplier and rounded, but never exceeds `190` days. Longer correct
streaks mean rarer appearances.

**Progression for `normal`** (new word, each Know in a row):

```
1st Know: 4 days   (2 × 2)
2nd Know: 8 days   (4 × 2)
3rd Know: 16 days  (8 × 2)
4th Know: word becomes easy; interval resets to 4 days
```

**Progression for `easy`** (after promotion to easy, starting interval 4 days):

```
1st Know: 10 days   (4 × 2.5)
2nd Know: 25 days   (10 × 2.5)
3rd Know: ~62 days  (25 × 2.5)
4th Know: ~155 days (62 × 2.5)
5th Know: 190 days  (cap)
further:  stays at 190 days
```

**Special interval values:**

- on `normal → hard` (3 errors): interval = `1` day;
- on `easy → normal` (3 errors): interval = `2` days (`NORMAL_DAYS_INITIAL`);
- on `hard → normal` (3 correct): interval = `2` days;
- on `normal → easy` (4 correct): interval = `4` days (`EASY_DAYS_INITIAL`);
- an error (`wrong > 0`) puts the word back in the test immediately, regardless of interval.

---

## 5. How stats are stored

Stats live in separate tables in `Jp.db`, one per test direction.
Table names are `{prefix}_{question}_{answer}` in lowercase, for example:

- `kanji_kanji_kun` — “kanji → kun” for the `Kanji` table;
- `words_read_trans` — “reading → translation” for the `Words` table.

Stats tables are created and topped up automatically on launch: new dictionary words are
added, and progress for existing records is never overwritten.
