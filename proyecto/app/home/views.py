# app/home/views.py

from flask import render_template
from flask_login import login_required

from . import home


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


@home.route('/api/listall')
def listatodos():
    return "Listando todos los items:"


@home.route('/api/list/<iduser>')
def listaporuser(iduser=0):
    x = "listando items de " + str(iduser)
    return x


@home.route('/api/update/<iduser>/<idprod>/<newcant>')
def modificacant(iduser=0, idprod=0, newcant=0):
    x = "Actualizando en cliente " + str(iduser) + " el producto " + str(idprod) + " con cantidad " + str(newcant)
    return x


@home.route('/api/delete/<iduser>/<idprod>')
def eliminaitem(iduser=0, idprod=0):
    x = "Eliminando el item " + str(idprod) + " del carrito del cliente " + str(iduser)
    return x


@home.route('/api/create/<iduser>/<idprod>/<valor>')
def insertaunitem(iduser=0, idprod=0, valor=0):
    x = "Creando item en carrito del cliente " + str(iduser) + " el producto " + str(idprod) + " con valor unitario: $" + str(valor)
    return x


@home.route('/api/create/<iduser>/<idprod>/<cantidad>/<valor>')
def insertaitems(iduser=0, idprod=0, cantidad=0, valor=0):
    x = "Creando item en carrito del cliente " + str(iduser) + " el producto " + str(idprod) + ", cantidad: " + str(cantidad) + " con valor unitario: $" + str(valor)
    return x


