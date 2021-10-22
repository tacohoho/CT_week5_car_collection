from flask import Blueprint, request, jsonify
from car_collection.helpers import token_required
from car_collection.models import Car, db, Car_schema, Cars_schema

api = Blueprint('api', __name__, url_prefix='/api')

# CREATE ENDPOINT
@api.route('/cars', methods=['POST'])
@token_required
def create_drone(current_user_token):
    make = request.json['make']
    model = request.json['model']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_prod = request.json['cost_of_prod']
    token = current_user_token.token

    print(f'TEST: {current_user_token.token}')

    car = Car(make,model,max_speed,dimensions, weight,cost_of_prod, user_token = token)

    db.session.add(car)
    db.session.commit()

    response = Car_schema.dump(car)
    return jsonify(response)

# RETRIEVE ROUTES
# Retrive all cars associated w/ user token
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = Cars_schema.dump(cars)
    return jsonify(response)

# Retrieve 1 car (by ID) associated w/ user token
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    car = Car.query.get(id)
    if car:
        print(f'Here is your car: {car.name}')
        response = Car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That drone does not exist!'})


# Update a single car by ID
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    print(car)
    if car:
        car.make = request.json['make']
        car.model = request.json['name']
        car.max_speed = request.json['max_speed']
        car.dimensions = request.json['dimensions']
        car.weight = request.json['weight']
        car.cost_of_prod = request.json['cost_of_prod']
        car.user_token = current_user_token.token
        db.session.commit()

        response = Car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That car does not exist!'})


# DELETE ROUTE
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return jsonify({'Success': f'car ID #{car.id} has been deleted'})
    else:
        return jsonify({'Error': 'That car does not exist!'})