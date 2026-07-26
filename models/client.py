from db import get_connection
from config import DB_CLIENT, DB_ARCHIVE

CLIENT_KEYS = [
    "id", "nom", "prenom", "cin", "tel", "email",
    "type_chambre", "chambre", "date_debut", "date_fin", "prix_total",
]

ARCHIVE_KEYS = [
    "id", "nom", "prenom", "cin", "tel", "email",
    "type_chambre", "chambre", "date_debut", "date_fin", "prix_total", "archived_at",
]


def fetch_all(table=DB_CLIENT):
    keys = ARCHIVE_KEYS if table == DB_ARCHIVE else CLIENT_KEYS
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM "{table}" ORDER BY id')
    rows = cur.fetchall()
    cur.close()
    return [dict(zip(keys, row)) for row in rows]


def search(text, table=DB_CLIENT):
    keys = ARCHIVE_KEYS if table == DB_ARCHIVE else CLIENT_KEYS
    conn = get_connection()
    cur = conn.cursor()
    pattern = f"%{text}%"
    cur.execute(
        f"""SELECT * FROM "{table}" WHERE
            nom LIKE %s OR prenom LIKE %s OR cin LIKE %s OR
            tel LIKE %s OR email LIKE %s OR type_chambre LIKE %s
            ORDER BY id""",
        (pattern, pattern, pattern, pattern, pattern, pattern),
    )
    rows = cur.fetchall()
    cur.close()
    return [dict(zip(keys, row)) for row in rows]


def fetch_by_id(client_id, table=DB_CLIENT):
    keys = ARCHIVE_KEYS if table == DB_ARCHIVE else CLIENT_KEYS
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM "{table}" WHERE id=%s', (client_id,))
    row = cur.fetchone()
    cur.close()
    if not row:
        return None
    return dict(zip(keys, row))


def insert(data):
    conn = get_connection()
    cur = conn.cursor()
    sql = f"""INSERT INTO "{DB_CLIENT}"
        (nom, prenom, cin, tel, email, type_chambre, chambre, date_debut, date_fin, prix_total)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(sql, (
        data["nom"], data["prenom"], data["cin"], data["tel"],
        data.get("email", ""), data["type_chambre"], data["chambre"],
        data["date_debut"], data["date_fin"], data["prix_total"],
    ))
    cur.close()


def update(client_id, data):
    conn = get_connection()
    cur = conn.cursor()
    sql = f"""UPDATE "{DB_CLIENT}" SET
        nom=%s, prenom=%s, cin=%s, tel=%s, email=%s,
        type_chambre=%s, chambre=%s, date_debut=%s, date_fin=%s, prix_total=%s
        WHERE id=%s"""
    cur.execute(sql, (
        data["nom"], data["prenom"], data["cin"], data["tel"],
        data.get("email", ""), data["type_chambre"], data["chambre"],
        data["date_debut"], data["date_fin"], data["prix_total"], client_id,
    ))
    cur.close()


def delete(client_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f'DELETE FROM "{DB_CLIENT}" WHERE id=%s', (client_id,))
    cur.close()


def delete_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f'TRUNCATE TABLE "{DB_CLIENT}" RESTART IDENTITY CASCADE')
    cur.close()


def insert_archive(data):
    conn = get_connection()
    cur = conn.cursor()
    sql = f"""INSERT INTO "{DB_ARCHIVE}"
        (nom, prenom, cin, tel, email, type_chambre, chambre, date_debut, date_fin, prix_total)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(sql, (
        data.get("nom", ""), data.get("prenom", ""), data.get("cin", ""),
        data.get("tel", ""), data.get("email", ""), data.get("type_chambre", "classic"),
        data.get("chambre", 1), data.get("date_debut"), data.get("date_fin"),
        data.get("prix_total", 0),
    ))
    cur.close()


def delete_all_history():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f'TRUNCATE TABLE "{DB_ARCHIVE}" RESTART IDENTITY CASCADE')
    cur.close()


def check_room_conflict(chambre, type_chambre, date_debut, date_fin, exclude_id=None):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT * FROM clients
        WHERE chambre = %s AND type_chambre = %s
        AND (date_debut <= %s AND date_fin >= %s)
    """
    params = [chambre, type_chambre, date_fin, date_debut]
    if exclude_id:
        query += " AND id != %s"
        params.append(exclude_id)
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    return len(result) > 0


def find_available_room(type_chambre, date_debut, date_fin):
    conn = get_connection()
    cur = conn.cursor()
    room_range = range(1, 21) if type_chambre.lower() == "vip" else range(1, 51)
    for ch in room_range:
        cur.execute("""
            SELECT * FROM clients
            WHERE chambre = %s AND type_chambre = %s
            AND (date_debut <= %s AND date_fin >= %s)
        """, (ch, type_chambre, date_fin, date_debut))
        if not cur.fetchall():
            cur.close()
            return ch
    cur.close()
    return None
