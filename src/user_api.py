from flask import Flask, Blueprint, request, jsonify, render_template, url_for, json, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
import os, requests, json, sys, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename
from schema import *
from carReport_api import *

app = Flask(__name__)
api = Blueprint("api",__name__)



@api.route("/api/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    print(email, " | ", password)
    print("password: ", password)

    user = User.query.filter(
        User.email == email).first()

    result = {}
    if user and check_password_hash(user.password, password):
        result = userSchema.dump(user)

    print(result)
    return jsonify(result)


@api.route("/api/userpassword", methods=["GET"])
def get_user_password(password):

    user = User.query.get(password)

    return userSchema.jsonify(user)


@api.route("/api/user", methods=["GET"])
def get_all_user():
    
    user = User.query.all()
    
    return userSchema.jsonify(user)


@api.route("/api/userbyid/<id>", methods=["GET"])
def get_user_by_id(id):
    
    user = User.query.get(id)

    return userSchema.jsonify(user)


@api.route("/api/userbyemail/<email>", methods=["GET"])
def get_user_by_email(email):
    
    user = User.query.filter(User.email == email).first()
    
    return userSchema.jsonify(user)


@api.route("/api/adduser", methods=["POST"])
def add_user():
    
    email = request.form["email"]
    password = request.form["password"] 
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    mac_address = request.form["mac_address"]
    user_class = request.form["user_class"]

    password_hash = generate_password_hash(password, method='sha256', salt_length=8)
    
    new_user = User(email = email, password = password_hash,
                    fname = first_name, lname = last_name, macaddress = mac_address, user_class = user_class)

    
    db.session.add(new_user)
    
    db.session.commit()

    return userSchema.jsonify(new_user)


@api.route("/api/deluser/<id>", methods=["DELETE"])
def delete_user(id):
    
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return userSchema.jsonify(user)


@api.route("/api/edituser", methods=["POST"])
def edit_user():
    
    user_id =  request.form["user_id"]
    email = request.form["email"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    mac_address = request.form["mac_address"]
    user_class = request.form["user_class"]

    print(user_id, " | ",email," | ", first_name," | ", last_name, " | ",mac_address," | ", user_class)

    user = User.query.get(user_id)
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.mac_address = mac_address
    user.user_class = user_class

    db.session.commit()

    return userSchema.jsonify(user)

@api.route("/api/engineers/<carid>", methods=["GET"])
def get_mac_address(carid):
    
    reportCar = Car_report.query.filter(Car_report.car_id == carid, Car_report.status == "faulty").first()
    result = {}
    if(reportCar):
        engineer = userSchema.dump(reportCar.engineer)
        report = reportcarSchema.dump(reportCar)
        result = {
            "email": engineer['email'],
            "first_name": engineer['first_name'],
            "mac_address": engineer['mac_address'],
            "issue": report['issue'],
            "report_id": report['report_id']
        }
    return jsonify(result)