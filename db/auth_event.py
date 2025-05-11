from db.db_utils import get_db, hash_password, check_password
import sqlite3

def register_member(username, password):
    conn = get_db()
    cursor = conn.cursor()
    try:
        #hashed = hash_password(password)
        cursor.execute("INSERT INTO member (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True, "註冊成功"
    except sqlite3.IntegrityError:
        return False, "使用者名稱已存在"
    finally:
        conn.close()

def verify_login(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM member WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and password == row[1]:  # 直接比對 hash string
        return True, row[0]
    else:
        return False, None

    if row and check_password(password, row[1]):
        return True, row[0]
    else:
        return False, None

def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM member WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"id": row[0], "username": row[1]}
    return None
