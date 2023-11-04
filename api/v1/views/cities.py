#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.city import City
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_citie(state_id):
    """list all cities in state"""
    outp = []
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if request.method == 'GET':
        for city in state.cities:
            outp.append(city.to_dict())
        return (jsonify(outp))

    if request.method == 'POST':
        datax = request.get_json()

        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")

        datax['state_id'] = state_id
        city = City(**datax)
        city.save()

        return (jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT'],
                 strict_slashes=False)
def city(city_id):
    """list a city by id"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if request.method == 'GET':
        outp = city.to_dict()
        return (jsonify(outp))
    if request.method == 'PUT':
        datax = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")

        for key, value in datax.items():
            setattr(city, key, value)
        city.save()

        return (jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=["GET", "DELETE"],
                 strict_slashes=False)
def del_city(city_id):
    """ delete one unique city object """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    res = make_response(jsonify({}), 200)
    return res
