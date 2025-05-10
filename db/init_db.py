
import sqlite3

def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    # 建立會員表
    c.execute("""
    CREATE TABLE IF NOT EXISTS member (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 建立聊天室表
    c.execute("""
    CREATE TABLE IF NOT EXISTS chatroom (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        owner_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_id) REFERENCES member(id)
    )
    """)

    # 建立訊息表
    c.execute("""
    CREATE TABLE IF NOT EXISTS message (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chatroom_id INTEGER NOT NULL,
        sender_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chatroom_id) REFERENCES chatroom(id),
        FOREIGN KEY (sender_id) REFERENCES member(id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS online_member (
        member_id INTEGER PRIMARY KEY,
        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        socket_id TEXT,
        chatroom_id INTEGER,
        FOREIGN KEY (member_id) REFERENCES member(id),
        FOREIGN KEY (chatroom_id) REFERENCES chatroom(id)
    )
    """)

    conn.commit()
    conn.close()


