from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Ruta del archivo JSON
EMAILS_JSON_FILE = 'emails.json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar_email', methods=['POST'])
def registrar_email():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    # Cargar los correos existentes del archivo JSON
    if os.path.exists(EMAILS_JSON_FILE):
        with open(EMAILS_JSON_FILE, 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Añadir el nuevo correo
    data.append({"email": email, "nombre": first_name, "apellido": last_name})

    # Guardar en el archivo JSON
    with open(EMAILS_JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

    return jsonify({"status": "éxito", "message": "Correo registrado con éxito"}), 200

if __name__ == '__main__':
    app.run(debug=True)
