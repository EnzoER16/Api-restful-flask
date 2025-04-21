from flask import Blueprint, jsonify, request
from models.vehicle import Vehicle
from models.db import db
from sqlalchemy.exc import IntegrityError

vehicle = Blueprint('vehicle', __name__)

@vehicle.route('/api/vehicles')
def get_vehicle():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles])

@vehicle.route('/api/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['brand', 'model', 'number_plate']):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    try:
        print(f"Datos recibidos: {data}")

        new_vehicle = Vehicle(data['brand'], data['model'], data['number_plate'])
        print(f"Creando vehiculo: {new_vehicle.brand}, {new_vehicle.model}, {new_vehicle.number_plate}")

        db.session.add(new_vehicle)
        db.session.commit()

        return jsonify({'message': 'Vehiculo agregado exitosamente', 'vehicle': new_vehicle.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'El vehiculo ya está registrado'}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error inesperado: {e}")
        return jsonify({'error': 'Error al agregar el vehiculo'}), 500

@vehicle.route("/api/del_vehicle/<int:id>", methods=['DELETE'])
def delete_vehicle(id):
    vehicle = Vehicle.query.get(id)
    
    if not vehicle: 
        return jsonify({'message':'Vehiculo no encontrado'}), 404 
    try:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({'message': 'Vehiculo borrado exitosamente!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500

@vehicle.route('/api/up_vehicle/<int:id>', methods=['PUT'])
def update_vehicle(id):

    data = request.get_json()

    if not data:
        return jsonify({'error':'No se recibieron datos'}, 400)
    
    vehicle = Vehicle.query.get(id)

    if not vehicle:
        return jsonify({'error': 'Vehiculo no encontrado'}), 404
    
    try:
        if "brand" in data:
            vehicle.brand = data['brand']
        if 'model' in data:
            vehicle.model = data['model']
        if 'number_plate' in data:
            vehicle.number_plate = data['number_plate']

        db.session.commit()

        return jsonify({'message':'Vehiculo actualizado correctamente', 'vehicle': vehicle.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@vehicle.route('/api/update_vehicle/<int:id>', methods=['PATCH'])
def patch_vehicle(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    vehicle = Vehicle.query.get(id)
    
    if not vehicle:
        return jsonify({'error': 'Vehiculo no encontrado'}), 404

    try:
        if 'brand' in data and data['brand']:
            vehicle.brand = data['brand']
        if 'model' in data and data['model']:
            vehicle.model = data['model']
        if 'number_plate' in data and data['number_plate']:
            vehicle.daout_datete = data['number_plate']

        db.session.commit()
        return jsonify({'message': 'Vehiculo actualizado correctamente', 'vehicle': vehicle.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500