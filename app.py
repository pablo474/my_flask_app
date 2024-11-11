from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Inicializar la base de datos
def init_db():
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS emails (id INTEGER PRIMARY KEY, email TEXT)''')
    conn.commit()
    conn.close()

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza el archivo HTML desde la carpeta 'templates'

# Ruta para almacenar correos electrónicos
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Guardar el email en la base de datos
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emails (email) VALUES (?)", (email,))
    conn.commit()
    conn.close()

    return jsonify({"success": "Email saved successfully!"})

# (Opcional) Ruta para verificar los correos almacenados
@app.route('/emails', methods=['GET'])
def get_emails():
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emails")
    emails = cursor.fetchall()
    conn.close()
    return jsonify(emails)

if __name__ == '__main__':
    init_db()  # Inicializar la base de datos cuando se ejecuta la aplicación
    app.run(host='0.0.0.0', port=5000)
