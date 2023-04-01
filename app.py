from flask import Flask, request, jsonify

app = Flask(__name__)

# Пример базы данных пользователей
users = {
    "u1": {
        "password": "pass1"
    },
    "user2": {
        "password": "password2"
    }
}


# Регистрация нового пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if username in users:
        return jsonify({"success": False, "message": "User already exists"}), 400
    users[username] = {"password": password}
    return jsonify({"success": True, "message": "User registered successfully"}), 201


# Авторизация пользователя
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if username not in users:
        return jsonify({"success": False, "message": "User does not exist"}), 401
    if users[username]['password'] != password:
        return jsonify({"success": False, "message": "Invalid password"}), 401
    return jsonify({"success": True, "message": "User authenticated successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
