from db.db_utils import get_db
import sqlite3
from datetime import datetime

# === 聊天室功能 ===

def create_chatroom(name, owner_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO chatroom (name, owner_id) VALUES (?, ?)", (name, owner_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_chatroom_id_by_name(name):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM chatroom WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# === 訊息儲存 ===

def save_message(chatroom_id, sender_id, content):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO message (chatroom_id, sender_id, content) VALUES (?, ?, ?)",
        (chatroom_id, sender_id, content)
    )
    conn.commit()
    conn.close()

# === 線上狀態管理 ===

def mark_online(member_id, socket_id, chatroom_id=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO online_member (member_id, socket_id, chatroom_id, last_active)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    """, (member_id, socket_id, chatroom_id))
    conn.commit()
    conn.close()

def mark_offline(member_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM online_member WHERE member_id = ?", (member_id,))
    conn.commit()
    conn.close()

def get_messages_by_room_name(room_name, limit=30):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.username, msg.content, msg.sent_at
        FROM message msg
        JOIN member m ON msg.sender_id = m.id
        JOIN chatroom c ON msg.chatroom_id = c.id
        WHERE c.name = ?
        ORDER BY msg.sent_at DESC
        LIMIT ?
    """, (room_name, limit))
    rows = cursor.fetchall()
    conn.close()

    return [
        f"[{sent_at}] {username}: {content}"
        for username, content, sent_at in reversed(rows)
    ]

def list_all_chatrooms():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM chatroom ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
