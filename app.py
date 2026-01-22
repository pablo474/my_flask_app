from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Cargar configuración de enlaces
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except Exception:
    config = {"links": {"youtube": "#", "spotify": "#", "instagram": "#"}}

# RUTA PARA GUARDAR LOS CORREOS (Archivo local)
LOG_FILE = "lista_correos.txt"

@app.route('/')
def index():
    return render_template('index.html', links=config['links'])

@app.route('/registrar_email', methods=['POST'])
def registrar_email():
    email = request.form.get('email')
    if email:
        # Guardar el correo en el archivo local 'lista_correos.txt'
        with open(LOG_FILE, "a") as f:
            f.write(f"{email}\n")
        print(f"NUEVO CORREO: {email}")
        return jsonify({"status": "éxito", "message": "¡Correo guardado!"}), 200
    return jsonify({"status": "error", "message": "Correo no válido"}), 400

# RUTA SECRETA PARA VER TUS CORREOS
# Entra a tu_dominio.com/ver_mis_correos_secretos para ver la lista
@app.route('/ver_mis_correos_secretos')
def ver_correos():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            correos = f.readlines()
        return f"<h1>Tus correos:</h1><pre>{''.join(correos)}</pre>"
    return "Aún no hay correos registrados."

if __name__ == '__main__':
    app.run(debug=True)
