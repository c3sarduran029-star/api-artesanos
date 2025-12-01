# app.py ACTUALIZADO
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- PEGA TU URI CON LA CONTRASEÑA CORRECTA AQUÍ ---
uri = "mongodb+srv://c3sarduran029_db_user:B97iDf13F4DGsvdP@cluster0.jkkyfin.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(uri)
    db = client['artesanos_db']
    coleccion = db['detalles_producto']
    print("✅ Conexión a MongoDB exitosa")
except Exception as e:
    print("❌ Error conectando a MongoDB:", e)

@app.route('/', methods=['GET'])
def inicio():
    return jsonify({"mensaje": "API NoSQL Artesanos V2 (Con Edición y Borrado) 🚀"})

# 1. LEER (GET)
@app.route('/api/detalles/<id_mysql>', methods=['GET'])
def obtener_detalles(id_mysql):
    try:
        # Intentar buscar como entero, si falla, como string
        id_busqueda = int(id_mysql)
    except:
        id_busqueda = id_mysql

    detalle = coleccion.find_one({"id_producto_mysql": id_busqueda}, {"_id": 0})
    
    if not detalle:
        # Intento secundario (por si se guardó como string)
        detalle = coleccion.find_one({"id_producto_mysql": str(id_mysql)}, {"_id": 0})

    if detalle:
        return jsonify(detalle)
    else:
        return jsonify({
            "historia": "", "tecnica": "", "materiales": "", "tags": []
        })

# 2. CREAR O ACTUALIZAR (POST / PUT) - "UPSERT"
@app.route('/api/detalles/guardar', methods=['POST'])
def guardar_o_actualizar():
    datos = request.json
    if not datos or 'id_producto_mysql' not in datos:
        return jsonify({"error": "Datos incompletos"}), 400

    id_mysql = datos['id_producto_mysql']
    
    # Datos a guardar
    datos_actualizados = {
        "historia": datos.get('historia', ''),
        "tecnica": datos.get('tecnica', ''),
        "materiales": datos.get('materiales', ''),
        "tags": datos.get('tags', []),
        "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Intentamos convertir ID a entero para consistencia
    try:
        id_query = int(id_mysql)
    except:
        id_query = id_mysql

    # La magia de Mongo: update_one con upsert=True
    # Si existe, lo actualiza. Si no existe, lo crea.
    coleccion.update_one(
        {"id_producto_mysql": id_query},
        {"$set": datos_actualizados},
        upsert=True
    )
    
    return jsonify({"mensaje": "Datos actualizados en NoSQL", "status": "ok"})

# 3. ELIMINAR (DELETE)
@app.route('/api/detalles/eliminar/<id_mysql>', methods=['DELETE'])
def eliminar_detalles(id_mysql):
    try:
        id_query = int(id_mysql)
    except:
        id_query = id_mysql
        
    coleccion.delete_one({"id_producto_mysql": id_query})
    return jsonify({"mensaje": "Eliminado de NoSQL", "status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

