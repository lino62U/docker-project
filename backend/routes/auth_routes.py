from flask import Blueprint, request, jsonify
import mysql.connector

auth_bp = Blueprint("auth", __name__)

# Configuración MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tu_password",
    database="mi_base"
)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
