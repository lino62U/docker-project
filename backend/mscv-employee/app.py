from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER", "myapp_user"),
        password=os.environ.get("DB_PASSWORD", "mypassword"),
        database=os.environ.get("DB_NAME", "myapp_db")
    )

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
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees 
        SET firstName=%s, lastName=%s, email=%s, salary=%s, date=%s 
        WHERE id=%s
    """, (data['firstName'], data['lastName'], data['email'], float(data['salary']), data['date'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Employee {id} updated successfully"})

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Employee {id} deleted successfully"})

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employees (firstName, lastName, email, salary, date)
        VALUES (%s, %s, %s, %s, %s)
    """, (data['firstName'], data['lastName'], data['email'], float(data['salary']), data['date']))
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID() as id")
    new_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return jsonify({"message": "Employee added successfully", "id": new_id}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
