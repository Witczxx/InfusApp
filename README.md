# InfusApp (Final Project of CS50P: Introduction to Python)

A terminal UI (TUI) that helps nurses automate IV infusion monitoring and 
documentation. Tap a button in time with the drip rhythm to measure flow 
rate; the app calculates infusion speed, duration, and completion time, then 
records everything automatically.

# Features

- Nurse registration with bcrypt-hashed passwords and validity check
- Patient and medication intake recording (name, medication, volume)
- Rhythm-based flow-rate detection (tap 3× with the drip rhythm)
- Automatic infusion speed and completion-time calculation
- Persistent records of past infusions

# Getting Started

### Clone the Project
git clone <your-repo-url>
cd InfusApp

### 2. Install Dependencies
uv sync

### 3 Create Database and Seed Data
uv run python scripts/schema.py
uv run python scripts/import_from_txt.py

### 4. Run the App
uv run python src/infusapp/main.py
