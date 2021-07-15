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

@home.route('/homelogin/<username>/<userphone>/<useraddress>')
def homelogin(username=None, userphone=None, useraddress=None):
    if userphone is not None :
        session['sess_loged_username'] = username
        session['sess_loged_userphone'] = userphone
        session['sess_loged_useraddress'] = useraddress
    
    return shoppingcart()


@home.route('/homelogout')
def homelogout():
    print("saliendo!")
    session.pop('sess_loged_username', default=None)
    session.pop('sess_loged_userphone', default=None)
    session.pop('sess_loged_useraddress', default=None)
    return render_template('home/index.html', title="PetStoreSystem")


@home.route('/register', methods=['GET','POST'])
def register(message=None):
    if request.method == 'POST':
        print("recibiendo datos - registrando")
        print(request.form['username'])
        print(request.form['phone'])
        print(request.form['address'])
        datos = {'name':request.form['username'], 'phone':request.form['phone'], 'address':request.form['address']}
        req_cliente = requests.get('http://petstorecustomer.appspot.com/list/byphone/'+request.form['phone'])
        if len(req_cliente.json()) > 0:
            print("Telefono de usuario ya existe")
            print(str(req_cliente.json()))
            return render_template('home/registro.html', title="Registro", message="Telefono de usuario ya existe")
        registro = requests.post('http://petstorecustomer.appspot.com/create', json = datos)
        if registro.status_code == 200:
            return homelogin(request.form['username'], request.form['phone'])
        print("respuesta: " + registro.text)
    print("desplegando webpage - registrando")
    return render_template('home/registro.html', title="Registro")


@home.route('/registerpet', methods=['GET','POST'])
def registerpet():
    if request.method == 'POST':
        print("recibiendo datos - registrando")
        print(request.form['breed'])
        print(request.form['id'])
        print(request.form['image_url'])
        print(request.form['price'])
        print(request.form['specie'])
        print(request.form['stock'])
        req_pet = requests.get('http://practiceiv-on-gcloud.appspot.com/products/get/id/'+request.form['id'])
        print(req_pet.status_code)
        print(req_pet.text)
        while req_pet.status_code != 200 and req_pet.status_code != 404:
            print("Otra vez..")
            req_pet = requests.get('http://practiceiv-on-gcloud.appspot.com/products/get/id/'+request.form['id'])
            print(req_pet.status_code)
            print(req_pet.text)
        if req_pet.status_code == 200:
            print("La mascota con esa id ya existe")
            return render_template('home/nuevamascota.html', title="Registro", message="El id de la mascota ya existe")
        datos = {'breed':request.form['breed'], 'id':int(request.form['id']), 'image_url':request.form['image_url'], 'price':int(request.form['price']), 'specie':request.form['specie'], 'stock':int(request.form['stock'])}
        print(str(datos))
        registro = requests.post('http://practiceiv-on-gcloud.appspot.com/products/create', json=datos)
        print("respuesta: " + registro.text)
        while registro.status_code != 200:
            registro = requests.post('http://practiceiv-on-gcloud.appspot.com/products/create', json=datos)
            print("respuesta: " + registro.text)    
        return listpets("Mascota registrada correctamente")
    print("desplegando webpage de registro de mascota")
    return render_template('home/nuevamascota.html', title="Registro")



@home.route('/listusers')
def listusers():
    users = requests.get('http://petstorecustomer.appspot.com/list/all').json()
    print(users)
    return render_template('home/users.html', title="Lista Ususarios", users=users)


@home.route('/listpets')
def listpets(message=None):
    pets = requests.get('http://practiceiv-on-gcloud.appspot.com/products/fetch').json()['products']
    print(pets)
    return render_template('home/pets.html', title="Lista Mascotas", pets=pets, message=message)


@home.route('/shoppingcart')
def shoppingcart(message=None):
    req_pets = requests.get('http://studentestwebapp.azurewebsites.net/api/list/'+session['sess_loged_userphone'])
    while req_pets.status_code != 200:
        print(str(req_pets))
        print("Otra vez...")
        req_pets = requests.get('http://studentestwebapp.azurewebsites.net/api/list/'+session['sess_loged_userphone'])
    print(req_pets.json()['json_list'])
    mmss = message
    pets = []
    for petcart in req_pets.json()['json_list']:
        print(petcart)
        pc_req = requests.get('http://practiceiv-on-gcloud.appspot.com/products/get/id/'+str(petcart['id_pet']))
        if pc_req.status_code == 404:
            mmss += " - Carrito modificado por problemas de stock \n"
            eliminaitem(session['sess_loged_userphone'], petcart['id_pet'])
        else:
            pcrejson = pc_req.json() 
            print(str(pcrejson))
            if pcrejson['stock'] < petcart['cant']:
                modificacant(session['sess_loged_userphone'], petcart["id_pet"], pcrejson["stock"])
                petcart['cant'] = pcrejson['stock']
                mmss = "El carrito de compra se ha actualizado por stock."
            petcart['breed'] = pcrejson['breed']
            petcart['specie'] = pcrejson['specie']
            pets.append(petcart)
    return render_template('home/shoppingcart.html', title="Carrito de compra", pets=pets, message=mmss)

@home.route('/checkout')
def checkout():
    print("Solicitando la compra!...")
    """
    Validar stock de los items en el carrito de compra
    """
    shCarts = requests.get('http://studentestwebapp.azurewebsites.net/api/list/'+session['sess_loged_userphone']).json()['json_list']
    pets = requests.get('http://practiceiv-on-gcloud.appspot.com/products/fetch').json()['products']
    suma = 0
    cantidadmascotas = 0
    mascotas = []
    actualizastock = []
    print("Carrito:")
    for cart in shCarts:
        for pet in pets:
            if cart["id_pet"] == pet["id"]:
                print(str(cart))
                print(str(pet))
                mascotas.append({'pet_species':pet["specie"], 'pet_breed':pet["breed"], 'pet_amount':cart["cant"], 'pet_price':pet["price"]})
                if cart["cant"] <= pet["stock"]:
                    print("Stock OK")
                    suma += (cart["cant"] * pet["price"])
                    nuevostock = pet["stock"] - cart["cant"]
                    actualizastock.append({'id':pet["id"], 'stock':nuevostock})
                    break
                else:
                    print("Problemas de stock con mascota" + str(pet["id"]))
                    modificacant(cart["id_user"], cart["id_pet"], pet["stock"])
                    return shoppingcart("El carrito de compra se ha actualizado por stock")
    print("suma: " + str(suma))
    print("mascotas cant: " + str(len(mascotas)))
    user = requests.get('http://petstorecustomer.appspot.com/list/byphone/'+session['sess_loged_userphone']).json()
    if suma <= user[0]["credit"] and len(mascotas) > 0:
        """
        Solicitar orden
        """
        uname = session['sess_loged_username']
        uphone = session['sess_loged_userphone']
        uaddress = session['sess_loged_useraddress']
        data_orden = {'address':uaddress, 'name':uname, 'phone':uphone, 'pets':mascotas}
        print(data_orden)
        req_orden = requests.post('http://petstoreorder.appspot.com/create/order', json=data_orden)
        print("solicitando orden ...")
        while req_orden.status_code != 200:
            print(str(req_orden))
            print("Otra vez...")
            req_orden = requests.post('http://petstoreorder.appspot.com/create/order', json=data_orden)
        """
        Vaciar carro
        """
        for cart in shCarts:
            eliminaitem(cart["id_user"], cart["id_pet"])
        """
        Reducir mascotas (servicio falla -> eliminar crear)
        """
        print("Reduciendo stock mascotas")
        for actstock in actualizastock:
            print(str(actstock))
            req_updatestock = requests.post('http://practiceiv-on-gcloud.appspot.com/products/update', json=actstock)
            while req_updatestock.status_code != 200:
                print(str(req_updatestock))
                print("Otra vez...")
                req_updatestock = requests.post('http://practiceiv-on-gcloud.appspot.com/products/update', json=actstock)
        """
        Reducir monto de la compra al usuario
        """
        print("Reduciendo monto al cliente"+str(int(suma)))
        print('http://petstorecustomer.appspot.com/pay/'+str(int(suma))+'/by-customer-with-phone/'+uphone)
        req_creditupdate = requests.get('http://petstorecustomer.appspot.com/pay/'+str(int(suma))+'/by-customer-with-phone/'+uphone)
        print(str(req_creditupdate))
        while req_creditupdate.status_code != 200:
            print("Otra vez...")
            req_creditupdate = requests.get('http://petstorecustomer.appspot.com/pay/'+str(int(suma))+'/by-customer-with-phone/'+uphone)
        print("Orden exitosa:")
        print(str(req_creditupdate))
        print(req_creditupdate.text)
        return render_template('home/ordendecompra.html', title="Orden de Compra", message="Compra realizada correctamente.", mascotas=mascotas, total=int(suma))
    if suma > user[0]["credit"]:
        print("Usuario sin saldo suficiente")
        return shoppingcart("Venta no se pudo realizar, saldo insuficiente")
    print("Mascotas en el carro = 0")
    return shoppingcart()

@home.route('/orders')
def orders():
    req_orders = requests.get('http://petstoreorder.appspot.com/list/orders/all')
    print(req_orders.text)
    userorders = []
    for order in req_orders.json():
        if order['customer_phone'] == int(session['sess_loged_userphone']):
            print("orden de usuario entcontrada: " + str(order))
            userorders.append(order)
    return render_template('home/ordenes.html', title="Ordenes de Compra", orders=userorders)

@home.route('/orderat/<fechahora>')
def orderat(fechahora=None):
    if fechahora is None:
        return listpets()
    order_req = requests.get('http://petstoreorder.appspot.com/list/pets/orderedby/'+session['sess_loged_userphone']+'/at/'+fechahora)
    orderjson = order_req.json()
    total = 0
    for pet in orderjson:
        total = total + (pet['pet_amount'] * pet['pet_price'])
    return render_template('home/ordendecompra.html', title="Orden de Compra", mascotas=orderjson, total=int(total), fechahora=fechahora)



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
    return listpets("La mascota ha sido agregada al carrito")


@home.route('/deletepet/<idpet>')
def deletepet(idpet):
    carrito = ShoppingCart.query.filter_by(id_user=session['sess_loged_userphone'], id_pet=idpet).first()
    if carrito is None:
        return shoppingcart("El carrito de compras ha sido actualizado.")
    carrito.delete()
    return shoppingcart("El carrito de compras ha sido actualizado.")


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


