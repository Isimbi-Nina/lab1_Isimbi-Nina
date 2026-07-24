# Lab 1: Grade Evaluator & Archiver

## Files
- `grade-evaluator.py` — Reads `grades.csv`, validates scores/weights, calculates GPA, determines Pass/Fail status, and reports formative assignment(s) eligible for resubmission.
- `organiser.sh` — Archives the current `grades.csv` with a timestamp, resets the workspace with a fresh empty `grades.csv`, and logs the action to `organiser.log`.
- `grades.csv` — Sample grade data used for testing.

## Requirements
- Python 3

## How to run the Python application

1. Make sure `grades.csv` is in the same folder as `grade-evaluator.py`.
2. Run:
   ```bash
   python3 grade-evaluator.py
   ```
3. When prompted, enter the CSV filename (e.g. `grades.csv`).
4. The script will print:
   - Formative and Summative category percentages
   - Total weighted grade and final GPA (out of 5.0)
   - Final status (`PASSED` or `FAILED`)
   - Any formative assignment(s) eligible for resubmission (the failed formative
     assignment(s) with the highest weight; ties are all listed)

**Note:** A student only passes if they score at least 50% in **both** the
Formative and Summative categories, not just 50% overall. Weights must add
up to exactly 100 overall, 60 for Formative, and 40 for Summative, or the
script will report a validation error and exit.

## How to run the shell script

1. Make the script executable (first time only):
   ```bash
   chmod +x organiser.sh
   ```
2. Run it from the folder containing `grades.csv`:
   ```bash
   ./organiser.sh
   ```
3. What it does:
   - Creates an `archive/` folder if one doesn't already exist.
   - Renames `grades.csv` to `grades_<TIMESTAMP>.csv` (e.g. `grades_20260724-195238.csv`)
     and moves it into `archive/`.
   - Creates a brand-new, empty `grades.csv` in the current directory so the
     workspace is ready for the next batch of grades.
   - Appends a record of the run (timestamp, original filename, archived filename)
     to `organiser.log`, which accumulates entries across every run.

