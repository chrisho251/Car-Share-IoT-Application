from flask import Flask, Blueprint, request, jsonify, render_template, url_for, json, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import currrent_app as app
import os, requests, json, sys, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename
from schema import *

app = Flask(__name__)
api = Blueprint("api",__name__)


@api.route("/api/getcars", methods=["GET"])
def get_all_cars():
    
    car = Car.query.filter(Car.availability == True)

    return carSchema.jsonify(car)

 
@api.route("/api/cars/<carid>", methods=["GET"])
def get_cars_by_id(carid):
    
    car = Car.query.get(id)
    
    return carSchema.jsonify(car)


@api.route("/api/addcar", methods=["POST"])
def add_car():

    brand = request.form["brand"] 
    color = request.form["color"]
    seat = request.form["seat"]
    location = request.form["location"]
    cost = request.form["cost"]

    new_car = Car(brand = brand, color = color, seat = seat, location = location, cost = cost)

    db.session.add(new_car)
    db.session.commit()

    return carSchema.jsonify(new_car)


@api.route("/api/delcar/<id>", methods=["DELETE"])
def delete_car(id):

    car = Car.query.get(id)

    db.session.delete(car)
    db.session.commit()

    return carSchema.jsonify(car)


@api.route("/api/editcar", methods=["POST"])
def edit_car():
    
    car_id = request.form["car_id"]
    brand = request.form["brand"]
    color = request.form["color"]
    seat = request.form["seat"]
    location = request.form["location"]
    cost = request.form["cost"]

    car = Car.query.get(car_id)
    car.brand = brand
    car.color = color
    car.seat = seat
    car.location = location
    car.cost = cost

    db.session.commit()

    return carSchema.jsonify(car)


