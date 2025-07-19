from flask import Flask, render_template, redirect, url_for, request, jsonify
from db_model import db, Clients
import os
from dotenv import load_dotenv, find_dotenv
import datetime
from twilio.rest import Client

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")

db.init_app(app)

with app.app_context():
    db.create_all()


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
    
    # format_date = "%Y-%m-%d"
    # datetime_date = datetime.datetime.strptime(reservation["date"], format_date)
    
    # x = reservation["time"].split(":")
    # datetime_time = datetime.time(hour=int(x[0]), minute=int(x[1]))
    
    # new_client = Clients(name = reservation["name"], date = datetime_date, time = datetime_time, phone = int(reservation["phone"]))
    # db.session.add(new_client)
    # db.session.commit()
    
    return redirect(url_for("home"))

@app.route("/cal")
def cal():
    return render_template("calendar.html")

def send_message():
    acc_sid = os.getenv("acc_sid")
    auth_token = os.getenv("auth_token")
    client = Client(acc_sid, auth_token)

    message = client.messages.create(
        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
        from_="+18483595203",
        to="+420730671753",
    )

    print(message.body)

@app.route("/events")
def events():
    return jsonify([
        {
            "title": "Ukázková událost",
            "start": "2025-07-21T10:00:00",
            "end": "2025-07-21T12:00:00"
        }
    ])

if app.name == "main":
    app.run(debug=True)