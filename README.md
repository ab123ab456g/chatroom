這裡是根據你已完成的聊天室系統，自動整理出來的一份專業又易讀的 `README.md`，適用於 GitHub 開源、履歷作品集、或課堂報告用：

---

## 📦 Chatroom System with Flask & Socket.IO

一個基於 Python Flask + Flask-SocketIO 打造的即時聊天室，支援使用者註冊、登入、建立聊天室、訊息廣播、歷史訊息載入，以及區域網路多裝置同步。

---

### 🖼️ 功能特色

* ✅ 使用者註冊 / 登入 / 登出
* ✅ 建立與加入聊天室（多房間）
* ✅ 即時訊息廣播（Socket.IO）
* ✅ 訊息儲存與歷史載入
* ✅ 線上使用者追蹤
* ✅ 支援區域網路連線（內網多人）
* ✅ 前端聊天室選單 / 動態更新

---

### 🧱 技術架構

| 類別         | 使用技術                         |
| ---------- | ---------------------------- |
| 語言         | Python 3.x                   |
| 後端         | Flask, Flask-SocketIO        |
| 資料庫        | SQLite                       |
| 前端         | HTML + JavaScript            |
| 實時通訊       | Socket.IO (v4)               |
| Session 管理 | Flask Session (Cookie-based) |

---

### 🚀 如何啟動

#### ✅ 安裝依賴

```bash
pip install -r requirements.txt
```

#### ✅ 初始化資料庫

```bash
python init_db.py
```

#### ✅ 啟動伺服器

```bash
python app.py
```

> 伺服器將在 `http://localhost:8000` 運作，區網內其他裝置可透過你本機 IP 存取。

---

### 📁 專案結構

```
chatroom/
├── app.py                  # 主 Flask 應用
├── db/
│   ├── init_db.py          # 資料表初始化
│   ├── db_utils.py         # DB 與 hash 工具
│   ├── auth_event.py       # 使用者操作邏輯
│   └── chat_event.py       # 聊天室操作邏輯
├── routes/
│   ├── auth.py             # 使用者登入註冊邏輯
│   └── chat.py             # SocketIO 聊天功能處理
├── templates/
│   ├── login.html
│   ├── register.html
│   └── chat.html
├── utils/
│   └── extensions.py       # SocketIO 延遲初始化
├── static/                 #（如有 CSS / JS 檔）
└── requirements.txt
```

---

### 🧪 開發者筆記

* 使用 SQLite 作為輕量型資料儲存
* 使用 Cookie-based session，請保留 `.env` 中的 `SECRET_KEY`
* 已測試於區域網路內多台設備同步運作

---

### 📌 Todo / 延伸功能（可持續開發）

* [ ] 支援聊天室人數統計與上線名單
* [ ] 私訊 / 對話加密
* [ ] 附件、圖片訊息支援
* [ ] WebSocket 壓力測試與效能調校
* [ ] 容器化部署（Docker）

---

### 🧑‍💻 作者與貢獻者

> 本專案由 {{ab123ab456g@gmail.com}} 於 {{2025年5月}} 設計與完成。
> 歡迎 fork 與發 issue 提出建議！

---
