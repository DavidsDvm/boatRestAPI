from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import models


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://xwmwjeubxgtphj:f4814208adbb2d1999d1bad5d5f8c6d03912cc61fc0bafb5644e95e4151b93da@ec2-18-208-24-104.compute-1.amazonaws.com:5432/d1g8oof4s9nh1u'
app.config['JSON_SORT_KEYS']=False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
models.db.init_app(app)
models.ma.init_app(app)

@app.route('/api/Boat/all')
def boatAll():
    all_boat = models.Boat.query.all()
    task_Schema = models.BoatSchema(many=True)
    output = task_Schema.dump(all_boat)

    for i in  output:
        if isinstance(i['category'], int):
            categoria = models.Category.query.filter(models.Category.id == i['category'])

            task_Schema1 = models.CategorySchema(exclude=('boats',), many=True)
            output1 = task_Schema1.dump(categoria)

            i['category'] = output1[0]

    return jsonify(output)

@app.route('/api/Boat/save', methods=['POST'])
def boatSave():
    brand = request.json['brand']
    year = request.json['year']
    name = request.json['name']
    description = request.json['description']
    category = request.json['category'].get('id')

    newBoat = models.Boat(name, brand, year, description, category)

    models.db.session.add(newBoat)
    models.db.session.commit()

    return jsonify()

@app.route('/api/Boat/update', methods=['PUT'])
def boatUpdate():
    id = request.json['id']
    brand = request.json['brand']
    name = request.json['name']
    description = request.json['description']
    year = request.json['year']

    boatActual = models.Boat.query.filter(models.Boat.id == id).first()

    boatActual.id = id
    boatActual.brand = brand
    boatActual.name = name
    boatActual.description = description
    boatActual.year = year

    models.db.session.commit()

    return jsonify()

@app.route('/api/Boat/<int:id>', methods=['DELETE'])
def boatDelete(id):

    boatActual = models.Boat.query.filter(models.Boat.id == id).first()

    models.db.session.delete(boatActual)
    models.db.session.commit()

    return jsonify()

@app.route('/api/Client/all')
def clientAll():
    all_clients = models.Client.query.all()
    task_Schema = models.ClientSchema(many=True)
    output = task_Schema.dump(all_clients)

    return jsonify(output)

@app.route('/api/Client/save', methods=['POST'])
def clientSave():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    age = request.json['age']

    newClient = models.Client(name, email, password, age)

    models.db.session.add(newClient)
    models.db.session.commit()

    return jsonify()

@app.route('/api/Client/update', methods=['PUT'])
def clientUpdate():
    idClient = request.json['idClient']
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    age = request.json['age']

    clientActual = models.Client.query.filter(models.Client.idClient == idClient).first()

    clientActual.idClient = idClient
    clientActual.name = name
    clientActual.email = email
    clientActual.password = password
    clientActual.age = age

    models.db.session.commit()

    return jsonify()

@app.route('/api/Client/<int:id>', methods=['DELETE'])
def clientDelete(id):

    clientActual = models.Client.query.filter(models.Client.idClient == id).first()

    models.db.session.delete(clientActual)
    models.db.session.commit()

    return jsonify()

@app.route('/api/Category/all')
def categoryAll():
    all_reservations = models.Category.query.all()
    task_Schema = models.CategorySchema(many=True)
    output = task_Schema.dump(all_reservations)

    return jsonify(output)

@app.route('/api/Category/save', methods=['POST'])
def categorySave():
    name = request.json['name']
    description = request.json['description']

    newClient = models.Category(name, description)

    models.db.session.add(newClient)
    models.db.session.commit()

    return jsonify()

@app.route('/api/Category/update', methods=['PUT'])
def categoryUpdate():
    id = request.json['id']
    name = request.json['name']
    description = request.json['description']

    categoryActual = models.Category.query.filter(models.Category.id == id).first()

    categoryActual.id = id
    categoryActual.name = name
    categoryActual.description = description

    models.db.session.commit()

    return jsonify()

@app.route('/api/Category/<int:id>', methods=['DELETE'])
def categoryDelete(id):

    categoryActual = models.Category.query.filter(models.Category.id == id).first()

    models.db.session.delete(categoryActual)
    models.db.session.commit()

    return jsonify()

if __name__ == '__main__':
    app.app_context().push()
    models.db.create_all()
    app.run(host='0.0.0.0', port=80)