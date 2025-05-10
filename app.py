from dotenv import load_dotenv
import os
from flask import Flask
from utils.extensions import socketio

# ✅ 載入 .env 檔案
load_dotenv()

# ✅ 建立 Flask 實例
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
socketio.init_app(app)

# ✅ 初始化資料庫（import 後直接執行）
from db.init_db import init_db
init_db()

# 🔁 載入 Blueprint
from routes.auth import auth_bp
app.register_blueprint(auth_bp)

from routes.chat import chat_bp
app.register_blueprint(chat_bp)


# ✅ 啟動伺服器
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True, port=8000)

