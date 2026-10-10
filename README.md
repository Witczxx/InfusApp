<div align="center">

# 💧 InfusApp

**A terminal application that helps nurses measure, calculate, and document IV infusions — one tap per drop.**

*Final Project of CS50P: Introduction to Programming with Python (Harvard)*

</div>

---

## 🔍 What is InfusApp?

**InfusApp** is a **terminal user interface (TUI)** application for nursing staff that automates the
monitoring and documentation of **intravenous (IV) infusions**.

Instead of manually counting dripping chambers with a stopwatch and writing down results on paper,
a nurse simply **taps any key in time with the falling drops** of the plugged infusion. InfusApp:

1. **Measures the drip rhythm** → computes the flow rate in *drops per minute*,
2. **Converts it** → to *milliliters per hour* using the standard drop factor,
3. **Calculates the finish time** → tells the nurse exactly when to unplug the infusion,
4. **Documents everything** → stores a complete record (nurse, patient, medication, volume, rates, start/stop times) in a local SQLite database.

It was built as the **final project for CS50P**, Harvard's *Introduction to Programming with Python*,
but it goes well beyond the basics: layered architecture, dependency injection, bcrypt authentication,
threaded real-time input handling, and a pytest suite covering repositories, services, and UI logic.

---

## 🩺 Why it exists

Manual infusion monitoring is error-prone and tedious:

- Counting drops by hand for a full minute (or estimating) is inaccurate and interrupts other work.
- Converting drops/min into mL/h and an expected end time requires arithmetic at the bedside.

InfusApp turns this whole workflow into **a few keystrokes**: tap along with the drip,
confirm the medication details picked from a real drug database, and the record is written automatically —
including a precise calculated stop time the nurse can rely on.

---

## 🎵 The core idea: rhythm-based flow-rate detection

While watching the drip chamber, the nurse presses **any key once per falling drop** (ESC stops). The tracker:

- Timestamps every key press via a `pynput` keyboard listener running in parallel with a live elapsed-time display;
- Keeps only the **last 5 intervals** between taps (sliding window), so early, erratic taps don't skew the result;
- Computes the rate live after every tap:

With the default medical **drop factor of 20 gtt/mL** (standard macro-drip set), e.g.:
> Tap rhythm ≈ 1 drop every 1.5 s → **40 drops/min → 120 mL/h** → a 500 mL bag finishes in ≈ 4 h 10 min.

Terminal hygiene is handled cross-platform: key echo is temporarily disabled (`termios` on macOS/Linux,
`msvcrt` on Windows), leftover keystrokes are flushed after measurement, and a print lock keeps the live
status line clean.

---

## ✨ Features

### 👩‍⚕️ Nurse account system
- **Registration** with name validation and password rules (8–32 characters)
- Passwords stored as **bcrypt hashes**
- **Login** by name *or* numeric nurse ID
- Unique 7-digit nurse IDs generated and collision-checked automatically

### 🧾 Patient management
- Search patients by name or ID while recording an infusion
- Unknown patients can be registered **inline**

### 💊 Real medication database (FDA Orange Book)
- Ships with a seeded SQLite database imported from the **FDA "Orange Book" dataset**
- Free-text ingredient search, **filtered to intravenous/injection routes only**.
- Guided selection of **strength** (numerically sorted) and display of **dosage forms**.
- Choose **units** (1/2/5/%, or custom) and optionally a **carrier fluid** (NaCl 0.9 %, Glucose 5 %, or free text).

### ⏱ Live infusion measurement
- Tap-in-rhythm counter with live `drops/min` and `mL/h` readout after every tap.

### 📅 Automatic calculation & documentation
- Enter the **total volume (mL)** → the app calculates **start time** and the **expected stop time** (`volume ÷ mL/h`).
- **Records view**: each nurse sees their own past infusions rendered as a clean `tabulate` grid.
- Abort anytime with `q` — raises `DocumentationAborted` and returns to the home menu without writing partial data.

### 🏠 Built-in help
- The home menu can print `docs/app_explanation.md` directly in the terminal

---

## 🚶 How a typical session looks

```text
1. Launch app            →  Login or Register as a Nurse
2. Home Screen           →  [1] Record an Infusion
3. Choose Patient        →  search by name/ID, or register inline
4. Choose Medication     →  type ingredient → pick from IV-only matches → pick strength
5. Units / Carrier Fluid →  guided menus
6. Total Volume          →  e.g. 500 mL
7. Infusion Speed Counter→  tap a key with each drop… ESC to stop
                           ⏱ Drop #12 | 41.3 drops/min | 123.9 ml/h
8. Results               →  drops/min + mL/h → start & calculated stop time computed
9. Saved                 →  full record written to SQLite
10. Home Screen          →  [2] Check your Infusion Records (table view)
```

---

## 🏗 Architecture

InfusApp follows a strict **layered architecture** with single-responsibility modules and manual
**dependency injection** performed in `Main` (`src/infusapp/main.py`):

```
┌──────────────────────────────────────────────────────────────┐
│  UI layer            (src/infusapp/ui/)                       │
│  AuthNurseUi · HomeUi · NewPatientUi · NewMediUi ·            │
│  MediUiHelper · NewInfusionUi · RecordUi                      │
│        ▲  runs the interaction loops, prompts, tables         │
├────────┼──────────────────────────────────────────────────────┤
│  Service layer  (src/infusapp/services/)                      │
│  NurseService · PatientService · MediService ·                │
│  InfusionService                                              │
│        ▲  validation, business rules, calculations, hashing   │
├────────┼──────────────────────────────────────────────────────┤
│  Repository layer     (src/infusapp/db/)                      │
│  NurseRepository · PatientRepository · MediRepository ·       │
│  InfusionRepository · RecordRepository                        │
│        ▲  parameterized SQL, row→model mapping helpers        │
├────────┼──────────────────────────────────────────────────────┤
│  Connection wrapper   (src/infusapp/db/connection.py)         │
│  Database: context-managed sqlite3 connections, commit/close, │
│  execute / executemany / fetchone / fetch_all                 │
└──────────────────────────────────────────────────────────────┘

Specialist module: InfusionTracker (infusion_tracker/) — real-time
keyboard sampling + statistics, used by NewMediUi during recording.

Shared dataclasses: models/models.py — Nurse, Patient, Medi
Custom exception:   exceptions/exceptions.py — DocumentationAborted
```

---

## 📁 Project structure

```text
InfusApp/
├── docs/
│   └── app_explanation.md          # In-app help text (printed by HomeUi option 3)
├── scripts/
│   ├── schema.py                   # Creates the 4 tables (idempotent: DROP IF EXISTS first)
│   ├── import_from_txt.py          # Cleans & bulk-imports the FDA dataset into `medications`
│   └── raw_data/
│       └── medi_db.txt             # Raw FDA Orange Book export (~48.6k lines, ';'-separated)
├── src/
│   └── infusapp/
│       ├── main.py                 # Composition root: DI wiring + entry point
│       ├── db/                     # connection.py + 5 repositories
│       ├── exceptions/             # DocumentationAborted
│       ├── infusion_tracker/       # Real-time tap-to-measure engine
│       ├── models/                 # Nurse, Patient, Medi dataclasses
│       ├── services/               # Nurse, Patient, Medi, Infusion services
│       └── ui/                     # All terminal screens/dialogs
├── tests/
│   ├── conftest.py                 # Temp-DB fixtures (schema applied per test run)
│   ├── db/                         # Repository & connection tests (real SQLite)
│   ├── services/                   # Business-logic tests (real bcrypt + temp DB)
│   └── ui/                         # Screen-flow tests (Mock services, monkeypatched input)
├── pyproject.toml                  # uv project: runtime + dev dependency groups
├── uv.lock                         # Locked, reproducible environments
└── LICENSE                         # AGPL-3.0
```

---

## 🚀 Getting Started

### 1. Clone the project

```bash
git clone https://github.com/Witczxx/InfusApp.git InfusApp
cd InfusApp
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Create the database and seed the medication data

> ℹ️ The `data/` directory must exist before the first run (SQLite does not create parent folders):
> ```bash
> mkdir -p data
> ```

```bash
uv run python scripts/schema.py           # creates the tables
uv run python scripts/import_from_txt.py  # imports the FDA medication dataset (~40k rows)
```

### 4. Run the app

```bash
uv run python src/infusapp/main.py
```

You'll land on the welcome screen — **register as a nurse first** (option `2`), note down your generated
ID, log in, and start recording. 🎉

---

## ✅ Running the tests

```bash
uv run pytest              # full suite
```

---

## ⚠️ Disclaimer

InfusApp is an **educational project** (CS50P final submission). It is **not a certified medical device**
and must not be used as the sole basis for clinical decisions. Flow rates measured by tapping are
estimates; always verify infusion parameters against institutional protocols and the equipment's actual
drop factor.
