from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection
from config import DB_USERS, ADMIN_USER, ADMIN_PASS

auth_bp = Blueprint("auth", __name__)


def ensure_admin():
    from db import ensure_tables
    ensure_tables()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT id FROM "{DB_USERS}" WHERE username=%s', (ADMIN_USER,))
    if not cur.fetchone():
        cur.execute(
            f'INSERT INTO "{DB_USERS}" (username, password_hash) VALUES (%s, %s)',
            (ADMIN_USER, generate_password_hash(ADMIN_PASS)),
        )
    cur.close()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f'SELECT id, password_hash FROM "{DB_USERS}" WHERE username=%s', (username,))
        row = cur.fetchone()
        cur.close()

        if row and check_password_hash(row[1], password):
            session["user_id"] = row[0]
            session["username"] = username
            flash("Connexion reussie", "success")
            return redirect(url_for("main.dashboard"))

        flash("Identifiants incorrects", "error")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
