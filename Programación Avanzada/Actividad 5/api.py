# Importaciones necesarias
from flask import Flask, request, jsonify, redirect, url_for, flash
import os
import database as db
from flask import session

# Establecer la ubicación de los archivos de plantilla (templates)
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

# Inicializar la aplicación Flask
app = Flask(__name__, template_folder=template_dir)
app.secret_key = "4ndr35&d14n4"

# Rutas de la aplicación

# Ruta principal para listar productos
@app.route('/productos')
def home():
    """
    Lista todos los productos si el usuario está autenticado.

    Returns:
        JSON: Una lista de productos en formato JSON.
    """
    if not session.get('logged_in'):
        return jsonify({"error": "No estás autenticado"}), 401

    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM productos")
    myresult = cursor.fetchall()
    # Convertir los datos a una lista de diccionarios
    data = []
    columncantidads = [column[0] for column in cursor.description]
    for record in myresult:
        data.append(dict(zip(columncantidads, record)))
    cursor.close()
    return jsonify(data)

# Ruta para guardar licores en la base de datos
@app.route('/licores', methods=['POST'])
def addLicores():
    """
    Agrega un nuevo licor a la base de datos.

    Returns:
        JSON: Un mensaje de éxito o un mensaje de error si faltan datos.
    """
    nameli = request.form['nameli']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    date = request.form['date']

    if nameli and cantidad and precio and date:
        cursor = db.database.cursor()
        sql = "INSERT INTO productos (nombre, cantidad, precio_unitario, fecha_vencimiento) VALUES (%s, %s, %s, %s)"
        data = (nameli, cantidad, precio, date)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
        return jsonify({"message": "Producto agregado con éxito"})
    return jsonify({"error": "Datos faltantes"}), 400

# Ruta para eliminar un producto por ID
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Elimina un producto de la base de datos por su ID.

    Returns:
        JSON: Un mensaje de éxito.
    """
    cursor = db.database.cursor()
    sql = "DELETE FROM productos WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    cursor.close()
    return jsonify({"message": "Producto eliminado con éxito"})

# Ruta para editar un producto por ID
@app.route('/edit/<int:id>', methods=['PUT'])
def edit(id):
    """
    Edita un producto de la base de datos por su ID.

    Returns:
        JSON: Un mensaje de éxito o un mensaje de error si faltan datos.
    """
    nameli = request.form['nameli']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    date = request.form['date']

    if nameli and cantidad and precio:
        cursor = db.database.cursor()
        sql = "UPDATE productos SET nombre = %s, cantidad = %s, precio_unitario = %s, fecha_vencimiento = %s WHERE id = %s"
        data = (nameli, cantidad, precio, date, id)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
        return jsonify({"message": "Producto actualizado con éxito"})
    return jsonify({"error": "Datos faltantes"}), 400

# Ruta de autenticación
@app.route('/login', methods=['POST'])
def login():
    """
    Realiza la autenticación del usuario.

    Returns:
        JSON: Un mensaje de éxito si la autenticación es exitosa, o un mensaje de error si no lo es.
    """
    username = request.form['username']
    password = request.form['password']
    if user_exists(username, password):
        session['logged_in'] = True
        return jsonify({"message": "Inicio de sesión exitoso"})
    else:
        return jsonify({"error": "Nombre de usuario o contraseña incorrectos"}), 401

# Función para verificar la existencia del usuario y la contraseña
def user_exists(username, password):
    """
    Verifica si el usuario y la contraseña proporcionados son correctos.

    Args:
        username (str): El nombre de usuario.
        password (str): La contraseña.

    Returns:
        bool: True si el usuario y contraseña son correctos, False en caso contrario.
    """
    cursor = db.database.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
    user_data = cursor.fetchone()
    cursor.close()

    if user_data and user_data[1] == password:
        return True
    return False

# Ejecutar la aplicación en el puerto 4000 en modo de depuración
if __name__ == '__main__':
    app.run(debug=True, port=4000)
