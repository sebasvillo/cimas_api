#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 19:25:09 2020

@author: macbook
"""
import flask
from flask import request, jsonify, redirect, url_for, Flask
from flask_cors import CORS, cross_origin, logging

logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


import random
import time
from pymongo import MongoClient

client = MongoClient('mongodb+srv://sebasvillo:villota123@songsdatabase.wdpae.mongodb.net/songsdatabase?retryWrites=true&w=majority')
db = client.songsdatabase

#1. definir las listas por emocion, y listas de pesos para cada una
alegria = []
tristeza = []
ira = []
calma = []
alegria_p = []
tristeza_p = []
ira_p = []
calma_p = []

#2. meter los elementos correspondientes desde la base de datos a cada lista 
for x in db.songs.find({'Emocion':'Alegría'}):
    alegria.append(x)
for x in db.songs.find({'Emocion':'Tristeza'}):
    tristeza.append(x)
for x in db.songs.find({'Emocion':'Ira'}):
    ira.append(x)
for x in db.songs.find({'Emocion':'Calma'}):
    calma.append(x)

#3. configurar las listas de probabilidades. 
for i in range(len(alegria)):
    alegria_p.append(0.5)
for i in range(len(tristeza)):
    tristeza_p.append(0.5)
for i in range(len(ira)):
    ira_p.append(0.5)
for i in range(len(calma)):
    calma_p.append(0.5)
    
#4. pedirle al usuario su emocion de preferencia
@app.route('/start',methods = ['POST', 'GET'])
def start():
    json_data = flask.request.json
#    listaactual = request.form['nm']
    listaactual = json_data['estado']
    entrega1 = entrega(listaactual)
    return jsonify(prueba=entrega1)


#5. entregarle al usuario una canción de la lista que escogió
#   enrtega recibe un string 'A', 'T, 'I', o 'C', y devuelve una canción "aleatoria" de esa lista
@app.route('/entrega',methods = ['POST', 'GET'])
def entrega(listaactual):
    if listaactual == 0:
        x = alegria    #aliasing B)
    elif listaactual == 1:
        x = calma
    elif listaactual == 2:
        x = tristeza
    elif listaactual == 3:
        x = ira     
    if listaactual == 0:
        y = alegria_p    #aliasing B)
    elif listaactual == 1:
        y = calma_p
    elif listaactual == 2:
        y = tristeza_p
    elif listaactual == 3:
        y = ira_p
    
    res = random.choices(x, weights=y)
    return (res[0]['Titulo'], res[0]['Autor'], res[0]['Link'])

#6. sistema de like o dislike por cada canción, modifica las listas de probabilidades. 
# recibe un objeto de mongodb (el que devuelve entrega()) y un like o dislike ('L' o 'D'), no devuelve nada. 
@app.route('/votacion',methods = ['POST', 'GET'])
def votacion():
    print("empezó")
    json_data = flask.request.json
    print(json_data)
    tit = json_data['tit']
    gus = json_data['gus']
    cancion = db.songs.find_one({'Titulo': tit})
    k = 0
    if gus == 'L': 
        k = 0.05
    elif gus == 'D': 
        k = -0.05
    genero = cancion['Genero']
    gen = cancion['Generacion']
    for i in alegria:
        if i['Genero'] == genero:
            alegria_p[alegria.index(i)]+=2*k
            #por seguridad: 
            if alegria_p[alegria.index(i)] < 0:
                alegria_p[alegria.index(i)] = 0
            elif alegria_p[alegria.index(i)] > 1:
                alegria_p[alegria.index(i)] = 1
        if i['Generacion'] == gen:
            alegria_p[alegria.index(i)]+=k
            #por seguridad: 
            if alegria_p[alegria.index(i)] < 0:
                alegria_p[alegria.index(i)] = 0
            elif alegria_p[alegria.index(i)] > 1:
                alegria_p[alegria.index(i)] = 1
    for i in tristeza:
        if i['Genero'] == genero:
            tristeza_p[tristeza.index(i)]+=2*k
            #por seguridad: 
            if tristeza_p[tristeza.index(i)] < 0:
                tristeza_p[tristeza.index(i)] = 0
            elif tristeza_p[tristeza.index(i)] > 1:
                tristeza_p[tristeza.index(i)] = 1
        if i['Generacion'] == gen:
            tristeza_p[tristeza.index(i)]+=k
            #por seguridad: 
            if tristeza_p[tristeza.index(i)] < 0:
                tristeza_p[tristeza.index(i)] = 0
            elif tristeza_p[tristeza.index(i)] > 1:
                tristeza_p[tristeza.index(i)] = 1
    for i in ira:
        if i['Genero'] == genero:
            ira_p[ira.index(i)]+=2*k
            #por seguridad: 
            if ira_p[ira.index(i)] < 0:
                ira_p[ira.index(i)] = 0
            elif ira_p[ira.index(i)] > 1:
                ira_p[ira.index(i)] = 1
        if i['Generacion'] == gen:
            ira_p[ira.index(i)]+=k
            #por seguridad: 
            if ira_p[ira.index(i)] < 0:
                ira_p[ira.index(i)] = 0
            elif ira_p[ira.index(i)] > 1:
                ira_p[ira.index(i)] = 1
    for i in calma:
        if i['Genero'] == genero:
            calma_p[calma.index(i)]+=2*k
            #por seguridad: 
            if calma_p[calma.index(i)] < 0:
                calma_p[calma.index(i)] = 0
            elif calma_p[calma.index(i)] > 1:
                calma_p[calma.index(i)] = 1
        if i['Generacion'] == gen:
            calma_p[calma.index(i)]+=k
            #por seguridad: 
            if calma_p[calma.index(i)] < 0:
                calma_p[calma.index(i)] = 0
            elif calma_p[calma.index(i)] > 1:
                calma_p[calma.index(i)] = 1
    return('ok')
#7 compilacion: 
def total():
    x = start()
    while True: 
        cancionactual = entrega(x)
        print(cancionactual[0]['Titulo'], "por", cancionactual[0]['Autor'], cancionactual[0]['Link'])
        gusto = input('Te gustó la canción que acabas de escuchar? Escribe L si te gustó, D si no: ')
        votacion(cancionactual,gusto)
        
        

app.run()
