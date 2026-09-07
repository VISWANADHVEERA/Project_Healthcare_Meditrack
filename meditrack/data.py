patients = [
    {
        "ID": "PAT-1000-1234",
        "NAME": "John Doe",
        "DOB": "1990-01-01",
        "AGE": 36,
        "GENDER": "M",
        "BLOOD_GROUP": "A+",
        "ALLERGIES": {"balloons", "peanuts"},
        "VITALS": {"height_cm":164,
                   "weight_kg": 75,
                   "heart_rate": 72,
                   "systolic": 128,
                   "diastolic": 84,
                   "temaperature_f": 96.6},
        "VISITS": [
            ("2026-06-11", "Annual Checkup"),("2026-07-16", "cold and cough, fever")
        ],                   
    },

    {
        "ID": "PAT-1001-5678",
        "NAME": "Samuel Joy",
        "DOB": "2002-12-12",
        "AGE": 23,
        "GENDER": "M",
        "BLOOD_GROUP": "O-",
        "ALLERGIES": {"dust", "pollen"},
        "VITALS": {"height_cm": 155,
                   "weight_kg": 65,
                   "heart_rate": 80,
                   "systolic": 120,
                   "diastolic": 80,
                   "temperature_f": 98.6},
        "VISITS": [
            ("2026-06-13", "throat infection"), ("2026-07-16", "right leg wound")
        ],
    },

    {
        "ID": "PAT-1002-9012",
        "NAME": "K. Ram Kumar",
        "DOB": "2000-01-24",
        "AGE": 26,
        "GENDER": "M",
        "BLOOD_GROUP": "B+",
        "ALLERGIES": {"dust"},
        "VITALS": {"height_cm": 168,
                   "weight_kg": 77,
                   "heart_rate": 75,
                   "systolic": 130,
                   "diastolic": 85,
                   "temperature_f": 97.3},
        "VISITS": [
                   ("2026-06-23", "Annual Checkup"), ("2006-08-11", "fever and headache")
                   ],

    }
]


#add a **nested** `HOSPITAL` dict: a name plus a
#`departments` list, where each department can have its own `sub` list of
# departments

HOSPITAL = {
    "name": "MediTrack General Hospital",
    "departments": [
        {
            "name": "Internal Medicine",
            "sub": [
                {"name": "Cardiology", "sub": []},
                {"name": "Endocrinology", "sub": []},
            ],
        },
        {
            "name": "Surgery",
            "sub": [
                {"name": "Orthopedics", "sub": []},
                {
                    "name": "Neurosurgery",
                    "sub": [{"name": "Spine Unit", "sub": []}],
                },
            ],
        },
        {"name": "Pediatrics", "sub": []},
    ],
}