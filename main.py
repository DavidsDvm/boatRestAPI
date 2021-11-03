from typing import OrderedDict
from flask import Flask, jsonify, request, Response
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from decouple import config as config_decouple
import os

import models


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost/mintic'
app.config['JSON_SORT_KEYS']=False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

if config_decouple('PRODUCTION', default=False):
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://xwmwjeubxgtphj:f4814208adbb2d1999d1bad5d5f8c6d03912cc61fc0bafb5644e95e4151b93da@ec2-18-208-24-104.compute-1.amazonaws.com:5432/d1g8oof4s9nh1u'

models.db.init_app(app)
models.ma.init_app(app)

@app.route('/api/Boat/all')
def boatAll():
    all_boat = models.Boat.query.all()
    task_Schema = models.BoatSchema(many=True)
    output = task_Schema.dump(all_boat)

    for i in output:
        if isinstance(i['category'], int):
            categoria = models.Category.query.filter(models.Category.id == i['category'])

            task_Schema1 = models.CategorySchema(exclude=('boats',), many=True)
            output1 = task_Schema1.dump(categoria)

            i['category'] = output1[0]
        
        # Get the reservation in case that there are some reservations for this boat
        if i['reservations'] != []:
            newReservation = []
            for j in i['reservations']:
                reservation = models.Reservations.query.filter(models.Reservations.idReservation == j.idReservation).first()
                task_SchemaReservation = models.ReservationsSchema(many=False)
                outputReservation = task_SchemaReservation.dump(reservation)

                newReservation.append(outputReservation)
            print(newReservation)
            i['reservations'] = newReservation

    return jsonify(output)

@app.route('/api/Boat/save', methods=['POST'])
def boatSave():
    brand = request.json['brand']
    year = request.json['year']
    name = request.json['name']
    description = request.json['description']
    if 'category' in request.json:
        category = request.json['category'].get('id')
    else:
        category = None


    newBoat = models.Boat(name, brand, year, description, category)

    models.db.session.add(newBoat)
    models.db.session.commit()

    status_code = Response(status=201)
    return status_code

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

    status_code = Response(status=201)
    return status_code

@app.route('/api/Boat/<int:id>', methods=['DELETE'])
def boatDelete(id):

    boatActual = models.Boat.query.filter(models.Boat.id == id).first()

    models.db.session.delete(boatActual)
    models.db.session.commit()

    status_code = Response(status=204)
    return status_code

@app.route('/api/Client/all')
def clientAll():
    all_clients = models.Client.query.all()
    task_Schema = models.ClientSchema(many=True)
    output = task_Schema.dump(all_clients)

    for i in output:
        # Get the reservation in case that there are some reservations for this boat
        if i['reservations'] != []:
            newReservation = []
            for j in i['reservations']:
                reservation = models.Reservations.query.filter(models.Reservations.idReservation == j.idReservation).first()
                task_SchemaReservation = models.ReservationsSchema(many=False)
                outputReservation = task_SchemaReservation.dump(reservation)

                newReservation.append(outputReservation)
            print(newReservation)
            i['reservations'] = newReservation

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

    status_code = Response(status=201)
    return status_code

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

    status_code = Response(status=201)
    return status_code

@app.route('/api/Client/<int:id>', methods=['DELETE'])
def clientDelete(id):

    clientActual = models.Client.query.filter(models.Client.idClient == id).first()

    models.db.session.delete(clientActual)
    models.db.session.commit()

    status_code = Response(status=204)
    return status_code

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

    status_code = Response(status=201)
    return status_code

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

    status_code = Response(status=201)
    return status_code

@app.route('/api/Category/<int:id>', methods=['DELETE'])
def categoryDelete(id):

    categoryActual = models.Category.query.filter(models.Category.id == id).first()

    models.db.session.delete(categoryActual)
    models.db.session.commit()

    status_code = Response(status=204)
    return status_code

@app.route('/api/Reservation/all')
def reservationAll():
    all_reservations = models.Reservations.query.all()
    task_Schema = models.ReservationsSchema(many=True)
    output = task_Schema.dump(all_reservations)

    # The objetive of this code is to get the id of a boat and a client and then json the data of that client and boat on the reservation json
    for i in output:
        if isinstance(i['boat'], int):
            boat = models.Boat.query.filter(models.Boat.id == i['boat'])

            task_Schema1 = models.BoatSchema(exclude=('reservations',), many=True)
            output1 = task_Schema1.dump(boat)

            i['boat'] = output1[0]

        if isinstance(i['client'], int):
            client = models.Client.query.filter(models.Client.idClient == i['client'])

            task_Schema2 = models.ClientSchema(exclude=('reservations', 'messages',), many=True)
            output2 = task_Schema2.dump(client)

            i['client'] = output2[0]

        # then after that will add '+00:00' at the end of the dates (because the date is in the format '%Y-%m-%dT%H:%M:%S.%f+00:00')
        i['startDate'] = i['startDate'] + '.000+00:00'
        i['devolutionDate'] = i['devolutionDate'] + '.000+00:00'

    return jsonify(output)

@app.route('/api/Reservation/save', methods=['POST'])
def reservationSave():
    startDate = request.json['startDate']
    devolutionDate = request.json['devolutionDate']
    status = request.json['status']
    score = None

    if 'boat' in request.json:
        boat = request.json['boat'].get('id')
    else:
        boat = None

    if 'client' in request.json:
        client = request.json['client'].get('idClient')
    else:
        client = None

    newReservation = models.Reservations(startDate, devolutionDate, status, score, boat, client)

    models.db.session.add(newReservation)
    models.db.session.commit()

    status_code = Response(status=201)
    return status_code

@app.route('/api/Reservation/report-dates/<startDate>/<devolutionDate>', methods=['GET'])
def reservationReport(startDate, devolutionDate):
    all_reservations = models.Reservations.query.filter(models.Reservations.startDate >= startDate, models.Reservations.devolutionDate <= devolutionDate).all()
    task_Schema = models.ReservationsSchema(many=True)
    output = task_Schema.dump(all_reservations)

    # The objetive of this code is to get the id of a boat and a client and then json the data of that client and boat on the reservation json
    for i in output:
        if isinstance(i['boat'], int):
            boat = models.Boat.query.filter(models.Boat.id == i['boat'])

            task_Schema1 = models.BoatSchema(exclude=('reservations',), many=True)
            output1 = task_Schema1.dump(boat)

            i['boat'] = output1[0]

        if isinstance(i['client'], int):
            client = models.Client.query.filter(models.Client.idClient == i['client'])

            task_Schema2 = models.ClientSchema(exclude=('reservations', 'messages',), many=True)
            output2 = task_Schema2.dump(client)

            i['client'] = output2[0]

        # then after that will add '+00:00' at the end of the dates (because the date is in the format '%Y-%m-%dT%H:%M:%S.%f+00:00')
        i['startDate'] = i['startDate'] + '.000+00:00'
        i['devolutionDate'] = i['devolutionDate'] + '.000+00:00'

    return jsonify(output)

@app.route('/api/Reservation/report-status', methods=['GET'])
def reservationReportStatus():
    all_reservations = models.Reservations.query.all()
    completed = 0
    cancelled = 0

    for i in all_reservations:
        if i.status == 'completed':
            completed += 1
        elif i.status == 'cancelled':
            cancelled += 1

    return jsonify({'completed': completed, 'cancelled': cancelled})

@app.route('/api/Reservation/report-clients', methods=['GET'])
def reservationReportClients():
    all_clients = models.Client.query.all()
    task_Schema = models.ClientSchema(many=True)
    output = task_Schema.dump(all_clients)
    totalOutput = []

    for i in output:
        data = OrderedDict()
        data['total'] = 0

        # Get the reservation in case that there are some reservations for this boat
        if i['reservations'] != []:
            newReservation = []
            for j in i['reservations']:
                data['total'] += 1
                reservation = models.Reservations.query.filter(models.Reservations.idReservation == j.idReservation).first()
                task_SchemaReservation = models.ReservationsSchema(many=False, exclude=('client',))
                outputReservation = task_SchemaReservation.dump(reservation)

                # Boat access
                if isinstance(outputReservation['boat'], int):
                    boat = models.Boat.query.filter(models.Boat.id == outputReservation['boat']).first()

                    task_Schema1 = models.BoatSchema(exclude=('reservations',), many=False)
                    output1 = task_Schema1.dump(boat)

                    outputReservation['boat'] = output1

                newReservation.append(outputReservation)
            i['reservations'] = newReservation

            # then after that will add '+00:00' at the end of the dates (because the date is in the format '%Y-%m-%dT%H:%M:%S.%f+00:00')
            i['reservations'][0]['startDate'] = i['reservations'][0]['startDate'] + '.000+00:00'
            i['reservations'][0]['devolutionDate'] = i['reservations'][0]['devolutionDate'] + '.000+00:00'

        # First we create total where we put the number of reservations for this client after that we add the client and the reservations
        data['client'] = i
        totalOutput.append({**data})

    return jsonify(totalOutput)

if __name__ == '__main__':
    app.app_context().push()
    models.db.create_all()

    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port, debug=1)