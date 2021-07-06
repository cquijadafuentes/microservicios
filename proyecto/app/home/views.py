# app/home/views.py
from flask import jsonify
from flask import render_template
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


