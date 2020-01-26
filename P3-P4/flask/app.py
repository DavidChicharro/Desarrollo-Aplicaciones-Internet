#./flask/app.py

from flask import Flask
from flask import request, escape, url_for, render_template, session, redirect, flash
from pickleshare import *
from pymongo import MongoClient
import os
import re

app = Flask(__name__)
app.secret_key = 'super secret key'

db = PickleShareDB('~/dbpickleshare')

client = MongoClient("mongo", 27017)
mdb = client.SampleCollections

list_webs = list()

def handle_visited_webs(vw,lista_webs):
    if vw in lista_webs:
        if vw!=lista_webs[-1] and len(lista_webs)>1:
            if lista_webs.index(vw)==0:
                lista_webs = lista_webs[1:]
                lista_webs.append(vw)
            else:
                lista_webs[1], lista_webs[2] = lista_webs[2], lista_webs[1]
    else:
        if(len(lista_webs)==3):
            lista_webs = lista_webs[1:]
            lista_webs.append(vw)
        else:
            lista_webs.append(vw)

    return lista_webs



@app.route('/mongo')
def mongo():
    poks = mdb.samples_pokemon.find()  # Encontramos los documentos de la coleccion "samples_friends"

    return poks
    #return val[0]['name']

@app.route('/buscarmispokemons')
def buscarmispokemons():
    if 'usuario' in session:
        usuario = session['usuario']

        mypoks = mdb.usuarios.find( )

        lista_poks = list()

        for pok in mypoks:
            if pok['user'] == session['email']:
                lista_poks = pok['pokemons']

        return lista_poks


@app.route('/buscarpokemon', methods = ['GET', 'POST'])
def buscarpokemon():
    if 'usuario' in session:
        nom_pok = request.form['nompokemon']

        #Si existe / si no existe
        return redirect(url_for('pokemon',pokemon=nom_pok))

@app.route('/addpokemon', methods = ['POST'])
def addpokemon():
    if 'usuario' in session:
        nom_pokemon_add = request.form['nom_pokemon']
        mdb.usuarios.update( { "user": session['email'] }, { "$push": { "pokemons": nom_pokemon_add } } )

    return redirect(url_for('pokemon',pokemon=nom_pokemon_add))

@app.route('/pokemon/<pokemon>', methods = ['GET', 'POST'])
def pokemon(pokemon):
    if 'usuario' in session:
        session['web_visit'] = handle_visited_webs(request.url.lower(),session['web_visit'])

        lista_pokemons = mongo()

        existe_pok = False
        mis_poks = buscarmispokemons()
        if pokemon in mis_poks:
            existe_pok = True

        for pok in lista_pokemons:
            if pok['name'].lower() == pokemon.lower():
                pokemon_buscado = pok

                return render_template('pokemon.html', datos_pokemon=pokemon_buscado, btn=existe_pok)

    return render_template('pokemon.html')
    


@app.route('/')
def index():
    if 'usuario' in session:
        usuario = session['usuario']
        webs = session['web_visit']
        list_content = ["Última web visitada","Penúltima web visitada","Antepenúltima web visitada"]
        return render_template('index.html',user=usuario,webs_visitadas=webs[::-1],cont=list_content)

    return render_template('index.html', user="")


@app.route('/login', methods = ['GET', 'POST'])
def login():
    usuario = request.form['usuario']
    password = request.form['password']
    db = PickleShareDB('~/dbpickleshare')
    if usuario in db:
        if db[usuario]['password'] == password:
            session['usuario'] = db[usuario]['nombre']
            session['email'] = usuario
            list_webs = []
            session['web_visit'] = list_webs
            return redirect('/')
    return redirect('/')



@app.route('/logout')
def logout():
    session.clear()
    session.pop('logged_in', None)
    return redirect('/')


@app.route('/altausuario')
def altausuario():
    return render_template('altausuario.html')

@app.route('/registro',methods=["POST"])
def registrousuario():
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    email = request.form['email']
    password = request.form['password']
    fecha_nac = request.form['fecha_nac']

    db[email]={'email':email, 'password':password, 'nombre':nombre, 'apellidos':apellidos, 'fecha_nac':fecha_nac}

    user_mongodb = {
        "user": email,
        "name": nombre,
        "pokemons": []
    }
    mdb.usuarios.insert(user_mongodb)

    return redirect('/')



@app.route('/mispokemons')
def mispokemons():
    if 'usuario' in session:
        session['web_visit'] = handle_visited_webs(request.url,session['web_visit'])
        poks = buscarmispokemons()
        pokemons_all = mongo()

        mis_pokemons = list()

        for pokemon in pokemons_all:
            if pokemon['name'] in poks:
                nombre_pok = pokemon['name']
                tipo_pok = pokemon['type']
                img_pok = pokemon['img']
                pok_item=[nombre_pok,tipo_pok,img_pok]
                mis_pokemons.append(pok_item)
        
        ult_poks = mdb.samples_pokemon.find().sort([("id", -1),("num", -1)]).limit(10)

        usuario = session['usuario']
        return render_template('mispokemons.html',user=usuario,pokemons=mis_pokemons,ultimos_poks=ult_poks)

    return redirect('/')


@app.route('/datospersonales')
def datospersonales():
    if 'usuario' in session:
        session['web_visit'] = handle_visited_webs(request.url,session['web_visit'])
        email = session['email']
        usuario = session['usuario']
        datos_personales = db[email]
        return render_template('datospersonales.html',user=usuario,datos=datos_personales)

    return redirect('/')


@app.route('/cambiardatos', methods = ['GET', 'POST'])
def cambiardatos():
    if 'nombre' in request.form:
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        fecha_nac = request.form['fecha_nac']

        email_user = db[session['email']]['email']

        #el email se ha cambiado
        if email != email_user:
            db[email] = db[email_user]
            db[email]['email'] = email
            session['email'] = email

        db[email]['nombre'] = nombre
        db[email]['apellidos'] = apellidos
        db[email]['fecha_nac'] = fecha_nac

        session['usuario'] = nombre
    elif 'passActual' in request.form:
        password = request.form['passActual']
        new_pass = request.form['passNueva']

        pass_user = db[session['email']]['password']
        if pass_user == password:
            db[session['email']]['password'] = new_pass


    return redirect('/datospersonales')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404