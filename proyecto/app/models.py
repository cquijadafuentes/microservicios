# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Student(UserMixin, db.Model):
    """
    Create an Student table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    programa_id = db.Column(db.Integer, db.ForeignKey('programas.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Student: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


class Programa(db.Model):
    """
    Create a Programa table
    """

    __tablename__ = 'programas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    students = db.relationship('Student', backref='programa',
                                lazy='dynamic')

    def __repr__(self):
        return '<Programa: {}>'.format(self.name)


class ShoppingCart(db.Model):
    """
    Create a ShoppingCart table
    """

    __tablename__ = 'shoppingcarts'

    id_user = db.Column(db.Integer, primary_key=True)
    id_pet = db.Column(db.Integer, primary_key=True)
    cant = db.Column(db.Integer)
    unitprice = db.Column(db.Integer)

    def __repr__(self):
        return "<ShoppingCart(id_user='%s', id_pet='%s', cant='%s', unitprice='%s')>" % (
                                self.id_user, self.id_pet, self.cant, self.unitprice)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id_user' : self.id_user,
           'id_pet' : self.id_pet,
           'cant' : self.cant,
           'unitprice' : self.unitprice
       }

    def update(self):
        print("Ingresando al update de ShoppingCart")
        return self

    def add(self):
        print("Ingresando al add de ShoppingCart")
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        print("Ingresando al udpate de ShoppingCart")
        db.session.commit()
        return self

    def delete(self):
        print("Ingresando al delete de ShoppingCart")
        db.session.delete(self)
        db.session.commit()
        return self

