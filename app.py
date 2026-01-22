from flask import Flask, request, jsonify, render_template
import json
import gspread
from google.oauth2.service_account import Credentials
import os

app = Flask(__name__)

# Configuración de Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Usamos el nombre exacto de tu archivo descargado
JSON_FILE = "yonko-web-039aabb8e53b.json"

try:
    creds = Credentials.from_service_account_file(JSON_FILE, scopes=scope)
    client = gspread.authorize(creds)
    # Reemplaza 'Yonko Emails' por el nombre exacto de tu hoja de Google Sheets
    SHEET_NAME = "Yonko Emails" 
except Exception as e:
    print(f"Error configurando Google Sheets: {e}")

@app.route('/')
def index():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except:
        config = {"links": {"youtube": "#", "spotify": "#"}}
    return render_template('index.html', links=config['links'])

@app.route('/registrar_email', methods=['POST'])
def registrar_email():
    email = request.form.get('email')
    if email:
        try:
            # Abre la hoja y añade el email al final
            sheet = client.open(SHEET_NAME).sheet1
            sheet.append_row([email])
            return jsonify({"status": "éxito", "message": "Email guardado"}), 200
        except Exception as e:
            print(f"Error al escribir en Sheets: {e}")
            return jsonify({"status": "error", "message": "Error de servidor"}), 500
    return jsonify({"status": "error", "message": "Email vacío"}), 400

if __name__ == '__main__':
    app.run(debug=True)
