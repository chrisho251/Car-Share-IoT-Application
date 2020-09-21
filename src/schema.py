from flask import Flask, Blueprint, request, jsonify, render_template, url_for, session, json, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields, Schema
import os, requests, json, sys
from table import * 

ma = Marshmallow()

class UserSchema(ma.Schema):

    class Meta:
        model = User
        fields = ("user_id", "email", "password", "first_name", "last_name", "face_regconization", "user_class", "mac_address")

userSchema = UserSchema()
usersSchema = UserSchema(many=True)


class CarSchema(ma.Schema):
    
    class Meta:
        model = Car
        fields = ("car_id", "brand", "color", "seat",
                  "location", "cost", "availability")

carSchema = CarSchema()
carsSchema = CarSchema(many=True)


class BookingSchema(ma.Schema):
    
    class Meta:
        model = Booking
        fields = ("booking_id", "user_id", "car_id", "from_date",
                  "to_date", "isActive", "total_cost")
    car = ma.Nested(CarSchema)

bookingSchema = BookingSchema()
bookingsSchema = BookingSchema(many=True)


class CarReportSchema(ma.Schema):
    
    class Meta:
        model = Car_report
        fields = ("report_id", "car_id", "user_id", "issue", "status", "report_date")

reportcarSchema = CarReportSchema()
reportcarsSchema = CarReportSchema(many=True)