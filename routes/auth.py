from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from db.auth_event import register_member, verify_login, get_user_by_id

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    data = request.form
    username = data.get('username')
    password = data.get('password')
    success, msg = register_member(username, password)
    if success:
        return redirect(url_for('auth.login'))
    return msg, 409

@auth_bp.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = request.form
    username = data.get('username')
    password = data.get('password')
    success, user_id = verify_login(username, password)
    if success:
        session['user_id'] = user_id
        return redirect('/chat')  # 或導向首頁
    return render_template('login.html', error="登入失敗")

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return render_template('logout.html')
