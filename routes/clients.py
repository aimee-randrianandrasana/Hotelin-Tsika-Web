from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from services import client_service
import io
import csv

clients_bp = Blueprint("clients", __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@clients_bp.route("/clients")
@login_required
def list_clients():
    search = request.args.get("search", "").strip()
    if search:
        clients = client_service.search_clients(search)
    else:
        clients = client_service.get_all_clients()
    return render_template("clients.html", clients=clients, client=None)


@clients_bp.route("/clients/ajouter", methods=["POST"])
@login_required
def new_client():
    data = {
        "nom": request.form.get("nom", ""),
        "prenom": request.form.get("prenom", ""),
        "cin": request.form.get("cin", ""),
        "tel": request.form.get("tel", ""),
        "email": request.form.get("email", ""),
        "type_chambre": request.form.get("type_chambre", "classic"),
        "chambre": request.form.get("chambre", 1),
        "date_debut": request.form.get("date_debut", ""),
        "date_fin": request.form.get("date_fin", ""),
    }
    success, messages = client_service.add_client(data)
    for msg in messages:
        flash(msg, "success" if success else "error")
    if not success:
        clients = client_service.get_all_clients()
        return render_template("clients.html", clients=clients, client=data)
    return redirect(url_for("clients.list_clients"))


@clients_bp.route("/clients/modifier/<int:client_id>", methods=["POST"])
@login_required
def edit_client(client_id):
    data = {
        "nom": request.form.get("nom", ""),
        "prenom": request.form.get("prenom", ""),
        "cin": request.form.get("cin", ""),
        "tel": request.form.get("tel", ""),
        "email": request.form.get("email", ""),
        "type_chambre": request.form.get("type_chambre", "classic"),
        "chambre": request.form.get("chambre", 1),
        "date_debut": request.form.get("date_debut", ""),
        "date_fin": request.form.get("date_fin", ""),
    }
    success, messages = client_service.update_client(client_id, data)
    for msg in messages:
        flash(msg, "success" if success else "error")
    if not success:
        clients = client_service.get_all_clients()
        return render_template("clients.html", clients=clients, client=data)
    return redirect(url_for("clients.list_clients"))


@clients_bp.route("/clients/archiver/<int:client_id>", methods=["POST"])
@login_required
def archive_client(client_id):
    success, messages = client_service.archive_client(client_id)
    for msg in messages:
        flash(msg, "success" if success else "error")
    return redirect(url_for("clients.list_clients"))


@clients_bp.route("/clients/supprimer/<int:client_id>", methods=["POST"])
@login_required
def delete_client(client_id):
    success, messages = client_service.delete_client(client_id)
    for msg in messages:
        flash(msg, "success" if success else "error")
    return redirect(url_for("clients.list_clients"))


@clients_bp.route("/clients/vider", methods=["POST"])
@login_required
def delete_all():
    all_clients = client_service.get_all_clients()
    for c in all_clients:
        client_service.archive_client(c["id"])
    flash("Tous les clients supprimes et archives", "success")
    return redirect(url_for("clients.list_clients"))


@clients_bp.route("/clients/export")
@login_required
def export_csv():
    clients = client_service.get_all_clients()
    if not clients:
        flash("Aucune donnee a exporter", "info")
        return redirect(url_for("clients.list_clients"))
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=clients[0].keys())
    writer.writeheader()
    writer.writerows(clients)
    from flask import Response
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=clients.csv"},
    )


@clients_bp.route("/api/clients/search")
@login_required
def api_search():
    q = request.args.get("q", "").strip()
    if q:
        clients = client_service.search_clients(q)
    else:
        clients = client_service.get_all_clients()
    return jsonify(clients)
