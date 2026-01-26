from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import gspread
from google.oauth2.service_account import Credentials
import os

app = Flask(__name__)
app.secret_key = 'yonko_ultra_secret_2026' 

# CONFIGURACIÓN DE ACCESOS
PASSWORDS = {
    "DROP2026": "drop_page",    # Acceso a la tienda
    "MUSICVIP": "musica_page"   # Acceso al reproductor
}

# Configuración de Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
JSON_FILE = "yonko-web-039aabb8e53b.json"

try:
    creds = Credentials.from_service_account_file(JSON_FILE, scopes=scope)
    client = gspread.authorize(creds)
    SHEET_NAME = "maillist" 
except Exception as e:
    print(f"Error Sheets: {e}")

@app.route('/')
def index():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except:
        config = {"links": {"youtube": "#", "spotify": "#", "instagram": "#"}}
    return render_template('index.html', links=config['links'])

@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password in PASSWORDS:
        target_route = PASSWORDS[password]
        session['access_type'] = target_route
        return jsonify({"status": "success", "redirect": url_for(target_route)}), 200
    return jsonify({"status": "error", "message": "CONTRASEÑA INVÁLIDA"}), 401

@app.route('/drop')
def drop_page():
    if session.get('access_type') != 'drop_page':
        return redirect(url_for('index'))
    return render_template('drop.html')

@app.route('/musica')
def musica_page():
    if session.get('access_type') != 'musica_page':
        return redirect(url_for('index'))
    return render_template('musica.html')

@app.route('/registrar_email', methods=['POST'])
def registrar_email():
    email = request.form.get('email')
    if email:
        try:
            sheet = client.open(SHEET_NAME).sheet1
            sheet.append_row([email])
            return jsonify({"status": "éxito", "message": "¡REGISTRADO!"}), 200
        except:
            return jsonify({"status": "error", "message": "ERROR"}), 500
    return jsonify({"status": "error", "message": "EMAIL INVÁLIDO"}), 400

if __name__ == '__main__':
    app.run(debug=True)
