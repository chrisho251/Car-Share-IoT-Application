from flask import Flask, flash, Blueprint, request, jsonify, render_template, redirect, url_for, session, json, jsonify, make_response, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json, sys, re, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from user_api import *
from schema import *
from car_api import *
from schema import *
from schema import *
import pathlib
sys.path.append(os.path.abspath('../Facial recognition'))
sys.path.append(os.path.abspath('../../src/QRReader'))
from create_qr import create_qr
from PIL import Image
import glob, shutil

app = Flask(__name__)
site = Blueprint("site", __name__)
app_root = os.path.dirname(os.path.abspath(__file__))

@site.route('/', methods=['GET', 'POST'])
def login():
  
    
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password'] 

        # api call to save the user.
        response = requests.post(
            "http://localhost:8080/api/login", {"email": email, "password": password})
        #print(response)
        data = json.loads(response.text)

        # If account exists in users table in out database
        if data:
            # Create session data, we can access this data in other routes
            session['logged_in'] = True
            session['user_id'] = data['user_id']
            session['email'] = data['email']
            session['user_class'] = data['user_class']
            session['mac_address'] = data['mac_address']

            # Redirect to home page
            return redirect(url_for('site.home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Wrong username or password. Please check again'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


# logs out user from the system
@site.route('/logout')
def logout():

    # Remove session data, this will log the user out
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('site.login'))


# this will be the home page, only accessible for loggedin users
@site.route('/home', methods=['GET', 'POST'])
def home():

    # Check if user is loggedin
    if 'logged_in' in session:
        user_class = session['user_class']

        
        if user_class == 'engineer':
            reportedcars = get_reported_cars()
            return render_template('engineer/engineer-dashboard.html', username=session['username'], reportedcars=reportedcars)
        elif user_class == 'manager':
            return render_template('manager/manager-dashboard.html', username=session['username'])
        else:
            car_response = requests.get("http://localhost:8080/api/getcars")
            cars = json.loads(car_response.text)
            
            if user_class == 'admin':
                user_response = requests.get("http://localhost:8080/api/user")
                users = json.loads(user_response.text)

                bookings_response = requests.get("http://localhost:8080/api/bookings")
                bookings = json.loads(bookings_response.text)
                return render_template('admin/admin-dashboard.html', username=session['email'], cars=cars, users=users, bookings=bookings)
            else:
                return render_template('home.html', username=session['email'], cars=cars)
    # users is not loggedin redirect to login page
    return redirect(url_for('site.login'))


@site.route('/profile',  methods=['GET'])
def profile():

    # Check if user is loggedin
    if 'logged_in' in session:
        # We need all the account info for the user so we can display it on the profile page
        response = requests.get(
            "http://localhost:8080/api/userbyid/"+str(session['user_id']))
        acc = json.loads(response.text)
        # Show the profile page with account info
        return render_template('profile.html', account=acc)
    # users is not loggedin redirect to login page
    return redirect(url_for('site.login'))


@site.route('/admincars', methods=['GET', 'POST'])
def admin_cars():
    """This function renders profile page for a user.
    :param: None
    :return: redirect to login page or home page.
    """
    if 'logged_in' in session:
        response = requests.get(
            "http://localhost:8080/api/getcars")
        cars = json.loads(response.text)
        return render_template('admin/admin-cars.html', cars=cars)

    return redirect(url_for('site.login'))


# get the list of bookings done by user.
@site.route('/bookings',  methods=['GET', 'POST'])
def bookings():
    """This function returns the list of bookings done for a loggedin user.
    :param: None
    :return: booking page with the list of booking history.
    """
    # check of user is loggedin
    if 'logged_in' in session:
        # get the booking history of the user.
        response = requests.get(
            "http://localhost:8080/api/bookings/"+str(session['user_id']))
        bookings = json.loads(response.text)

        return render_template('bookings.html', bookinglist=bookings)
    # users is not loggedin redirect to login page
    return redirect(url_for('site.login'))


@site.route('/cancelbooking',  methods=['GET', 'POST'])
def cancelbooking():

    # check of user is loggedin
    if 'logged_in' in session:
        if request.method == 'POST':
            booking_id = request.form['booking_id']

            response = requests.delete(
                "http://localhost:8080/api/bookings/"+str(booking_id))
            acc = json.loads(response.text)
            return redirect(url_for('site.bookings'))


@site.route('/carbooking', methods=['GET', 'POST'])
def carbooking():

    if 'logged_in' in session:
        if request.method == 'POST':

            isActive = True
            user_id = session['user_id']
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            car_id = request.form['car_id']
            response = requests.post(
                "http://localhost:8080/api/add_booking", {
                    "car_id": car_id, "user_id": user_id, "from_date": from_date, "to_date": to_date})
            acc = json.loads(response.text)
        return redirect(url_for('site.bookings'))


@site.route('/register', methods=['GET', 'POST'])
def register():

    
    msg = ''
    
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'username' in request.form and 'password' in request.form and 'confirmpassword' in request.form:

        # Create variables for easy access
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']

        if 'logged_in' in session and session['user_class'] == 'admin':
            user_class = request.form['user_class']
            mac_address = request.form['mac_address']
        else:
            user_class = 'customer'
            mac_address = ''
        
        if not re.match(r'[^@]+@[^@]+\.[^@]+', username):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', first_name) or not re.match(r'[A-Za-z0-9]+', last_name):
            msg = 'First or last name must contain only characters and numbers!'
        elif not first_name or not last_name or not username or not password:
            msg = 'Please fill out the form again'
        elif len(password) < 8:
            msg = 'Password must have at least 8 characters.'
        elif password != confirmpassword:
            msg = "Password does not match."
        else:
            #check if user exists            
            response = requests.get("http://localhost:8080/api/userbyemail/"+str(username))
            account = json.loads(response.text) 
            if account:
                msg = 'Account existed.'
            else:
                response = ''
                # make a api call to save the user.
                response = requests.post("http://localhost:8080/api/adduser", {
                                        "email": username, "password": password, "first_name": first_name, "last_name": last_name, "user_class": user_class, "mac_address": mac_address})
                data = json.loads(response.text)

                # check if response data is valid
                if data:
                    msg = 'You are registerd and can login'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form.'

    if 'logged_in' in session and session['user_class'] == 'admin':
        flash(msg)
        return redirect(url_for('site.home'))

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@site.route('/edituser', methods=['POST'])
def edit_user():

    user_id = request.form['user_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    user_class = request.form['user_class']
    mac_address = request.form['mac_address']

    response = requests.post("http://localhost:8080/api/edituser", {
                                     "user_id": user_id, "email": username, "first_name": first_name, "last_name": last_name, "user_class": user_class, "mac_address": mac_address})
    data = json.loads(response.text)

    if data is None:
        flash("Failed to update the user.")
    else:
        flash("User updated sucessfully.")
    return redirect(url_for('site.home'))


@site.route('/deluser', methods=['POST'])
def delete_user():

    if 'logged_in' in session:
        user_id = request.form['user_id']

        response = requests.delete(
            "http://localhost:8080/api/deluser/"+str(user_id))

        acc = json.loads(response.text)

        if acc is None:
            flash("Cannot delete the user")
        else:
            flash("Deleted successfully.")
        return redirect(url_for('site.home'))


@site.route('/addcar', methods=['POST'])
def add_car():

    brand = request.form['brand']
    color = request.form['color']
    seat = request.form['seat']
    location = request.form['location']
    cost = request.form['cost']

    response = requests.post("http://localhost:8080/api/addcar", {'brand':brand, 'color':color, 'seat':seat, 'location':location, 'cost':cost})
    data = json.loads(response.text)
    
    if data is None:
        flash("Cannot save the car")
    else:
        flash("Added successfully.")
    return redirect(url_for('site.home'))


@site.route('/editcar', methods=['POST'])
def edit_car():
    """This function is used for updating new car to db.
    :param: (str)make, (str)bodytype, (str)color, (float)cost, (int)seats, (str)location
    :return: redirection with success/failure string message 
    """
    car_id = request.form['car_id']
    brand = request.form['brand']
    color = request.form['color']
    seat = request.form['seat']
    location = request.form['location']
    cost = request.form['cost']

    response = requests.post("http://localhost:8080/api/editcar", {'car_id':car_id, 'brand':brand, 'color':color, 'seat':seat, 'location':location, 'cost':cost})
    data = json.loads(response.text)
    
    if data is None:
        flash("Cannot update the car.")
    else:
        flash("Updated successfully")
    return redirect(url_for('site.home'))

    print("Test")


@site.route('/delcar', methods=['POST'])
def delete_car():

    if 'logged_in' in session:
        car_id = request.form['car_id']

        response = requests.delete(
            "http://localhost:8080/api/delcar/"+str(car_id))

        car = json.loads(response.text)

        if car is None:
            flash("Failed to delete the car.")
        else:
            flash("Car deleted sucessfully.")
        return redirect(url_for('site.home'))

@site.route('/reportcar', methods=['POST'])
def report_car():
    if 'logged_in' in session:
        car_id = request.form['car_id']
        user_id = request.form['user_id']
        status = 'faulty'
        issue = request.form['issue']

        response = requests.post("http://localhost:8080/api/reportcar", {'car_id': car_id, 'user_id': user_id, 'status':status, 'issue':issue})
        data = json.loads(response.text)
        
        if data is None:
            flash("Cannot report the issue")
        else:
            flash("Reported sucessfully")
        return redirect(url_for('site.home'))


@site.route('/carslocation', methods=['GET', 'POST'])
def carslocation():

    # Check if user is loggedin
    if 'logged_in' in session:

        if request.method == 'POST':
            car_id = str(request.form['car_id'])
            response = requests.get("http://localhost:8080/api/carlocation/"+car_id)
        else:
            response = requests.get("http://localhost:8080/api/carslocation")
        print(response)
        location = json.loads(response.text)

        # users is loggedin show them the home page
        return render_template('map.html', location=location)
        # return render_template('map.html')
    # users is not loggedin redirect to login page
    return redirect(url_for('site.login'))


@site.route('/uploadimg', methods=['POST'])
def uploadimg():
 
    print(str(pathlib.Path(__file__).resolve().parents[1])+"im hereeeeeeeeeeeeeeeeeeeeeeeee")
    path = str(pathlib.Path(__file__).resolve().parents[1])
    target = os.path.join(path,'Facial recognition/dataset')
    email = session['username']
    target = target+'/'+email

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    return render_template("imguploaded.html")


@site.route('/qr', methods=['POST'])
def generate_qr():
    if 'logged_in' in session and session['user_class'] == 'engineer':
        car_id = request.form['car_id']
        mac_address = session['mac_address']

        gen_qr_obj = create_qr()
        isCreated = gen_qr_obj.start("EngineerId: {}, carID: {}, MacID: {}".format(session['user_id'], car_id, mac_address))

        if isCreated:
            filename = "qr.jpg"
            target = os.path.abspath('../../src/QRReader/generatedimage')

            #source and destination
            src = os.path.join(target, filename)            
            dest = "static/img/qr.jpg"
            filePath = shutil.copyfile(src, dest)
            return render_template("/engineer/qrcode.html", qrfile=filePath, msg="")
        else:
            return render_template("/engineer/qrcode.html", qrfile="", msg="Failed to generate QR Code.")



def get_reported_cars():

    if session['user_class'] == 'engineer':
        carissues = requests.get("http://localhost:8080/api/reportedcars/" + str(session['user_id']))
        return json.loads(carissues.text)

    return None
