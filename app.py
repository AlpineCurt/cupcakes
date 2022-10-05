"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'oh-so-secret'

connect_db(app)

@app.route("/api/cupcakes")
def get_all_cupcakes():
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:id>")
def get_single_cupcake(id):
    cupcake=Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    cupcake = request.get_json()
    errored = False
    if "flavor" not in cupcake.keys():
        cupcake['flavor'] = "Error:  'flavor' is required."
        errored = True
    if "size" not in cupcake.keys():
        cupcake['size'] = "Error:  'size' is required."
        errored = True
    if "rating" not in cupcake.keys():
        cupcake['rating'] = "Error:  'rating' is required."
        errored = True
    if errored:
        response_json = jsonify(cupcake=cupcake)
        return (response_json, 400)

    new_cupcake=Cupcake(
        flavor=cupcake["flavor"],
        size=cupcake["size"],
        rating=cupcake["rating"],
        )
    if "image" in cupcake:
        new_cupcake.image = cupcake["image"]

    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(new_cupcake.serialize())
    return (response_json, 201)