"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap

app = Flask(__name__)
app.url_map.strict_slashes = False

CORS(app)

# In-memory storage
people_storage = {}
planets_storage = {}
users_storage = {}
favorites_storage = {}

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    response = requests.get('https://swapi.py4e.com/api/people/')
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from SWAPI"}), response.status_code
    data = response.json()
    return jsonify(data['results']), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    response = requests.get(f'https://swapi.py4e.com/api/people/{people_id}/')
    if response.status_code != 200:
        return jsonify({"error": "Person not found"}), response.status_code
    data = response.json()
    return jsonify(data), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    response = requests.get('https://swapi.py4e.com/api/planets/')
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from SWAPI"}), response.status_code
    data = response.json()
    return jsonify(data['results']), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    response = requests.get(f'https://swapi.py4e.com/api/planets/{planet_id}/')
    if response.status_code != 200:
        return jsonify({"error": "Planet not found"}), response.status_code
    data = response.json()
    return jsonify(data), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = [
        {"id": 1, "name": "Andres", "email": "123@gmail.com"},
        {"id": 2, "name": "Torres", "email": "456@gmail.com"}
    ]
    return jsonify(users), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = favorites_storage.get(user_id, [])
    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['POST', 'DELETE'])
def manage_favorite_planet(user_id, planet_id):
    user_favorites = favorites_storage.setdefault(user_id, [])

    if request.method == 'POST':
        if planet_id not in user_favorites:
            user_favorites.append(planet_id)
            return jsonify({"msg": "Favorite added"}), 201
        return jsonify({"msg": "Favorite already exists"}), 200

    if request.method == 'DELETE':
        if planet_id in user_favorites:
            user_favorites.remove(planet_id)
            return jsonify({"msg": "Favorite removed"}), 204
        return jsonify({"msg": "Favorite not found"}), 404

@app.route('/favorite/people/<int:user_id>/<int:people_id>', methods=['POST', 'DELETE'])
def manage_favorite_people(user_id, people_id):
    user_favorites = favorites_storage.setdefault(user_id, [])

    if request.method == 'POST':
        if people_id not in user_favorites:
            user_favorites.append(people_id)
            return jsonify({"msg": "Favorite added"}), 201
        return jsonify({"msg": "Favorite already exists"}), 200

    if request.method == 'DELETE':
        if people_id in user_favorites:
            user_favorites.remove(people_id)
            return jsonify({"msg": "Favorite removed"}), 204
        return jsonify({"msg": "Favorite not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
