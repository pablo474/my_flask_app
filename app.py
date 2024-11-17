from flask import Flask, request, jsonify, render_template
import psycopg2
import os
import json

app = Flask(__name__)

# Cargar configuración de enlaces desde config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Conexión a PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')
try:
    conn = psycopg2.connect(DATABASE_URL)
except Exception as e:
    print("Error connecting to the database:", e)

@app.route('/')
def index():
    # Renderizar la plantilla index.html con los enlaces del archivo config.json
    return render_template('index.html', links=config['links'])

@app.route('/registrar_email', methods=['POST'])
def registrar_email():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    # Insertar en la base de datos
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO emails (email, nombre, apellido) VALUES (%s, %s, %s)",
                           (email, first_name, last_name))
            conn.commit()
        return jsonify({"status": "éxito", "message": "Correo registrado con éxito"}), 200
    except Exception as e:
        print("Error inserting into the database:", e)
        return jsonify({"status": "error", "message": "Error registrando el correo"}), 500

if __name__ == '__main__':
    app.run(debug=True)
