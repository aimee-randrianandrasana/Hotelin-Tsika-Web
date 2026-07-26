from datetime import date, datetime
from models import employee as db
from config import SALAIRE_BASE, COEFF_GRADE
from utils.helpers import validate_employee_data, check_cin_unique
from config import DB_EMPLOYEE


def get_all_employees():
    return db.fetch_all()


def search_employees(text):
    return db.search(text)


def get_employee(emp_id):
    return db.fetch_by_id(emp_id)


def recruit_employee(data):
    errors = validate_employee_data(data)
    if errors:
        return False, errors

    cin = data.get("cin", "").strip()
    if not check_cin_unique(DB_EMPLOYEE, cin):
        return False, ["Ce CIN est deja utilise par un autre employe."]

    data["nom"] = data.get("nom", "").strip().upper()
    data["prenom"] = data.get("prenom", "").strip().capitalize()

    if not data.get("date_embauche"):
        data["date_embauche"] = date.today().isoformat()

    db.insert(data)
    return True, [f"Employe {data['nom']} recrute avec succes"]


def modify_grade(emp_id):
    emp = db.fetch_by_id(emp_id)
    if not emp:
        return False, ["Employe introuvable"]

    grade_order = ["Junior", "Intermediaire", "Senior", "Directeur"]
    current_idx = grade_order.index(emp["grade"]) if emp["grade"] in grade_order else 0
    if current_idx < len(grade_order) - 1:
        new_grade = grade_order[current_idx + 1]
    else:
        return False, ["Grade maximal atteint"]

    if new_grade == "Directeur":
        all_emps = db.fetch_all()
        for e in all_emps:
            if e["id"] != emp_id and e.get("grade") == "Directeur":
                return False, ["Un Directeur existe deja. Un seul Directeur est autorise."]

    poste = emp["poste"]
    new_salaire = int(SALAIRE_BASE.get(poste, 0) * COEFF_GRADE.get(new_grade, 1.0))

    emp["grade"] = new_grade
    emp["salaire_base"] = new_salaire
    db.update(emp_id, emp)
    return True, [f"Grade mis a jour : {new_grade}", f"Nouveau salaire : {new_salaire:,} Ar".replace(",", " ")]


def mark_absence(emp_id):
    emp = db.fetch_by_id(emp_id)
    if not emp:
        return False, ["Employe introuvable"]

    absences = emp.get("absences", 0) + 1
    salaire = emp["salaire_base"]
    if absences % 5 == 0:
        salaire = int(salaire * 0.85)

    emp["absences"] = absences
    emp["salaire_base"] = salaire
    db.update(emp_id, emp)
    return True, [f"{emp['nom']} {emp['prenom']} a maintenant {absences} absence(s)"]


def pay_salary(emp_id):
    emp = db.fetch_by_id(emp_id)
    if not emp:
        return False, ["Employe introuvable"], None

    salaire_base = emp["salaire_base"]
    absences = emp.get("absences", 0)

    today = date.today()
    date_embauche = emp.get("date_embauche")
    if isinstance(date_embauche, str):
        date_embauche = datetime.strptime(date_embauche, "%Y-%m-%d").date()

    nb_mois = (today.year - date_embauche.year) * 12 + (today.month - date_embauche.month)
    if nb_mois < 1:
        nb_mois = 1

    deduction_par_mois = int(salaire_base * 0.15 * (absences // 5))
    total_deduction = deduction_par_mois * nb_mois
    montant_total = salaire_base * nb_mois - total_deduction

    info = {
        "nom": f"{emp['prenom']} {emp['nom']}",
        "poste": emp["poste"],
        "grade": emp["grade"],
        "salaire_mensuel": salaire_base,
        "absences": absences,
        "total_deduction": total_deduction,
        "montant_total": montant_total,
        "nb_mois": nb_mois,
    }

    emp["absences"] = 0
    emp["last_paid"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.update(emp_id, emp)

    return True, [f"Paiement effectue : {montant_total:,} Ar pour {nb_mois} mois".replace(",", " ")], info


def fire_employee(emp_id):
    emp = db.fetch_by_id(emp_id)
    if not emp:
        return False, ["Employe introuvable"]
    db.delete(emp_id)
    return True, ["Employe supprime avec succes"]
