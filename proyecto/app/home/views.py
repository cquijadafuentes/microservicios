# app/home/views.py
from flask import jsonify
from flask import render_template
from flask import session
from flask import request
from flask_login import login_required
from ..models import ShoppingCart

from . import home

import requests

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="PetStoreSystem")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")

@home.route('/homelogin/<username>/<userphone>')
def homelogin(username=None, userphone=None):
    if userphone is not None :
        session['sess_loged_username'] = username
        session['sess_loged_userphone'] = userphone
    
    return shoppingcart()


@home.route('/homelogout')
def homelogout():
    print("saliendo!")
    session.pop('sess_loged_username', default=None)
    session.pop('sess_loged_userphone', default=None)
    return render_template('home/index.html', title="PetStoreSystem")


@home.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        print("recibiendo datos - registrando")
        print(request.form['username'])
        print(request.form['phone'])
        print(request.form['address'])
        datos = {'name':request.form['username'], 'phone':request.form['phone'], 'address':request.form['address']}
        registro = requests.post('http://petstorecustomer.appspot.com/create', json = datos)
        if registro.status_code == 200:
            return homelogin(request.form['username'], request.form['phone'])
        print("respuesta: " + registro.text)
    print("desplegando webpage - registrando")
    return render_template('home/registro.html', title="Registro")



@home.route('/listusers')
def listusers():
    users = requests.get('http://petstorecustomer.appspot.com/list/all').json()
    print(users)
    return render_template('home/users.html', title="Lista Ususarios", users=users)


@home.route('/listpets')
def listpets():
    pets = requests.get('http://practiceiv-on-gcloud.appspot.com/products/fetch').json()['products']
    print(pets)
    return render_template('home/pets.html', title="Lista Mascotas", pets=pets)


@home.route('/shoppingcart')
def shoppingcart():
    pets = requests.get('http://studentestwebapp.azurewebsites.net/api/list/'+session['sess_loged_userphone']).json()['json_list']
    print(pets)
    return render_template('home/shoppingcart.html', title="Carrito de compra", pets=pets)

@home.route('/addpet/<idpet>/<value>')
def addpet(idpet, value):
    A = ShoppingCart.query.filter_by(id_user=session['sess_loged_userphone'], id_pet=idpet).first()
    if A is not None:
        A.cant += 1
        A.update()
        return listpets()
    carrito = ShoppingCart()
    carrito.id_user = id_user=session['sess_loged_userphone']
    carrito.id_pet = idpet
    carrito.cant = 1
    carrito.unitprice = value
    carrito.add()
    return listpets()


@home.route('/deletepet/<idpet>')
def deletepet(idpet):
    carrito = ShoppingCart.query.filter_by(id_user=session['sess_loged_userphone'], id_pet=idpet).first()
    if carrito is None:
        return "No existe el registro en el carrito", 400
    carrito.delete()
    return "Item del carrito eliminado", 200


@home.route('/api/listall')
def listatodos():
    carritos = ShoppingCart.query.all()
    return jsonify(json_list=[i.serialize for i in carritos])


@home.route('/api/list/<iduser>')
def listaporuser(iduser=0):
    carritos = ShoppingCart.query.filter_by(id_user=iduser)
    return jsonify(json_list=[i.serialize for i in carritos])


@home.route('/api/update/cant/<iduser>/<idprod>/<newcant>')
def modificacant(iduser=0, idprod=0, newcant=0):
    carrito = ShoppingCart.query.filter_by(id_user=iduser, id_pet=idprod).first()
    if carrito is None:
        return "No existe el registro en el carrito", 400

    if(newcant == '0'):
        eliminaitem(iduser, idprod)
        return "Item del carrito eliminado", 200

    carrito.cant = newcant
    carrito.update()
    return jsonify(carrito.serialize)


@home.route('/api/update/price/<iduser>/<idprod>/<newprice>')
def modificaprice(iduser=0, idprod=0, newprice=0):
    carrito = ShoppingCart.query.filter_by(id_user=iduser, id_pet=idprod).first()
    if carrito is None:
        return "No existe el registro en el carrito", 400

    carrito.unitprice = newprice
    carrito.update()
    return jsonify(carrito.serialize)


@home.route('/api/delete/<iduser>/<idprod>')
def eliminaitem(iduser=0, idprod=0):
    carrito = ShoppingCart.query.filter_by(id_user=iduser, id_pet=idprod).first()
    if carrito is None:
        return "No existe el registro en el carrito", 400
    carrito.delete()
    return "Item del carrito eliminado", 200


@home.route('/api/create/<iduser>/<idprod>/<valor>')
def insertaunitem(iduser=0, idprod=0, valor=0):
    A = ShoppingCart.query.filter_by(id_user=iduser, id_pet=idprod).first()
    if A is not None:
        return "El registro del carrito ya existe", 400
    carrito = ShoppingCart()
    carrito.id_user = iduser
    carrito.id_pet = idprod
    carrito.cant = 1
    carrito.unitprice = valor
    carrito.add()
    return jsonify(carrito.serialize)


@home.route('/api/create/<iduser>/<idprod>/<cantidad>/<valor>')
def insertaitems(iduser=0, idprod=0, cantidad=0, valor=0):
    A = ShoppingCart.query.filter_by(id_user=iduser, id_pet=idprod).first()
    if A is not None:
        return "El registro del carrito ya existe", 400
    carrito = ShoppingCart()
    carrito.id_user = iduser
    carrito.id_pet = idprod
    carrito.cant = cantidad
    carrito.unitprice = valor
    carrito.add()
    return jsonify(carrito.serialize)


