#   `from meditrack import data, utils, vitals, patients, analytics`.
#   Write `show_patient(p)` that prints a nicely formatted patient card
#   (id, age, blood group, allergies, BMI + category, BP + stage, risk, visits).
from prompt_toolkit import prompt

from meditrack import data, utils, vitals, patients, analytics, storage

__version__ = "1.1.0"
__all__ = ["utils", "data", "vitals", "patients", "analytics", "storage"]

def show_patient(p):
    """Pretty-print one patient record."""
    v = p["VITALS"]
    bmi = vitals.calculate_bmi(v["weight_kg"], v["height_cm"])
    score = vitals.risk_score(p)
    allergies = ", ".join(sorted(p["ALLERGIES"])) or "None"

    print(utils.divider(p["NAME"]))
    print(f"  ID           : {p['ID']}")
    print(f"  Age / Gender : {utils.calculate_age(p['DOB'])} / {p['GENDER']}")
    print(f"  Blood group  : {p['BLOOD_GROUP']}")
    print(f"  Allergies    : {allergies}")
    print(f"  BMI          : {bmi} ({vitals.bmi_category(bmi)})")
    print(f"  Blood press. : {v['systolic']}/{v['diastolic']} "
          f"({vitals.bp_category(v['systolic'], v['diastolic'])})")
    print(f"  Risk score   : {score} ({vitals.risk_label(score)})")
    print(f"  Visits       : {len(p['VISITS'])}")
    for date, reason in p["VISITS"]:
        print(f"     - {date}: {reason}")

#   - a `while True` loop that prints options and reads `input()`
#   - `if / elif / else` branches for: list all, view by id, search, add patient,
#     add visit, high-risk report, departments, and exit
#   - `break` out of the loop on the exit option

#   Handle bad blood groups with `try / except ValueError`.


MENU = """
Choose an option:
  1) List all patients
  2) View a patient by ID
  3) Search patients by name
  4) Add a new patient
  5) Add a visit
  6) High-risk report
  7) Hospital departments
  8) Run full demo
  9) Save patients to file
 10) Load patients from file
 11) View visit log
  0) Exit
> """

def ask_number(prompt, default, as_int=False):
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return default
        try:
            return int(raw) if as_int else float(raw)
        except ValueError:
            print("    Please enter a number (or press Enter to skip).")


def menu_loop():
  while True:
    pass



