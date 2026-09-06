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