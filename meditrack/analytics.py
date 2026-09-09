from meditrack import vitals, data
from functools import reduce

def high_risk_patients(patients, threshold=60):
    """Keep only patients whose risk score >= threshold."""
    return list(filter(lambda p: vitals.risk_score(p) >= threshold, patients))

def summarise(patients):
    """Transform each patient dict into a short summary dict."""
    return list(map(lambda p: {
        'id': p.get('ID') or p.get('id'),
        'name': p.get('NAME') or p.get('name'),
        'risk': vitals.risk_score(p),
        'label': vitals.risk_label(vitals.risk_score(p))
    }, patients))

def average_age(patients, calculate_age):
    """Average patient age using reduce to sum the ages."""
    if not patients:
        return 0
    ages = list(map(lambda p: calculate_age(p.get('DOB') or p.get('dob')), patients))
    total = reduce(lambda a, b: a + b, ages)
    return round(total / len(ages), 1)

def patient_stream(patients):
    """Generator function to yield patients one at a time."""
    for patient in patients:
        yield patient

def risk_report_lines(patients):
    """Generator function to yield a formatted string per patient."""
    for patient in patients:
        score = vitals.risk_score(patient)
        pid = patient.get('ID') or patient.get('id', '')
        name = patient.get('NAME') or patient.get('name', '')
        yield f"{pid:<16} {name:<16} risk={score:>3} ({vitals.risk_label(score)})"

def count_departments(node):
    """Recursively count every department in the hospital tree."""
    children = node.get('sub', node.get('departments', []))
    total = 0
    for child in children:
        total += 1 + count_departments(child)
    return total

def list_departments(node, depth=0, acc=None):
    """Recursively collect an indented department listing."""
    if acc is None:
        acc = []
    name = node.get("name", "")
    if name and depth > 0:
        acc.append(("  " * (depth - 1)) + "- " + name)
    for child in node.get("sub", node.get("departments", [])):
        list_departments(child, depth + 1, acc)
    return acc