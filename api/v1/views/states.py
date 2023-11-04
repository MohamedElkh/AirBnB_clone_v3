#!/usr/bin/python3
"""func to state view """
from models import storage
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states', methods=["GET", "POST"], strict_slashes=False)
def get_all_st():
    """ func to retrieves all state objects """
    if request.method == 'GET':
        outp = []
        states = storage.all(State).values()

        for state in states:
            outp.append(state.to_dict())
        return (jsonify(outp))

    if request.method == 'POST':
        datax = request.get_json()

        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")

        state = State(**datax)
        state.save()
        return (jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["GET", "PUT"],
                 strict_slashes=False)
def get_state(state_id):
    """ func to retrieves one unique state object """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if request.method == "GET":
        outp = state.to_dict()
        return (jsonify(outp))

    if request.method == "PUT":
        print("test\n")
        datax = request.get_json()

        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, val in datax.items():
            setattr(state, key, val)
        state.save()

        return (jsonify(state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=["GET", "DELETE"],
                 strict_slashes=False)
def del_state(state_id):
    """ func to delete one unique state object """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    res = make_response(jsonify({}), 200)
    return res
