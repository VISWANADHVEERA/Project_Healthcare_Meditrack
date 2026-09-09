"""
storage.py -- Saving & loading data to files.
"""

import os

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(_PROJECT_DIR, "data")
PATIENTS_FILE = os.path.join(DATA_DIR, "patients.txt")
VISIT_LOG_FILE = os.path.join(DATA_DIR, "patient_visits.txt")

_HEADER = ("ID|NAME|DOB|GENDER|BLOOD_GROUP|ALLERGIES|"
           "height_cm|weight_kg|systolic|diastolic|heart_rate|temperature_f")


def _ensure_data_dir():
    """Create the data/ folder if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


def save_patients(patients, path=PATIENTS_FILE):
    """Write every patient to a text file, one record per line."""
    _ensure_data_dir()
    lines = [_HEADER + "\n"]
    for p in patients:
        v = p.get("VITALS", {})
        allergy_csv = ",".join(sorted(p.get("ALLERGIES", set())))
        
        # Safely resolve temperature key
        temp = v.get("temperature_f", v.get("temaperature_f", v.get("temperature_c", 98.6)))
        
        line = "|".join([
            str(p.get("ID", "")),
            str(p.get("NAME", "")),
            str(p.get("DOB", "")),
            str(p.get("GENDER", "")),
            str(p.get("BLOOD_GROUP", "")),
            allergy_csv,
            str(v.get("height_cm", 0)),
            str(v.get("weight_kg", 0)),
            str(v.get("systolic", 0)),
            str(v.get("diastolic", 0)),
            str(v.get("heart_rate", 0)),
            str(temp),
        ]) + "\n"
        lines.append(line)

    with open(path, "w") as f:
        f.writelines(lines)
    return len(patients)


def load_patients(path=PATIENTS_FILE):
    """Read patients back from the text file into a list of dicts."""
    patients = []
    try:
        with open(path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return patients

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) != 12:
            continue
        (pid, name, dob, gender, bg, allergy_csv,
         height, weight, sys_bp, dia_bp, hr, temp) = parts

        allergies = {a for a in allergy_csv.split(",") if a}
        patient = {
            "ID": pid,
            "NAME": name,
            "DOB": dob,
            "GENDER": gender,
            "BLOOD_GROUP": bg,
            "ALLERGIES": allergies,
            "VITALS": {
                "height_cm": float(height),
                "weight_kg": float(weight),
                "systolic": int(sys_bp),
                "diastolic": int(dia_bp),
                "heart_rate": int(hr),
                "temperature_f": float(temp),
            },
            "VISITS": [],
        }
        patients.append(patient)
    return patients


def log_visit(patient_id, name, symptom, path=VISIT_LOG_FILE):
    """Append ONE visit line to the log file."""
    _ensure_data_dir()
    with open(path, "a") as f:
        f.write(f"{patient_id}, {name}, {symptom}\n")


def read_visit_log(path=VISIT_LOG_FILE):
    """Return every visit line as a list."""
    log = []
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    log.append(line)
    except FileNotFoundError:
        return log
    return log


def preview_file(path, n_lines=3):
    """Return first n_lines of a file with cursor report."""
    preview = []
    try:
        with open(path, "r") as f:
            for _ in range(n_lines):
                line = f.readline()
                if not line:
                    break
                preview.append(line.strip())
            position = f.tell()
            f.seek(0)
    except FileNotFoundError:
        return [], 0
    return preview, position