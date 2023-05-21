import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask import Flask, request, jsonify

app = Flask(__name__)

# Инициализация Firebase

cred = credentials.Certificate('./workspace-auth-aebdb-firebase-adminsdk-z6u31-d49d1f10a3.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://firebase-adminsdk-z6u31@workspace-auth-aebdb.iam.gserviceaccount.com'
})

# Получение ссылки на базу данных
ref = db.reference('users')

# Регистрация нового пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if ref.child(username).get() is not None:
        return jsonify({"success": False, "message": "User already exists"}), 400
    ref.child(username).set({"password": password})
    return jsonify({"success": True, "message": "User registered successfully"}), 201

# Авторизация пользователя
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = ref.child(username).get()
    if user is None:
        return jsonify({"success": False, "message": "User does not exist"}), 401
    if user['password'] != password:
        return jsonify({"success": False, "message": "Invalid password"}), 401
    return jsonify({"success": True, "message": "User authenticated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
