def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate BMI(Body Mass Index) using the formula: BMI = weight(kg) / height(m)^2"""
    height_m = height_cm / 100
    if height_cm <= 0 or weight_kg <= 0:
        return 0
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

def bmi_category(bmi: float) -> str:
    """Determine the bmi category based on the BMI value."""
    if bmi <= 0:
        return "Invalid BMI"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obese"

def bp_category(systolic: int, diastolic: int) -> str:
    """Determine the blood pressure category based on systolic and diastolic values."""
    if systolic < 120 and diastolic < 80:
        return "Normal"
    if systolic < 130 and diastolic < 80:
        return "Elevated"
    if systolic < 140 or diastolic < 90:
        return "Hypertension Stage 1"
    return "Hypertension Stage 2"

def has_fever(temperature_f: float) -> bool:
    """Determine if the patient has a fever based on temperature in Fahrenheit."""
    return temperature_f >= 100.4

def risk_score(patient: dict) -> int:
    v = patient.get("VITALS") or patient.get("vitals", {})
    score = 0

    # BMI Risk
    bmi = calculate_bmi(v.get("weight_kg", 0), v.get("height_cm", 0))

    # BP Risk
    bp = bp_category(v.get("systolic", 0), v.get("diastolic", 0))

    if bmi >= 30:
        score += 30
    elif 30 > bmi >= 25:
        score += 12

    if bp == "Hypertension Stage 2":
        score += 35
    elif bp == "Hypertension Stage 1":
        score += 20
    elif bp == "Elevated":
        score += 10

    if v.get("heart_rate", 0) < 50 or v.get("heart_rate", 0) > 100:
        score += 10

    temp = v.get("temperature_f", v.get("temaperature_f", 98.6))
    if has_fever(temp):
        score += 10

    return min(score, 100)

def risk_label(score: int) -> str:
    """Determine the risk label based on the risk score."""
    if score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MODERATE"
    else:
        return "LOW"

if __name__ == "__main__":
    example_patient = {
        "ID": "PAT-1004-4821",
        "NAME": "Aarav Sharma",
        "DOB": "1990-05-14",
        "GENDER": "M",
        "BLOOD_GROUP": "O+",
        "ALLERGIES": {"penicillin", "dust"},
        "VITALS": {
            "height_cm": 175.0,
            "weight_kg": 82.0,
            "systolic": 128,
            "diastolic": 84,
            "heart_rate": 78,
            "temperature_f": 98.6,
        },
        "VISITS": [
            ("2026-06-10", "Routine checkup"),
            ("2026-07-02", "Fever"),
        ],
    }
    print(risk_label(risk_score(example_patient)))