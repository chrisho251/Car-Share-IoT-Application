from flask import Flask, Blueprint, request, jsonify, render_template, url_for, json, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
import os, requests, json, sys, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename
from schema import *



@api.route("/api/reportcar", methods=["POST"])
def car_report():
    

    car_id = request.form["car_id"]
    user_id = request.form["user_id"] 
    status = request.form["status"]
    issue = request.form["issue"]
    report_date = datetime.datetime.now()

    print(car_id," | ", user_id," | ", status," | ", issue," | ", report_date)
    car = Car.query.get(car_id)
    car.availability = False
    
    report = Car_report(carid=car_id, userid=user_id, status=status, issue=issue, reportdate=report_date)
    
    db.session.add(report)
    
    db.session.commit()
    
    user = User.query.get(user_id)
    email = user.email
    title_for_notification = "Car ID [{}] reported by admin".format(car_id)
    body_for_notification = "Issue: {}. Please check your dashboard for more details".format(issue)
    #notification(title_for_notification, body_for_notification, email)

    return reportcarSchema.jsonify(report)


@api.route("/api/reportedcars/<userid>", methods=["GET"])
def reported_cars(userid):
    
    faultycars = Car_report.query.filter(Car_report.user_id == user_id, Car_report.status == 'faulty').all()
    
    return reportcarSchema.jsonify(faultycars)


@api.route("/api/reportstatus/<reportid>/<status>", methods=["GET"])
def update_report_status(report_id, status):
    
    reportCar = Car_report.query.get(report_id)
    reportCar.status = status

    if(status=="fixed"):
        car = reportCar.car
        car.availability = True

    db.session.commit()
    
    return jsonify({"message": "Status changed to " + status})