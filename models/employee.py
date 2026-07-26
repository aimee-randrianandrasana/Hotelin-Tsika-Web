from db import get_connection
from config import DB_EMPLOYEE, SALAIRE_BASE, COEFF_GRADE

TABLE_KEYS = [
    "id", "nom", "prenom", "cin", "tel", "poste",
    "grade", "salaire_base", "absences", "date_embauche", "last_paid",
]


def fetch_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM "{DB_EMPLOYEE}" ORDER BY id')
    rows = cur.fetchall()
    cur.close()
    return [dict(zip(TABLE_KEYS, row)) for row in rows]


def search(text):
    conn = get_connection()
    cur = conn.cursor()
    pattern = f"%{text}%"
    cur.execute(
        f"""SELECT * FROM "{DB_EMPLOYEE}" WHERE
            nom LIKE %s OR prenom LIKE %s OR cin LIKE %s OR
            poste LIKE %s OR grade LIKE %s OR tel LIKE %s
            ORDER BY id""",
        (pattern, pattern, pattern, pattern, pattern, pattern),
    )
    rows = cur.fetchall()
    cur.close()
    return [dict(zip(TABLE_KEYS, row)) for row in rows]


def fetch_by_id(emp_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM "{DB_EMPLOYEE}" WHERE id=%s', (emp_id,))
    row = cur.fetchone()
    cur.close()
    if not row:
        return None
    return dict(zip(TABLE_KEYS, row))


def insert(data):
    conn = get_connection()
    cur = conn.cursor()
    poste = data.get("poste", "Receptionniste")
    grade = data.get("grade", "Junior")
    salaire = int(SALAIRE_BASE.get(poste, 0) * COEFF_GRADE.get(grade, 1.0))
    sql = f"""
        INSERT INTO "{DB_EMPLOYEE}"
        (nom, prenom, cin, tel, poste, grade, salaire_base, absences, date_embauche, last_paid)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cur.execute(sql, (
        data["nom"], data["prenom"], data["cin"],
        data.get("tel", ""), poste, grade, salaire,
        data.get("absences", 0), data.get("date_embauche"),
        data.get("last_paid"),
    ))
    cur.close()


def update(emp_id, data):
    conn = get_connection()
    cur = conn.cursor()
    sql = f"""
        UPDATE "{DB_EMPLOYEE}" SET
        nom=%s, prenom=%s, cin=%s, tel=%s, poste=%s,
        grade=%s, salaire_base=%s, absences=%s, date_embauche=%s, last_paid=%s
        WHERE id=%s
    """
    cur.execute(sql, (
        data["nom"], data["prenom"], data["cin"],
        data.get("tel", ""), data["poste"], data.get("grade", "Junior"),
        data.get("salaire_base", 0), data.get("absences", 0),
        data.get("date_embauche"), data.get("last_paid"), emp_id,
    ))
    cur.close()


def delete(emp_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f'DELETE FROM "{DB_EMPLOYEE}" WHERE id=%s', (emp_id,))
    cur.close()
