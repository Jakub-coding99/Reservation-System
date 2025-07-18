from flask import Flask, render_template, redirect, url_for, request
from db_model import db
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reservation", methods = ["GET", "POST"])
def save_reservation():
    reservation = {
        "name" : request.form.get("name"),
        "date" : request.form.get("date"),
        "time" : request.form.get("time"),
        "phone" : request.form.get("phone")

    }
    
    print(reservation)
    return redirect(url_for("home"))

with app.app_context():
    db.create_all()

if app.name == "main":
    app.run(debug=True)