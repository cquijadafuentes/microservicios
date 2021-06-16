from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://petstoreadmin:Pet_Store@db-microservices-petstore:3306/petstore'
db = SQLAlchemy(app)



###Models####
class Carrito(db.Model):
    __tablename__ = "carritos"
    id = db.Column(db.Integer, primary_key=True)
    idmascota = db.Column(db.Integer)
    idusuario = db.Column(db.Integer)
    preciounidad = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,title,productDescription,productBrand,price):
        self.idmascota = idmascota
        self.idusuario = idusuario
        self.preciounidad = preciounidad
        self.cantidad = cantidad
    def __repr__(self):
        return '' % self.id
db.create_all()



class CarritoSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Carrito
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    idmascota = fields.Number(required=True)
    idusuario = fields.Number(required=True)
    preciounidad = fields.Number(required=True)
    cantidad = fields.Number(required=True)



@app.route('/carritos', methods = ['GET'])
def index():
    get_carritos = Carrito.query.all()
    carrito_schema = CarritoSchema(many=True)
    carritos = carrito_schema.dump(get_carritos)
    return make_response(jsonify({"carrito": carritos}))


