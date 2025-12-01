from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
CORS(app) # Permite que tu PHP en IONOS hable con este Python

# --- CONEXIÓN A LA NUBE (MONGODB ATLAS) ---
# 1. Borra lo que hay entre comillas y pega TU connection string de Atlas.
# 2. Asegúrate de cambiar <password> por tu contraseña real de la base de datos.
uri = "mongodb+srv://c3sarduran029_db_user:<db_password>@cluster0.jkkyfin.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(uri)
    db = client['artesanos_db']       # Nombre de tu base de datos en Mongo
    coleccion = db['detalles_producto'] # Nombre de la colección
    print("✅ Conexión a MongoDB exitosa")
except Exception as e:
    print("❌ Error conectando a MongoDB:", e)

@app.route('/', methods=['GET'])
def inicio():
    return jsonify({"mensaje": "API NoSQL Artesanos funcionando en la nube ☁️"})

# --- GUARDAR DETALLES (POST) ---
@app.route('/api/detalles', methods=['POST'])
def guardar_detalles():
    datos = request.json
    if not datos:
        return jsonify({"error": "No se recibieron datos"}), 400

    nuevo_detalle = {
        "id_producto_mysql": datos.get('id_producto_mysql'),
        "historia": datos.get('historia', ''),
        "tecnica": datos.get('tecnica', ''),
        "materiales": datos.get('materiales', ''),
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    coleccion.insert_one(nuevo_detalle)
    return jsonify({"mensaje": "Guardado correctamente", "status": "ok"})

# --- OBTENER DETALLES (GET) ---
@app.route('/api/detalles/<id_mysql>', methods=['GET'])
def obtener_detalles(id_mysql):
    # Buscamos por el ID que viene de MySQL
    detalle = coleccion.find_one({"id_producto_mysql": id_mysql}, {"_id": 0})
    
    if detalle:
        return jsonify(detalle)
    else:
        # Si no existe, devolvemos vacíos para que no falle el HTML
        return jsonify({
            "historia": "Este producto aún no tiene historia detallada.",
            "tecnica": "Información no disponible.",
            "materiales": "Información no disponible."
        })

if __name__ == '__main__':
    # Esto permite correrlo en tu PC para probar si quieres
    app.run(debug=True, port=5000)