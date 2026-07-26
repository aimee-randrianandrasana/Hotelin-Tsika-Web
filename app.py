from flask import Flask, redirect, url_for, session, render_template
from flask import Blueprint
from config import SECRET_KEY
from db import ensure_tables
from routes.auth import auth_bp, ensure_admin
from seed import seed_data
from routes.clients import clients_bp
from routes.employees import employees_bp
from routes.archives import archives_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(archives_bp)

main_bp = Blueprint("main", __name__)


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return redirect(url_for("main.dashboard"))


@main_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from models import client as client_model
    from models import employee as employee_model

    clients = client_model.fetch_all()
    archives = client_model.fetch_all(table="clients_archive")
    employees = employee_model.fetch_all()

    total_recette = sum(c.get("prix_total", 0) for c in clients)

    return render_template(
        "dashboard.html",
        nb_clients=len(clients),
        nb_archives=len(archives),
        nb_employees=len(employees),
        total_recette=total_recette,
    )


app.register_blueprint(main_bp)


with app.app_context():
    ensure_tables()
    ensure_admin()
    seed_data()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
