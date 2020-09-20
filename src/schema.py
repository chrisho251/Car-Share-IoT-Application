from flask import Flask, Blueprint, request, jsonify, render_template, url_for, session, json, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields, Schema
import os, requests, json, sys
from table import * 

ma = Marshmallow()

class userSchema(ma.Schema):

    class Meta:
        model = User
        fields = ("user_id", "email", "password", "first_name", "last_name", "face_regconization", "user_class", "mac_address")

userSchema = userSchema()
usersSchema = userSchema(many=True)


class carSchema(ma.Schema):
    
    class Meta:
        model = Car
        fields = ("car_id", "brand", "color", "seat",
                  "location", "cost", "availability")

carSchema = carSchema()
carsSchema = carSchema(many=True)


class bookingSchema(ma.Schema):
    
    class Meta:
        model = Booking
        fields = ("booking_id", "user_id", "car_id", "from_date",
                  "to_date", "isActive", "total_cost")
    car = ma.Nested(CarSchema)

bookingSchema = bookingSchema()
bookingsSchema = bookingSchema(many=True)


class carReportSchema(ma.Schema):
    
    class Meta:
        model = Car_report
        fields = ("report_id", "car_id", "user_id", "issue", "status", "report_date")

reportcarSchema = carReportSchema()
reportcarsSchema = carReportSchema(many=True)