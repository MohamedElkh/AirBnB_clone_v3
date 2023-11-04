#!/usr/bin/python3
""" func to place view """
from models import storage
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models.base_model import BaseModel


@app_views.route('/cities/<city_id>/places', methods=["GET", "POST"],
                 strict_slashes=False)
def get_c_place(city_id):
    """ gets all place objs of a city """
    outp = []
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    if request.method == "GET":
        for place in city.places:
            outp.append(place.to_dict())
        return (jsonify(outp))

    if request.method == "POST":
        datax = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'user_id' not in request.json:
            abort(400, description="Missing user_id")

        user_id = datax['user_id']
        user = storage.get(User, user_id)

        if user is None:
            abort(404)
        if 'name' not in request.json:
            abort(400, description="Missing name")

        datax['city_id'] = city_id
        place = Place(**datax)
        place.save()
        return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=[
                 "GET", "PUT", "DELETE"], strict_slashes=False)
def get_place(place_id):
    """ retrieves one unique place object """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if request.method == "GET":
        outp = place.to_dict()
        return (jsonify(outp))

    if request.method == "PUT":
        datax = request.get_json()

        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in datax.items():
            setattr(place, key, value)
        place.save()
        return (jsonify(place.to_dict()), 200)

    if request.method == "DELETE":
        storage.delete(place)
        storage.save()

        res = make_response(jsonify({}), 200)
        return res
