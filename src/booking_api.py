from flask import Flask, Blueprint, request, jsonify, render_template, url_for, json, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
import os, requests, json, sys, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename
from schema import *



@api.route("/api/bookings", methods=["GET"])
def get_all_bookings():
    
    booking = Booking.query.all()

    return bookingSchema.jsonify(booking)


@api.route("/api/bookings/<userid>", methods=["GET"])
def get_booking_by_id(user_id):
    
    booking = Booking.query.filter(Booking.user_id == user_id)

    return bookingSchema.jsonify(booking)


@api.route("/api/add_booking", methods=["POST"])
def add_booking():
    
    try:
        
        car_id = request.form["car_id"]
        user_id = request.form["user_id"]
        fromDate = request.form["from_date"].strip()
        toDate = request.form["to_date"].strip()

        print(fromDate, "|", toDate)

        car = Car.query.get(car_id)
        car.availability = False

        user = User.query.get(user_id)
        user_email = user.email

        fromDate_obj = datetime.datetime.strptime(fromDate, '%Y-%m-%d')
        toDate_obj = datetime.datetime.strptime(toDate, '%Y-%m-%d')
        
        summary = "Car Booking. Car id: " + car_id

        cal = CalendarUtil()
        resp = cal.addToCalendar(user_email, fromDate_obj, toDate_obj, summary)
        cal_event_id = resp['id']
        booking = Booking(carid=car_id, userid=user_id, fromdate=fromDate, todate=toDate, caleventid= cal_event_id, isActive=True)

        test = db.session.add(booking)
        db.session.commit()
        return bookingSchema.jsonify(booking)
    except Exception as ex:

        print("Failed to add event to calender. Exception: ", str(ex))

        return jsonify(None)


@api.route("/api/bookings/<bookingid>", methods=["DELETE"])
def delete_bookings(booking_id):
    
    booking = Booking.query.get(booking_id)

    car = booking.car
    car.availability = True
    
    calender_event_id = booking.calender_event_id

    db.session.delete(booking)
    db.session.commit()

    cal = CalendarUtil()
    resp = cal.deleteFromCalendar(calender_event_id)

    if resp == False:
        print("Failed to delete event from calender.")

    return bookingSchema.jsonify(booking)