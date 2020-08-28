from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from flask_sqlalchemy import SQLAlchemy
import  pymysql
from passlib.hash import sha256_crypt
import re
engine = create_engine("mysql+pymysql://root:1234567@localhost/register")
                        #(mysql+pymysql://username:password@local/databasename)
db=scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

#register form
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("name")
        gmail = request.form.get("gmail")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        secure_password = sha256_crypt.encrypt(str(password))
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        # check valid gmail
        if re.search(regex,gmail):
            gmail = db.execute("SELECT gmail FROM users WHERE username=:username",{"username":username}).fetchone()
            if not gmail:
                # the email doesnt exist
                pass
            else:
                flash("email exists","danger")
                return render_template("register.html")
                pass
        else:
            flash("invalid email","danger")
            return render_template("register.html") #### make function in this task

        #check gmail is existed
        gmail = db.execute("SELECT gmail FROM users WHERE username=:username",{"username":username}).fetchone()
        if not gmail:
            # the email doesnt exist
            pass
        else:
            flash("email exists","danger")
            return render_template("register.html")

        # check password correct
        if password == confirm:
            db.execute("INSERT INTO users(name, username, gmail, password) VALUES (:name, :username, :gmail, :password)",
                                        {"name":name, "username":username,"gmail":gmail,"password":secure_password})
            db.commit()
            flash("You are registerd and can login", "success")
            return redirect(url_for('login'))
        else:
            flash("password does not match", "danger")
            return render_template("register.html")

    return render_template("register.html")

#login
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("password")

        usernamedata = db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        passwordata = db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()

        if usernamedata is None:
            flash("No username","danger")
            return render_template("login.html")
        else:
            for passwor_data in passwordata:
                if sha256_crypt.verify(password,passwor_data):
                    session["log"] = True

                    flash("You are now login","success")
                    return redirect(url_for('photo'))
                else:
                    flash("incorrect password","danger")
                    return render_template("login.html")

    return render_template("login.html")

#photo
@app.route("/photo")
def photo():
    return render_template("photo.html")

#logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logger out","success")
    return redirect(url_for('login'))

if __name__ =="__main__":
    app.secret_key="1234567dailywebcoding"
    app.run(debug=True)
