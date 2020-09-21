from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields
import os, requests, json
from user_api import *
from carReport_api import *
from car_api import *
from booking_api import *
from schema import *
from flask_site import *

app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'team13'
# Update HOST and PASSWORD appropriately.
HOST = "35.185.177.46"
USER = "root"
PASSWORD = "696969"
DATABASE = "carshare"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
####################################################################################################

db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(site)


if __name__ == "__main__":
    app.run(host = "localhost", port=8080, debug=True)