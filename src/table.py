from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app

app = Flask(__name__)
api = Blueprint("api",__name__)
db = SQLAlchemy()


class User(db.Model):

    __tablename__  = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password=db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(255), unique=True, nullable = False)
    first_name = db.Column(db.String(200), nullable = False)
    last_name = db.Column(db.String(200), nullable = False)
    user_class = db.Column(db.String(200), nullable = False)
    face_recognization = db.Column(db.LargeBinary(), nullable = True)
    mac_address = db.Column(db.String(200), nullable = True)
    booking = db.relationship("Booking", backref='customer')
    reported_issues = db.relationship("Rerpot_car", backref='engineer')
    
    def __repr__(self):
        return "User(user_id='%s', password='%s', email='%s', fullname='%s', lastname'%s')>"%(
            self.user_id, self.password, self.email, self.fullname, self.lastname
        )

class Car(db.Model):

    __tablename__ = "car"
    __search__ = ['color','seat','cost','brand', 'availability', 'location']
    car_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.String(100), nullable = False)
    color = db.Column(db.String(100), nullable = False)
    seat = db.Column(db.Integer, nullable = False)
    cost = db.Column(db.Float, nullable = False)
    location = db.Column(db.String(255), nullable = False)
    availability = db.Column(db.Boolean, default = True, nullable=False)
    booking = db.relationship('Booking', backref='car')
    reported_issues = db.relationship('Rerport_car', backref='car')

    def __repr__(self):
        return "Car(car_id='%s', brand='%s', color='%s','seat=%s', 'location=%s', 'cost =%s','availability=%s')>"%(
            self.car_id, self.brand, self.color, self.seat, self.location, self.cost, self.availability
        )

class Booking(db.Model):
    
    __tablename__="booking"
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'), nullable=False)
    from_date = db.Column(db.DateTime, nullable = False)
    to_date = db.Column(db.DateTime, nullable = False)
    isActive = db.Column(db.Boolean, default=True, nullable=False)
    total_cost = db.Column(db.Float, nullable = False)
    calendar_event_id = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "<Booking(booking_id='%s', user_id='%s', car_id='%s', from_date='%s',to_date='%s',isActive='%s')>" % ( 
            self.booking_id, self.user_id, self.car_id, self.from_date,self.to_date,self.isActive)


class Car_report(db.Model):

    __tablename__ = "carReport"
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'), nullable=False)
    issue = db.Column(db.String(225), nullable=False)
    report_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Reportcar(report_id='%s', car_id='%s', user_id='%s', issue='%s', report_date='%s', status='%s')>" % (
            self.reportid, self.car_id, self.user_id, self.issue, self.report_date, self.status
        )