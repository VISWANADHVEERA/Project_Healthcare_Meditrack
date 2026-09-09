from meditrack import data, utils

def add_patient(name, dob, gender, blood_group, allergies, **extra):
    """Add a new patient to the system with the provided details."""
    patient_id = utils.generate_patient_id()
    name = utils.clean_name(name)
    dob = utils.clean_dob(dob)

    if not utils.is_valid_blood_group(blood_group):
        raise ValueError(f"Invalid blood group: {blood_group}")

    age = utils.calculate_age(dob)
    allergies = set(allergies)

    vitals = {
        "height_cm": extra.get("height_cm", 0.0),
        "weight_kg": extra.get("weight_kg", 0.0),
        "heart_rate": extra.get("heart_rate", 0),
        "systolic": extra.get("systolic", 0),
        "diastolic": extra.get("diastolic", 0),
        "temperature_f": extra.get("temperature_f", 98.6)
    }

    patient = {
        "ID": patient_id,
        "NAME": name,
        "DOB": dob,
        "AGE": age,
        "GENDER": gender,
        "BLOOD_GROUP": blood_group,
        "ALLERGIES": allergies,
        "VITALS": vitals,
        "VISITS": []
    }

    data.patients.append(patient)
    return patient

def find_by_id(patient_id):
    for patient in data.patients:
        if patient["ID"] == patient_id:
            return patient
    return None

def find_by_name(keyword):
    keyword = keyword.lower().strip()
    return [p for p in data.patients if keyword in p["NAME"].lower()]

def add_visit(patient_id, date=None, *reasons):
    patient = find_by_id(patient_id)
    if not patient:
        raise ValueError("Patient not found")
    date = date or utils.today_str()
    reason = ", ".join(reasons) if reasons else "General consultation"
    patient["VISITS"].append((date, reason))
    return True

def all_allergies():
    combined = set()
    for patient in data.patients:
        combined |= patient.get("ALLERGIES", set())
    return combined