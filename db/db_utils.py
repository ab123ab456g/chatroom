import sqlite3
import bcrypt

DB_PATH = "chat.db"

def get_db():
    return sqlite3.connect(DB_PATH)

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)
