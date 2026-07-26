from datetime import date, timedelta
from db import get_connection
from models import client as client_model, employee as employee_model
from config import PRIX_CHAMBRE

SAMPLE_CLIENTS = [
    {"nom": "RAKOTO", "prenom": "Andry", "cin": "101010101010", "tel": "0341234567", "email": "andry@gmail.com", "type_chambre": "vip", "chambre": 3, "date_debut": "2026-08-01", "date_fin": "2026-08-05"},
    {"nom": "RABE", "prenom": "Harena", "cin": "202020202020", "tel": "0339876543", "email": "harena@gmail.com", "type_chambre": "classic", "chambre": 12, "date_debut": "2026-08-02", "date_fin": "2026-08-06"},
    {"nom": "RAZAFY", "prenom": "Fanja", "cin": "303030303030", "tel": "0324567890", "email": "fanja@gmail.com", "type_chambre": "vip", "chambre": 7, "date_debut": "2026-08-03", "date_fin": "2026-08-07"},
    {"nom": "ANDRIAMANARIVO", "prenom": "Tovo", "cin": "404040404040", "tel": "0345678901", "email": "tovo@gmail.com", "type_chambre": "classic", "chambre": 25, "date_debut": "2026-08-01", "date_fin": "2026-08-04"},
    {"nom": "RAHARISON", "prenom": "Mija", "cin": "505050505050", "tel": "0331112233", "email": "mija@gmail.com", "type_chambre": "classic", "chambre": 8, "date_debut": "2026-08-05", "date_fin": "2026-08-10"},
]

SAMPLE_EMPLOYEES = [
    {"nom": "RAJAOHNINA", "prenom": "Soa", "cin": "606060606060", "tel": "0342223344", "poste": "Receptionniste", "grade": "Intermediaire", "date_embauche": "2024-06-15"},
    {"nom": "HERILALA", "prenom": "Tojo", "cin": "707070707070", "tel": "0333334455", "poste": "Serveur", "grade": "Junior", "date_embauche": "2025-01-10"},
    {"nom": "RATSIMANDRESY", "prenom": "Lova", "cin": "808080808080", "tel": "0324445566", "poste": "Cuisinier", "grade": "Senior", "date_embauche": "2023-03-20"},
    {"nom": "FANEVA", "prenom": "Hery", "cin": "909090909090", "tel": "0345556677", "poste": "Directeur", "grade": "Directeur", "date_embauche": "2022-01-01"},
    {"nom": "MANDIMBISON", "prenom": "Rija", "cin": "111111111111", "tel": "0336667788", "poste": "Maintenance", "grade": "Junior", "date_embauche": "2025-06-01"},
]


def seed_data():
    clients = client_model.fetch_all()
    if len(clients) >= len(SAMPLE_CLIENTS):
        return

    today = date.today()

    for data in SAMPLE_CLIENTS:
        d1 = date.fromisoformat(data["date_debut"])
        d2 = date.fromisoformat(data["date_fin"])
        nb_nuits = (d2 - d1).days
        prix_nuit = PRIX_CHAMBRE.get(data["type_chambre"], 12_000)
        client_model.insert({
            "nom": data["nom"],
            "prenom": data["prenom"],
            "cin": data["cin"],
            "tel": data["tel"],
            "email": data["email"],
            "type_chambre": data["type_chambre"],
            "chambre": data["chambre"],
            "date_debut": data["date_debut"],
            "date_fin": data["date_fin"],
            "prix_total": nb_nuits * prix_nuit,
        })

    for data in SAMPLE_EMPLOYEES:
        employee_model.insert(data)
