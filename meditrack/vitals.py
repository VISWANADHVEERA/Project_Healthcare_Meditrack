def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """
    Calculate BMI(Body Mass Index) using the formula: BMI = weight(kg) / height(m)^2"""
    height_m = height_cm / 100
    if height_cm <= 0 or weight_kg <= 0:
        return 0
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

def bmi_category(bmi: float) -> str:
    """
    Determine the bmi category based on the BMI value."""
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
    """
    Determine the blood pressure category based on systolic and diastolic values."""
    if systolic < 120 and diastolic < 80:
        return "Normal"
    if systolic < 130 and diastolic < 80:
        return "Elevated"
    if systolic < 140 or diastolic < 90:
        return "Hypertension Stage 1"
    return "Hypertension Stage 2"

def has_fever(temperature_f: float) -> bool:
    """
    Determine if the patient has a fever based on temperature in Fahrenheit.
    Fever is typically defined as a body temperature of 100.4°F (38°C) or higher.
    """
    return temperature_f >= 100.4


def risk_score(patient: dict) -> int:
    vitals = patient.get("VITALS", {})
    score = 0

    #BMI RISK
    bmi = calculate_bmi(vitals.get("weight_kg", 0), vitals.get("height_cm", 0))

    #bp RISK
    bp = bp_category(vitals.get("systolic", 0), vitals.get("diastolic", 0))

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
    if vitals.get("heart_rate", 0) < 50 or vitals.get("heart_rate", 0) > 100:
        score += 10
    if has_fever(vitals.get("temperature_f", 0)):
        score += 10
    return min((score, 100))

def risk_label(score: int) -> str:
    """
    Determine the risk label based on the risk score."""
    if score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MODERATE"
    else:
        return "LOW"

if __name__ == "__main__":
    # Example usage
     patient = {
            "id": "PAT-1004-4821",
            "name": "Aarav Sharma",
            "dob": "1990-05-14",
            "gender": "M",
            "blood_group": "O+",
            "allergies": {"penicillin", "dust"},          # set
            "vitals": {                                    # nested dict
                "height_cm": 175.0,
                "weight_kg": 82.0,
                "systolic": 128,
                "diastolic": 84,
                "heart_rate": 78,
                "temperature_c": 37.0,
            },
            "visits": [                                    # list of tuples
                ("2026-06-10", "Routine checkup"),
                ("2026-07-02", "Fever"),
            ],
        }


print(risk_label(risk_score(patient)))