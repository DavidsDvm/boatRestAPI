from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

db = SQLAlchemy()
ma = Marshmallow()

class Boat(db.Model):
    __tablename__ = 'Boat'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    brand = db.Column(db.String(45))
    year = db.Column(db.Integer)
    description = db.Column(db.String(250))

    # Relations
    category = db.Column(db.Integer, db.ForeignKey('Category.id'))

    def __init__(self, name, brand, year, description, category):
        self.name = name
        self.brand = brand
        self.year = year
        self.description = description
        self.category = category

class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    description = db.Column(db.String(250))

    # Relations
    boats = db.relationship('Boat')

    def __init__(self, name, description):
        self.name = name
        self.description = description

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "name", "description", "boats")
        ordered = True

class BoatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "name", "brand", "year", "description", "category", "messages", "reservations")
        ordered = True

class Client(db.Model):
    __tablename__ = 'Client'
    idClient = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(250))
    age = db.Column(db.Integer)

    def __init__(self, name, email, password, age):
        self.name = name
        self.email = email
        self.password = password
        self.age = age

class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("idClient", "email", "password", "name", "age", "messages", "reservations")
        ordered = True

class Messages(db.Model):
    __tablename__ = 'Massages'
    id = db.Column(db.Integer, primary_key=True)
    boat_id = db.Column(db.Integer, db.ForeignKey("Boat.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("Client.idClient"))

    boat = db.relationship("Boat", backref="messages")
    client = db.relationship("Client", backref="messages")

class MessagesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Messages
        include_fk = True

class Reservations(db.Model):
    __tablename__ = 'Reservations'
    idReservation = db.Column(db.Integer, primary_key=True)
    startDate = db.Column(db.DateTime)
    devolutionDate = db.Column(db.DateTime)
    status = db.Column(db.String(45))
    score = db.Column(db.Integer)

    # foraneas
    boat = db.Column(db.Integer, db.ForeignKey("Boat.id"))
    client = db.Column(db.Integer, db.ForeignKey("Client.idClient"))

    boat_id = db.relationship("Boat", backref="reservations")
    client_id = db.relationship("Client", backref="reservations")

    def __init__(self, startDate, devolutionDate, status, score, boat, client):
        self.startDate = startDate
        self.devolutionDate = devolutionDate
        self.status = status
        self.score = score
        self.boat = boat
        self.client = client

class ReservationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("idReservation", "startDate", "devolutionDate", "status", "boat", "client", "score")
        ordered = True
    