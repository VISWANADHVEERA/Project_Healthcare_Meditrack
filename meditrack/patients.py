from meditrack import data, utils


def add_add_patient(name, dob, gender, blood_group, allergies, **extra):
    """
    Add a new patient to the system with the provided details.
    """
    from meditrack.utils import clean_name, clean_dob, calculate_age, is_valid_blood_group, generate_patient_id, today_str, calulate_age

    # gerate a unique patient ID

    patient_id = generate_patient_id()

    #clean name
    name = clean_name(name)

    #clean dob
    dob = clean_dob(dob)

    #validate blood group
    if not is_valid_blood_group(blood_group):
        raise ValueError(f"Invalid blood group: {blood_group}")

    #calculate age
    age = calculate_age(dob)

    #Allergies set
    allergies = set(allergies)

    #vitals
    vitals = {
        "height_cm": extra.get("height_cm", 0),
        "weight_kg": extra.get("weight_kg", 0),
        "heart_rate": extra.get("heart_rate", 0),
        "systolic": extra.get("systolic", 0),
        "diastolic": extra.get("diastolic", 0),
        "temperature_f": extra.get("temperature_f", 98.6)
    }

    patient = {
        "ID" : patient_id,
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


# Find a patient by their ID
def find_by_id(patient_id):
    for patient in data.patients:
        if patient["ID"] == patient_id:
            return patient
        return None


# Find a patient by their NAME
def find_by_name(keyword):
    keyword = keyword.lower().strip()
    matches = []
    for patient in data.patients:
        if keyword in patient["NAME"].lower():
            matches.append(patient)
    return matches

#adding visits
def add_visit(patient_id, date=None, *reasons):
    patient = find_by_id(patient_id)
    if not patient:
        raise ValueError("Patient not found")
    date = date or utils.today_str()
    reason = ", ".join(reasons) if reasons else "General consultation"
    patient["visits"].append((date, reason))
    return True

#combined all allergies
def all_allergies():
    combined = set()
    for patient in data.PATIENTS:
        combined |= patient["allergies"]
    return combined
