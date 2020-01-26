#./flask/app.py

from flask import Flask
from flask import request, escape, url_for, render_template
import os
import time, datetime
import mandelbrot as mdb
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


'''
Sirviendo contenidos estáticos
Incluye CSS e imagen
Manejo de URLs
'''
# Variable rules
@app.route('/user/<username>')
def hello(username):
    msg_bienvenida = 'Hola muy buenas, Welcome!'
    return render_template('hello.html', name=username, titulo=msg_bienvenida )

@app.route('/usuario/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'Subpath %s' % (subpath)

'''
URL no definida
'''
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

def existe_fichero(ruta_fichero):
    if os.path.isfile(ruta_fichero):
        return True
    return False

'''
Imágenes Dinámicas (binarias)
'''
@app.route('/mandelbrot', methods=['GET','POST'])
def mandelbrot():
    nom_imagen = ""
    ruta="./static/"
    #nombre_fichero = ""
    #existe_mandel = False

    if request.method == "POST":
        x1 = float(request.form["x1"])
        y1 = float(request.form["y1"])
        x2 = float(request.form["x2"])
        y2  = float(request.form["y2"])
        anchura = int(request.form["anchura"])

        nom_imagen = f"mandel_x1{x1}y1{y1}x2{x2}y2{y2}ancho{anchura}.png"

        if not existe_fichero(ruta+nom_imagen):
            nom_imagen = mdb.pintaMandelbrot(x1,y1,x2,y2,anchura,255)

    elif request.method == "GET":
        param = request.args.get("x1")
        if param is not None:
            x1 = float(request.args.get('x1'))
            y1 = float(request.args.get('y1'))
            x2 = float(request.args.get('x2'))
            y2 = float(request.args.get('y2'))
            anchura = int(request.args.get('anch'))

            nom_imagen = f"mandel_x1{x1}y1{y1}x2{x2}y2{y2}ancho{anchura}.png"

            if not existe_fichero(ruta+nom_imagen):
                nom_imagen = mdb.pintaMandelbrot(x1,y1,x2,y2,anchura,255)

    comprobar_cache()
    return render_template('mandelbrot.html', printImage=nom_imagen)

# Elimina imágnes con más de un dia
def comprobar_cache():
    now = time.time()
    path = "./static/"
    for f in os.listdir(path):
        name = os.path.basename(f)
        if 'mandel' in name:
            if os.stat(path+f).st_mtime < now - 86400:
                os.remove(path+f)


# Unique URLS / Redirection behavior
# Si no escribo la / final, se añade sola
@app.route('/projects/')
def projects():
    return 'The project page'

# Si escribo una / al final no reconoce el path
@app.route('/about')
def about():
    return 'The about page'


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return 'login'
    else:
        return 'muestra el formulario'
