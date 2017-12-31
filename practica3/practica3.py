# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
from pymongo import MongoClient
from flask import redirect,session,url_for, escape, jsonify, request
import shelve
import re
import string

app = Flask(__name__)

app.secret_key = 'Secreto'

pag=1

@app.after_request
def save_history(rsp):
        if 'miembro' in session and request.method == "GET" and rsp.mimetype == "text/html":
                        session['urls'].append(request.path)
                        session.modified = True
                        if(len(session['urls'])) > 3:
                                session['urls'].pop(0)
        return rsp


@app.route("/")
def template():
	return render_template('padre.html')



@app.route("/hijo")
def hijo():
	return render_template('hijo.html')

@app.route("/hijo2")
def hijo2():
	return render_template('hijo2.html')

@app.route("/hijo3")
def hijo3():
	return render_template('hijo3.html')

@app.route("/login", methods = ['GET', 'POST'])
def login():
	database = shelve.open('database.db')
	miembro = request.form['miembro']
        
	if request.method == 'POST' and miembro in database and database[miembro]['Contraseña'] == request.form['pass'] :
		session['miembro'] = request.form['miembro']
		session['urls'] = []

	database.close()
	return render_template('padre.html')

@app.route('/logout')
def logout():
   session.pop('miembro','urls')   
   return render_template('padre.html')


@app.route('/registro', methods = ['GET', 'POST'])
def reg():
	if request.method == 'POST' :
		database = shelve.open('database.db')
		database[request.form['miembro']] = {'Nombre' : request.form['miembro'], 'Contraseña' : request.form['pass'], 'Telefono' : request.form['tel']}
		database.close()
	return render_template('registro.html')

@app.route('/ver')
def ver():
	database = shelve.open('database.db')
	datos = database[session['miembro']]
	database.close()
	return render_template('ver.html', Nombre = 'Nombre: ' + datos['Nombre'], Tel =  'Telefono: ' + datos['Telefono'])

@app.route('/editar', methods = ['GET', 'POST'])
def editar():
	database = shelve.open('database.db',writeback=True)
	datos = database[session['miembro']]
	if request.method == 'POST' :
		datos['Nombre']=request.form['miembro']
		datos['Contraseña']=request.form['pass']
		datos['Telefono']=request.form['tel']
	database.close()
	return render_template('editar.html', Nombre = datos['Nombre'], Tel =datos['Telefono'], Contra =datos['Contraseña'])
	
@app.route('/buscar', methods = ['GET', 'POST'])
def buscar():
	paginas = 200
	client = MongoClient()
	db = client.test    

	if request.method == 'POST' :
			
		s=db.restaurants.find_one( { "cuisine": request.form["cocina"] }, { "name": 1, "_id":0 , "borough": 1} )
		res=str(s)
		if res=="None":
			res="No hay resultados"
		else:
			patron = re.compile("u'name':\su'(.*?)'")
			name=patron.findall(str(res))
			patron = re.compile("u'borough':\su'(.*?)'")
			boro=patron.findall(str(res))
			res="Nombre: "+ str(name) + " Barrio: "+str(boro)
		return render_template('buscar.html',NotFound=res)
	else:


		total = db.restaurants.find().count()
		offset = (1-1)*paginas
		res=db.restaurants.find().skip(offset).limit(paginas)
		a=""
		while(res.alive):
			try:
				a=a+str(res.next())
			except StopIteration:
				a="No hay resultados"
				return render_template('buscar.html',NotFound=a)

		patron = re.compile("'name':\s'(.*?)'")
		s=patron.findall(str(a))


		return render_template('buscar.html',Nombre=s)
	
@app.route('/get_sig')
def responde():
	paginas = 200
	client = MongoClient('mongodb://localhost:27017/')
	db = client['test']

	global pag
	accion = request.args.get('pag', '')
	if accion=="mas":
		pag=pag+1
	else:
		if pag >1:
			pag=pag-1
		
	total = db.restaurants.find().count()
	offset = (pag-1)*paginas
	sig=db.restaurants.find().skip(offset).limit(paginas)
	a=""
	while(sig.alive):
		try:
			a=a+str(sig.next())
		except StopIteration:
			a="No hay resultados"
			return render_template('buscar.html',NotFound=a)

	patron = re.compile("'name':\s'(.*?)'")
	s=patron.findall(str(a))

	return jsonify({'s':s})    # podría ser string o HTML





if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
