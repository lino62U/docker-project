from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a la base de datos usando variables de entorno
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER", "myapp_user"),
        password=os.environ.get("DB_PASSWORD", "mypassword"),
        database=os.environ.get("DB_NAME", "myapp_db")
    )

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email FROM users;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (data["name"], data["email"], data["password"])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User added!"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(employees)
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    try:
        data = request.get_json()
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        email = data.get('email')
        salary = data.get('salary')
        date = data.get('date')

        if not all([firstName, lastName, email, salary, date]):
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE employees 
            SET firstName = %s, lastName = %s, email = %s, salary = %s, date = %s 
            WHERE id = %s
        """, (firstName, lastName, email, float(salary), date, id))
        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Employee not found"}), 404

        cursor.close()
        conn.close()
        return jsonify({"message": f"Employee {id} updated successfully"})
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Employee not found"}), 404

        cursor.close()
        conn.close()
        return jsonify({"message": f"Employee {id} deleted successfully"})
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/employees', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        email = data.get('email')
        salary = data.get('salary')
        date = data.get('date')

        if not all([firstName, lastName, email, salary, date]):
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO employees (firstName, lastName, email, salary, date)
            VALUES (%s, %s, %s, %s, %s)
        """, (firstName, lastName, email, float(salary), date))
        conn.commit()

        cursor.execute("SELECT LAST_INSERT_ID() as id")
        new_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({"message": "Employee added successfully", "id": new_id}), 201
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Flask escucha en 0.0.0.0 para ser accesible desde el contenedor
    app.run(host="0.0.0.0", port=5000, debug=True)
