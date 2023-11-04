#!/usr/bin/python3
"""func to reviews"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models.review import Review
from models.place import Place
from models.user import User
from models.base_model import BaseModel


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_review(place_id):
    """func list all reviews in place"""
    outp = []
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if request.method == 'GET':
        for onePl in place.reviews:
            outp.append(onePl.to_dict())
        return (jsonify(outp))

    if request.method == 'POST':
        datax = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'user_id' not in request.json:
            abort(400, description="Missing user_id")

        user_id = datax['user_id']
        user = storage.get(User, user_id)

        if user is None:
            abort(404)
        if 'text' not in request.json:
            abort(400, description="Missing text")

        datax['place_id'] = place_id
        review = Review(**datax)
        review.save()
        return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=[
                 'GET', 'PUT', 'DELETE'], strict_slashes=False)
def review(review_id):
    """func to list a review by id"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    if request.method == 'GET':
        outp = review.to_dict()
        return (jsonify(outp))

    if request.method == 'PUT':
        datax = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")

        for key, value in datax.items():
            setattr(review, key, value)
        review.save()

        return (jsonify(review.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()

        res = make_response(jsonify({}), 200)
        return res
