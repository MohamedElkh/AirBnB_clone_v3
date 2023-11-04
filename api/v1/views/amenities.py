#!/usr/bin/python3
""" amenities """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def get_all():
    """ retrieves all amenity objects """
    outp = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        outp.append(amenity.to_dict())
    return (jsonify(outp))


@app_views.route('/amenities', methods=["GET", "POST"], strict_slashes=False)
def create():
    """creates a new amenity """
    datax = request.get_json()

    if not request.is_json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")

    amenity = Amenity(**datax)
    amenity.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=[
                 "GET", "PUT"], strict_slashes=False)
def get_amenity(amenity_id):
    """ retrieves one unique amenity object """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)
    if request.method == "GET":
        outp = amenity.to_dict()
        return (jsonify(outp))

    if request.method == "PUT":
        datax = request.get_json()

        if not request.is_json:
            abort(400, description="Not a JSON")

        for key, value in datax.items():
            setattr(amenity, key, value)
        amenity.save()
        return (jsonify(amenity.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=["GET", "DELETE"],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ deletes one unique amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    res = make_response(jsonify({}), 200)
    return res
