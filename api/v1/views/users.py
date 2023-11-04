#!/usr/bin/python3
""" func to user view """
from models import storage
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models.user import User
from models.base_model import BaseModel


@app_views.route('/users', methods=["GET", "POST"],
                 strict_slashes=False)
def get_all():
    """ func to retrieves all user objects """
    outp = []
    users = storage.all(User).values()

    if request.method == "GET":
        for user in users:
            outp.append(user.to_dict())
        return (jsonify(outp))

    if request.method == "POST":
        datax = request.get_json()

        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'email' not in request.json:
            abort(400, description="Missing email")
        if 'password' not in request.json:
            abort(400, description="Missing password")

        user = User(**datax)
        user.save()
        return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def get_user(user_id):
    """ func to retrieves one unique user object """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    if request.method == "GET":
        outp = user.to_dict()
        return (jsonify(outp))

    if request.method == "PUT":
        datax = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")

        for key, value in datax.items():
            setattr(user, key, value)
        user.save()
        return (jsonify(user.to_dict()), 200)

    if request.method == "DELETE":
        storage.delete(user)
        storage.save()

        res = make_response(jsonify({}), 200)
        return res
