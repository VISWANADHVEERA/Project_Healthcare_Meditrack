import random
import os
import sys

VALID_BLOOD_GROUPS = frozenset(
    {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}
)


def clean_name(raw_name: str) -> str:
    """ 
    Remove leading and trailing whitespace
    Collapse multiple internal spaces to a single space 
    convert to title case
    """
    return " ".join(raw_name.strip().split()).title()


def is_valid_blood_group(blood_group: str) -> bool:
    """
    Return True if given blood group{case-insensitive} is 
    in VALID_BLOOD_GROUPS else return False.
    """
    return blood_group.strip().upper() in VALID_BLOOD_GROUPS


import random
_ID_COUNTER_ = 1000

def generate_patient_id() -> str:
    """
    Generate a unique patient ID in the format 'PAT-{counter}-{suffix}'.
    """
    global _ID_COUNTER_
    suffix = random.randint(1000, 9999)
    id = f"PAT-{_ID_COUNTER_}-{suffix}"
    _ID_COUNTER_ += 1
    return id


from datetime import datetime, timedelta

def today_str() -> str:
    """
    Return today's date in the format 'YYYY-MM-DD'."""

    return datetime.now().strftime("%Y-%m-%d")

def clean_dob(dob: str) -> str:
    """
    Clean the date of birth string by removing leading/trailing whitespace.
    Validate the format to ensure it is in 'YYYY-MM-DD' format.
    """
    dob = dob.strip()
    try:
        datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date of birth format: {dob}. Expected 'YYYY-MM-DD'.")
    return dob

def calculate_age(dob: str) -> int:
    """
    Calculate age in years based on the date of birth string in 'YYYY-MM-DD' format.
    """
    dob = datetime.strptime(dob, "%Y-%m-%d")
    today = datetime.strptime(today_str(), "%Y-%m-%d")
    age = today.year - dob.year
    if ((today.month, today.day) < (dob.month, dob.day)):
        age -= 1
    return age    

#   `next_appointment_slots(start_hour=9, count=4, gap_minutes=30)` that `yield`s
#   formatted time strings (e.g. `"09:00 AM"`, `"09:30 AM"`, ...).

# Use `timedelta(minutes=gap_minutes * i)` inside a loop and
#   `strftime("%I:%M %p")`.

def next_appointment_slots(start_hour=9, count=4, gap_minutes=30):
    """GENERATOR of appointment time strings.

    Uses default parameters. Yields values lazily with `yield`"""
    base = datetime.now().replace(hour=start_hour, minute=0,
                                  second=0, microsecond=0)
    for i in range(count):
        slot = base + timedelta(minutes=gap_minutes * i)
        yield slot.strftime("%I:%M %p")


def clear_screen():
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")

def divider(title=""):
    line = "=" * 52          
    if title:
        return f"{line}\n  {title.upper()}\n{line}"
    return line


# ------------------------------------------------------------------ #
#  Presentation helpers (Class 07 strings, Class 13 functions)
# ------------------------------------------------------------------ #








# if __name__ == '__main__':
#     print(clean_name("   john   DOE "))
#     print(is_valid_blood_group('o-'))
#     print(generate_patient_id())
#     print(type(today_str()))
#     print(calculate_age('2000-08-04'))
#     print(clean_name("   john   DOE "))