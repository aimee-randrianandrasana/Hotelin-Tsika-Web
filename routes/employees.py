from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from services import employee_service
from config import SALAIRE_BASE, COEFF_GRADE

employees_bp = Blueprint("employees", __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@employees_bp.route("/personnel")
@login_required
def list_employees():
    search = request.args.get("search", "").strip()
    if search:
        employees = employee_service.search_employees(search)
    else:
        employees = employee_service.get_all_employees()
    return render_template("employees.html", employees=employees, search=search)


@employees_bp.route("/personnel/ajouter", methods=["GET", "POST"])
@login_required
def new_employee():
    if request.method == "POST":
        data = {
            "nom": request.form.get("nom", ""),
            "prenom": request.form.get("prenom", ""),
            "cin": request.form.get("cin", ""),
            "tel": request.form.get("tel", ""),
            "poste": request.form.get("poste", "Receptionniste"),
            "grade": request.form.get("grade", "Junior"),
            "date_embauche": request.form.get("date_embauche", ""),
        }
        success, messages = employee_service.recruit_employee(data)
        for msg in messages:
            flash(msg, "success" if success else "error")
        if not success:
            employees = employee_service.get_all_employees()
            return render_template("employees.html", employees=employees, employee=data, search="")
        return redirect(url_for("employees.list_employees"))
    return render_template("employee_form.html", employee=None)


@employees_bp.route("/personnel/modifier/<int:emp_id>", methods=["GET", "POST"])
@login_required
def edit_employee(emp_id):
    if request.method == "POST":
        emp = employee_service.get_employee(emp_id)
        if not emp:
            flash("Employe introuvable", "error")
            return redirect(url_for("employees.list_employees"))
        data = {
            "nom": request.form.get("nom", emp["nom"]),
            "prenom": request.form.get("prenom", emp["prenom"]),
            "cin": request.form.get("cin", emp["cin"]),
            "tel": request.form.get("tel", emp["tel"]),
            "poste": request.form.get("poste", emp["poste"]),
            "grade": request.form.get("grade", emp["grade"]),
            "salaire_base": emp["salaire_base"],
            "absences": emp["absences"],
            "date_embauche": emp["date_embauche"],
        }
        from models import employee as emp_db
        emp_db.update(emp_id, data)
        flash("Employe mis a jour", "success")
        return redirect(url_for("employees.list_employees"))
    emp = employee_service.get_employee(emp_id)
    if not emp:
        flash("Employe introuvable", "error")
        return redirect(url_for("employees.list_employees"))
    return render_template("employee_form.html", employee=emp)


@employees_bp.route("/personnel/promouvoir/<int:emp_id>", methods=["POST"])
@login_required
def promote_employee(emp_id):
    success, messages = employee_service.modify_grade(emp_id)
    for msg in messages:
        flash(msg, "success" if success else "error")
    return redirect(url_for("employees.list_employees"))


@employees_bp.route("/personnel/absence/<int:emp_id>", methods=["POST"])
@login_required
def absence_employee(emp_id):
    success, messages = employee_service.mark_absence(emp_id)
    for msg in messages:
        flash(msg, "success" if success else "error")
    return redirect(url_for("employees.list_employees"))


@employees_bp.route("/personnel/payer/<int:emp_id>", methods=["POST"])
@login_required
def pay_employee(emp_id):
    success, messages, info = employee_service.pay_salary(emp_id)
    for msg in messages:
        flash(msg, "success" if success else "error")
    return redirect(url_for("employees.list_employees"))


@employees_bp.route("/personnel/renvoyer/<int:emp_id>", methods=["POST"])
@login_required
def fire_employee(emp_id):
    success, messages = employee_service.fire_employee(emp_id)
    for msg in messages:
        flash(msg, "success" if success else "error")
    return redirect(url_for("employees.list_employees"))


@employees_bp.route("/api/employees/search")
@login_required
def api_search():
    q = request.args.get("q", "").strip()
    if q:
        employees = employee_service.search_employees(q)
    else:
        employees = employee_service.get_all_employees()
    return jsonify(employees)
