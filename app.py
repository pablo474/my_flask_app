from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import gspread
from google.oauth2.service_account import Credentials
import os

app = Flask(__name__)
# Esta clave es necesaria para que las sesiones funcionen. Cámbiala por algo único.
app.secret_key = 'yonko_secret_key_2024' 

# Configuración de Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
JSON_FILE = "yonko-web-039aabb8e53b.json"

# Contraseña para entrar al Drop (Cámbiala por la que tú quieras)
DROP_PASSWORD = "YONKO_PASSWORD"

try:
    creds = Credentials.from_service_account_file(JSON_FILE, scopes=scope)
    client = gspread.authorize(creds)
    SHEET_NAME = "maillist" 
except Exception as e:
    print(f"Error de conexión Sheets: {e}")

@app.route('/')
def index():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except:
        config = {"links": {"youtube": "#", "spotify": "#", "instagram": "#"}}
    return render_template('index.html', links=config['links'])

@app.route('/registrar_email', methods=['POST'])
def registrar_email():
    email = request.form.get('email')
    if email:
        try:
            sheet = client.open(SHEET_NAME).sheet1
            sheet.append_row([email])
            return jsonify({"status": "éxito", "message": "¡Suscrito correctamente!"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": "Error de base de datos"}), 500
    return jsonify({"status": "error", "message": "Email inválido"}), 400

@app.route('/login', methods=['POST'])
def login():
    # Recibimos la contraseña del modal
    password = request.form.get('password')
    if password == DROP_PASSWORD:
        session['access_granted'] = True # Guardamos el permiso en la sesión
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "PASSWORD INCORRECTO"}), 401

@app.route('/drop')
def drop_page():
    # Si intentan entrar al drop sin contraseña, los devuelve a la landing
    if not session.get('access_granted'):
        return redirect(url_for('index'))
    return "PÁGINA DEL DROP (PRÓXIMAMENTE)" # Aquí pondremos el cronómetro y Stripe luego

if __name__ == '__main__':
    app.run(debug=True)
