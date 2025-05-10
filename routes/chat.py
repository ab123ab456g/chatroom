from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_socketio import emit, join_room, leave_room, disconnect
from utils.extensions import socketio
from db.auth_event import get_user_by_id
from db.chat_event import (
    create_chatroom, get_chatroom_id_by_name,
    save_message, mark_online, mark_offline,
    get_messages_by_room_name, list_all_chatrooms
)

chat_bp = Blueprint('chat', __name__)

# ✅ 聊天室頁面
@chat_bp.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = get_user_by_id(session['user_id'])
    if not user:
        return redirect(url_for('auth.login'))

    return render_template('chat.html', username=user['username'])

# ✅ 使用者連線
@socketio.on('connect')
def handle_connect():
    sid = request.sid
    user_id = session.get('user_id')
    user = get_user_by_id(user_id)
    if user_id:
        mark_online(user_id, sid)
        emit('update', {'message': f'✅ 使用者 {user['username']} 上線'}, broadcast=True)
    else:
        disconnect()

# ✅ 處理訊息發送並儲存
@socketio.on('message')
def handle_message(data):
    user = data.get('user', '匿名')
    message = data.get('message', '')
    room = data.get('room')

    full_message = f"{user}: {message}"
    emit('message', full_message, room=room)

    chatroom_id = get_chatroom_id_by_name(room)
    sender_id = session.get('user_id')
    if chatroom_id and sender_id:
        save_message(chatroom_id, sender_id, message)

# ✅ 建立聊天室並寫入資料庫
@socketio.on('create_room')
def handle_create_room(data):
    room = data.get('room')
    user_id = session.get('user_id')

    if room and user_id:
        if create_chatroom(room, user_id):
            emit('update', {'message': f"✅ 已建立聊天室：{room}"}, broadcast=True)
        else:
            emit('update', {'message': f"⚠️ 聊天室 {room} 已存在"}, broadcast=True)

# ✅ 加入聊天室並載入歷史
@socketio.on('join')
def handle_join(data):
    room = data.get('room')
    username = data.get('user', '匿名')
    join_room(room)
    emit('update', {'message': f"👤 {username} 加入了 {room}"}, room=room)

# ✅ 離開聊天室
@socketio.on('leave')
def handle_leave(data):
    room = data.get('room')
    username = data.get('user', '匿名')
    leave_room(room)
    emit('update', {'message': f"👋 {username} 離開了 {room}"}, room=room)

# ✅ 載入歷史訊息
@socketio.on('load_history')
def handle_load_history(data):
    room = data.get('room')
    if not room:
        return

    messages = get_messages_by_room_name(room, limit=30)
    emit('load_history', {'messages': messages})

@socketio.on('list_rooms')
def handle_list_rooms():
    rooms = list_all_chatrooms()
    emit('room_list', {'rooms': rooms})
