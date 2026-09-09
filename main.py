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
    bmi = vitals.calculate_bmi(v.get("weight_kg", 0), v.get("height_cm", 0))
    score = vitals.risk_score(p)
    allergies = ", ".join(sorted(p.get("ALLERGIES", []))) or "None"

    print(utils.divider(p["NAME"]))
    print(f"  ID           : {p['ID']}")
    print(f"  Age / Gender : {utils.calculate_age(p['DOB'])} / {p['GENDER']}")
    print(f"  Blood group  : {p['BLOOD_GROUP']}")
    print(f"  Allergies    : {allergies}")
    print(f"  BMI          : {bmi} ({vitals.bmi_category(bmi)})")
    print(f"  Blood press. : {v.get('systolic', 0)}/{v.get('diastolic', 0)} "
          f"({vitals.bp_category(v.get('systolic', 0), v.get('diastolic', 0))})")
    print(f"  Risk score   : {score} ({vitals.risk_label(score)})")
    print(f"  Visits       : {len(p.get('VISITS', []))}")
    for date, reason in p.get("VISITS", []):
        print(f"     - {date}: {reason}")

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
        choice = input(MENU).strip()

        if choice == "1":
            if not data.patients:
                print("\nNo patients registered.")
            else:
                for p in data.patients:
                    show_patient(p)

        elif choice == "2":
            pid = input("Enter Patient ID (e.g. PAT-1000-1234): ").strip()
            p = patients.find_by_id(pid)
            if p:
                show_patient(p)
            else:
                print(f"Patient with ID '{pid}' not found.")

        elif choice == "3":
            kw = input("Enter name to search: ").strip()
            matches = patients.find_by_name(kw)
            if matches:
                for p in matches:
                    show_patient(p)
            else:
                print(f"No patients found matching '{kw}'.")

        elif choice == "4":
            print("\n--- Register New Patient ---")
            name = input("Full Name: ").strip()
            dob = input("Date of Birth (YYYY-MM-DD): ").strip()
            gender = input("Gender (M/F/Other): ").strip().upper()
            bg = input("Blood Group (e.g. A+, O-): ").strip().upper()
            allergies_raw = input("Allergies (comma-separated, optional): ").strip()
            allergies = [a.strip() for a in allergies_raw.split(",") if a.strip()]

            print("\n--- Vitals (press Enter for defaults) ---")
            height_cm = ask_number("Height (cm) [170]: ", 170.0)
            weight_kg = ask_number("Weight (kg) [70]: ", 70.0)
            systolic = ask_number("Systolic BP [120]: ", 120, as_int=True)
            diastolic = ask_number("Diastolic BP [80]: ", 80, as_int=True)
            heart_rate = ask_number("Heart Rate [72]: ", 72, as_int=True)
            temp_f = ask_number("Temperature (°F) [98.6]: ", 98.6)

            try:
                new_p = patients.add_patient(
                    name=name,
                    dob=dob,
                    gender=gender,
                    blood_group=bg,
                    allergies=allergies,
                    height_cm=height_cm,
                    weight_kg=weight_kg,
                    systolic=systolic,
                    diastolic=diastolic,
                    heart_rate=heart_rate,
                    temperature_f=temp_f
                )
                print(f"\nPatient successfully registered with ID: {new_p['ID']}")
            except ValueError as e:
                print(f"\nError creating patient: {e}")

        elif choice == "5":
            pid = input("Enter Patient ID: ").strip()
            p = patients.find_by_id(pid)
            if not p:
                print("Patient not found.")
                continue

            reason = input("Visit reason: ").strip()
            date_input = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
            visit_date = date_input if date_input else utils.today_str()

            try:
                patients.add_visit(pid, visit_date, reason)
                storage.log_visit(pid, p["NAME"], reason)
                print("Visit logged successfully.")
            except ValueError as e:
                print(f"Error adding visit: {e}")

        elif choice == "6":
            threshold = ask_number("Enter risk threshold [60]: ", 60, as_int=True)
            print(f"\nPatients with risk score >= {threshold}:")
            high_risk = analytics.high_risk_patients(data.patients, threshold)
            if not high_risk:
                print("No high-risk patients found.")
            else:
                for line in analytics.risk_report_lines(high_risk):
                    print(f"  {line}")

        elif choice == "7":
            total_depts = analytics.count_departments(data.HOSPITAL)
            print(f"\n{data.HOSPITAL['name']} ({total_depts} total units/departments):")
            for dept in analytics.list_departments(data.HOSPITAL):
                print(f"  {dept}")

        elif choice == "8":
            print("\n=== SYSTEM DEMO ===")
            print(f"Total Patients: {len(data.patients)}")
            print(f"Average Age   : {analytics.average_age(data.patients, utils.calculate_age)} yrs")
            print("\nNext available appointments:")
            for slot in utils.next_appointment_slots():
                print(f"  - {slot}")

        elif choice == "9":
            count = storage.save_patients(data.patients)
            print(f"Successfully saved {count} patients to file.")

        elif choice == "10":
            loaded = storage.load_patients()
            if loaded:
                data.patients = loaded
                print(f"Successfully loaded {len(loaded)} patients into memory.")
            else:
                print("No patients file found or file is empty.")

        elif choice == "11":
            logs = storage.read_visit_log()
            if not logs:
                print("No visit logs found.")
            else:
                print("\n--- Visit Logs ---")
                for entry in logs:
                    print(f"  {entry}")

        elif choice == "0":
            print("Exiting MediTrack. Goodbye!")
            break

        else:
            print("Invalid option. Please choose from 0-11.")

if __name__ == "__main__":
    menu_loop()


