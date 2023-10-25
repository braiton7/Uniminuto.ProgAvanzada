from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import os
import database as db
import bcrypt
from flask import session


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = "4ndr35&d14n4"


#Rutas de la aplicación
@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM productos")
    myresult = cursor.fetchall()
    # Convertir los datos a un diccionario
    insertObject = []
    columncantidads = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columncantidads, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar licores en la bd
@app.route('/licores', methods=['POST'])
def addLicores():
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
    return redirect(url_for('home'))


@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM productos WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
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
    return redirect(url_for('home'))

#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Verifica el nombre de usuario y la contraseña en la base de datos
        if user_exists(username, password):
            # Autenticación exitosa, establece una sesión para marcar al usuario como autenticado
            session['logged_in'] = True
            # Redirige al usuario a la página de inicio
            return redirect(url_for('home'))
        else:
            # Autenticación fallida, muestra un mensaje de error
            flash('Nombre de usuario o contraseña incorrectos', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')


# Función para verificar la existencia del usuario y la contraseña
def user_exists(username, password):
    cursor = db.database.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
    user_data = cursor.fetchone()
    cursor.close()

    if user_data and user_data[1] == password:
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True, port=4000)