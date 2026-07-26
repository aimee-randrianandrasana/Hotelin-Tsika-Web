from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services import client_service

archives_bp = Blueprint("archives", __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@archives_bp.route("/archives")
@login_required
def list_archives():
    search = request.args.get("search", "").strip()
    if search:
        archives = client_service.search_archives(search)
    else:
        archives = client_service.get_archives()
    return render_template("archives.html", archives=archives, search=search)


@archives_bp.route("/archives/vider", methods=["POST"])
@login_required
def clear_archives():
    success, messages = client_service.clear_archives()
    for msg in messages:
        flash(msg, "success" if success else "error")
    return redirect(url_for("archives.list_archives"))
