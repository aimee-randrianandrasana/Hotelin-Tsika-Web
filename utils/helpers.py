import re
from datetime import date


def validate_client_data(data):
    errors = []
    if not data.get("prenom") or not data.get("cin"):
        errors.append("Le prenom et le CIN sont obligatoires.")

    cin = str(data.get("cin", ""))
    if cin and not (cin.isdigit() and len(cin) == 12):
        errors.append("Le CIN doit contenir exactement 12 chiffres.")

    tel = str(data.get("tel", ""))
    if tel and not (tel.isdigit() and len(tel) == 10):
        errors.append("Le telephone doit contenir exactement 10 chiffres.")

    email = data.get("email", "").strip()
    if email:
        email_regex = r"^[\w.+-]+@[\w.-]+\.\w+$"
        if not re.match(email_regex, email):
            errors.append("Adresse email invalide.")

    type_chambre = data.get("type_chambre", "classic").lower()
    chambre = data.get("chambre", 1)
    try:
        chambre = int(chambre)
    except (ValueError, TypeError):
        chambre = 1
    if type_chambre == "vip" and not (1 <= chambre <= 20):
        errors.append("Une chambre VIP doit etre entre 1 et 20.")
    elif type_chambre == "classic" and not (1 <= chambre <= 50):
        errors.append("Une chambre Classic doit etre entre 1 et 50.")

    date_debut = data.get("date_debut", "")
    date_fin = data.get("date_fin", "")
    if date_debut and date_fin:
        try:
            d1 = date.fromisoformat(date_debut)
            d2 = date.fromisoformat(date_fin)
            if d1 < date.today():
                errors.append("La date de debut ne peut pas etre dans le passe.")
            if d2 <= d1:
                errors.append("La date de fin doit etre apres la date de debut.")
        except ValueError:
            errors.append("Format de date invalide.")

    return errors


def validate_employee_data(data):
    errors = []
    if not data.get("prenom") or not data.get("cin"):
        errors.append("Le prenom et le CIN sont obligatoires.")

    cin = str(data.get("cin", ""))
    if cin and not (cin.isdigit() and len(cin) == 12):
        errors.append("Le CIN doit contenir exactement 12 chiffres.")

    tel = str(data.get("tel", ""))
    if tel and not (tel.isdigit() and len(tel) == 10):
        errors.append("Le telephone doit contenir exactement 10 chiffres.")

    email = data.get("email", "").strip()
    if email:
        email_regex = r"^[\w.+-]+@[\w.-]+\.\w+$"
        if not re.match(email_regex, email):
            errors.append("Adresse email invalide.")

    return errors


def check_cin_unique(table, cin, exclude_id=None):
    from db import get_connection
    conn = get_connection()
    cur = conn.cursor()
    query = f'SELECT id FROM "{table}" WHERE cin = %s'
    params = [cin]
    if exclude_id:
        query += " AND id != %s"
        params.append(exclude_id)
    cur.execute(query, params)
    result = cur.fetchone()
    cur.close()
    return result is None


def format_currency(amount):
    return f"{amount:,} Ar".replace(",", " ")


def days_between(date1, date2):
    from datetime import datetime
    if isinstance(date1, str):
        date1 = datetime.strptime(date1, "%Y-%m-%d").date()
    if isinstance(date2, str):
        date2 = datetime.strptime(date2, "%Y-%m-%d").date()
    return abs((date2 - date1).days)
