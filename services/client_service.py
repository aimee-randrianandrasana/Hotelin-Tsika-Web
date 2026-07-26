from datetime import datetime, date
from models import client as db
from config import PRIX_CHAMBRE
from utils.helpers import validate_client_data, check_cin_unique
from config import DB_CLIENT


def auto_archive_finished():
    today = date.today()
    clients = db.fetch_all()
    archived_count = 0
    for c in clients:
        if c["date_fin"] and c["date_fin"] < today:
            db.insert_archive(c)
            db.delete(c["id"])
            archived_count += 1
    return archived_count


def get_all_clients():
    auto_archive_finished()
    return db.fetch_all()


def search_clients(text):
    return db.search(text)


def get_client(client_id):
    return db.fetch_by_id(client_id)


def add_client(data):
    errors = validate_client_data(data)
    if errors:
        return False, errors

    cin = data.get("cin", "").strip()
    if not check_cin_unique(DB_CLIENT, cin):
        return False, ["Ce CIN est deja utilise par un autre client."]

    data["nom"] = data.get("nom", "").strip().upper()
    data["prenom"] = data.get("prenom", "").strip().capitalize()

    date_debut = data.get("date_debut")
    date_fin = data.get("date_fin")
    if not date_debut or not date_fin:
        return False, ["Les dates de debut et fin sont obligatoires"]

    type_chambre = data.get("type_chambre", "classic").lower()
    prix_nuit = PRIX_CHAMBRE.get(type_chambre, 12_000)

    d1 = datetime.strptime(date_debut, "%Y-%m-%d").date()
    d2 = datetime.strptime(date_fin, "%Y-%m-%d").date()
    nb_nuits = (d2 - d1).days
    if nb_nuits <= 0:
        return False, ["La date de fin doit etre apres la date de debut"]

    data["prix_total"] = nb_nuits * prix_nuit
    data["type_chambre"] = type_chambre

    chambre = int(data.get("chambre", 1))
    if db.check_room_conflict(chambre, type_chambre, date_debut, date_fin):
        disponible = db.find_available_room(type_chambre, date_debut, date_fin)
        if disponible:
            data["chambre"] = disponible
        else:
            return False, [f"Toutes les chambres {type_chambre} sont occupees !"]

    db.insert(data)
    return True, ["Client ajoute avec succes"]


def update_client(client_id, data):
    errors = validate_client_data(data)
    if errors:
        return False, errors

    cin = data.get("cin", "").strip()
    if not check_cin_unique(DB_CLIENT, cin, exclude_id=client_id):
        return False, ["Ce CIN est deja utilise par un autre client."]

    data["nom"] = data.get("nom", "").strip().upper()
    data["prenom"] = data.get("prenom", "").strip().capitalize()

    date_debut = data.get("date_debut")
    date_fin = data.get("date_fin")
    if not date_debut or not date_fin:
        return False, ["Les dates de debut et fin sont obligatoires"]

    type_chambre = data.get("type_chambre", "classic").lower()
    prix_nuit = PRIX_CHAMBRE.get(type_chambre, 12_000)

    d1 = datetime.strptime(date_debut, "%Y-%m-%d").date()
    d2 = datetime.strptime(date_fin, "%Y-%m-%d").date()
    nb_nuits = (d2 - d1).days
    if nb_nuits <= 0:
        return False, ["La date de fin doit etre apres la date de debut"]

    data["prix_total"] = nb_nuits * prix_nuit
    data["type_chambre"] = type_chambre

    chambre = int(data.get("chambre", 1))
    if db.check_room_conflict(chambre, type_chambre, date_debut, date_fin, exclude_id=client_id):
        disponible = db.find_available_room(type_chambre, date_debut, date_fin)
        if disponible:
            data["chambre"] = disponible
        else:
            return False, [f"Toutes les chambres {type_chambre} sont occupees pour cette periode !"]

    db.update(client_id, data)
    return True, ["Client mis a jour avec succes"]


def archive_client(client_id):
    client = db.fetch_by_id(client_id)
    if not client:
        return False, ["Client introuvable"]
    db.insert_archive(client)
    db.delete(client_id)
    return True, ["Client archive avec succes"]


def delete_client(client_id):
    db.delete(client_id)
    return True, ["Client supprime avec succes"]


def delete_all_clients():
    all_clients = db.fetch_all()
    for client in all_clients:
        db.insert_archive(client)
    db.delete_all()
    return True, ["Tous les clients supprimes et archives"]


def get_archives():
    return db.fetch_all(table="clients_archive")


def search_archives(text):
    return db.search(text, table="clients_archive")


def clear_archives():
    db.delete_all_history()
    return True, ["Historique vide"]
