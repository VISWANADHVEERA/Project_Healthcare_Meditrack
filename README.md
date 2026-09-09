🏥 MediTrack — Patient Health Record & Risk Management System
A console-based healthcare application built using ONLY the Python concepts. No external libraries, no classes/OOP— just core Python, functions, data structures, functional tools, generators, recursion, packages and the standard library.

1. Problem Statement
A small clinic needs a lightweight system (no database, no internet) to:

Store patient records (name, DOB, gender, blood group, allergies, vitals).

Automatically compute BMI, blood-pressure stage and an overall

health-risk score for each patient.

Search patients, add new patients and log visits.

Produce reports: high-risk patients, average age, all allergies on file.

Show the hospital's department hierarchy and generate appointment slots.

Everything runs in memory and prints to the terminal.

2. How to Run
Open a terminal inside this project folder and run:

python3  main.py  --demo  # runs an automated tour of every feature
or

python3  main.py  # opens the interactive menu
Requires Python 3 only. Nothing to install.

3. Project Structure (this itself is the Class 17 concept)

Project_Healthcare_MediTrack/

├── main.py # entry point: menu + demo (Class 08/09/18)

├── README.md # this file

└── meditrack/ # a PACKAGE (folder + __init__.py)

	├── __init__.py # makes it a package (Class 17)

	├── data.py # the in-memory "database" (Class 05/10/11/12)

	├── utils.py # helpers: strings, datetime, random, os, sys

	├── vitals.py # clinical math & rules (Class 06/08)

	├── patients.py # add / find / update (Class 13/14)

	├── analytics.py # reports: lambda/map/filter/reduce,

		│ # generators, recursion (Class 15/16)

	└── storage.py # save / load / visit log (Class 19: files)

  

data/ # created automatically the first time you save

	├── patients.txt # all patient records (one per line)

	└── patient_visits.txt # append-only visit log

A module = one .py file.

A package = the meditrack/ folder because it contains __init__.py.

A library = the standard library we import (os, sys, random,

datetime, functools).

4. Step-by-Step Solution
Step 1 — Model the data → data.py
Each patient is a dictionary.

All patients live in a list (PATIENTS).

allergies is a set (no duplicates).

Each visit is a tuple (date, reason) — immutable historical record.

HOSPITAL is a nested dict/list tree — used later for recursion.

Step 2 — Build reusable helpers → utils.py
clean_name() uses string methods (strip, split, join, title).

generate_patient_id() uses random + the global keyword (scope).

calculate_age() / next_appointment_slots() use datetime.

clear_screen() uses os + sys.

VALID_BLOOD_GROUPS is a frozenset (an immutable constant).

Step 3 — Encode the clinical rules → vitals.py
calculate_bmi() → arithmetic operators (/, **).

bmi_category() / bp_category() → if / elif / else decisions.

risk_score() → combines operators + branching into a rule engine.

Step 4 — CRUD with rich function signatures → patients.py
add_patient(name, dob, gender, blood_group, *allergies, **extra)
demonstrates every parameter kind: positional, default, *args, **kwargs.

find_by_id() / search_by_name() → loops with break / continue.

all_allergies() → set union (|=).

Step 5 — Reporting / functional layer → analytics.py
high_risk_patients() → filter + lambda.

summarise() → map.

average_age() → reduce (from functools).

patient_stream() / risk_report_lines() → generators (yield).

first_high_risk() → iterator protocol (iter / next).

count_departments() / list_departments() / factorial() → recursion.

Step 6 — Persist data to files → storage.py
save_patients() → opens the file in write mode 'w' and uses
writelines() to store every patient as a delimited line.

load_patients() → read mode 'r' + readlines(), rebuilds the dicts,
and handles FileNotFoundError when nothing is saved yet.

log_visit() → append mode 'a' to add a visit to the end of the log
(mirrors the Class 19 hospital example).

read_visit_log() → iterates the file line by line.

preview_file() → demonstrates readline(), tell() and seek().

All wrapped in the with open(...) as f: context manager (auto-closes).

Step 7 — Tie it together → main.py
A while loop menu with if/elif/else branching (now incl. save/load/log).

Reads sys.argv for the --demo flag and exits with sys.exit.

Uses the classic if __name__ == "__main__": entry-point guard.

6. Ideas to Extend (once you learn more)
Store visits inside the patients file too (currently kept in a separate log).

Save the data as CSV or JSON instead of a custom delimited format.

Turn each patient into a class (OOP).

Plot risk scores with a charting library.
