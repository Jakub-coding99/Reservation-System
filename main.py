from flask import Flask, render_template, redirect, url_for, request
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
    clients = get_reservation()
    return render_template("index.html", clients = clients, )

@app.route("/reservation", methods = ["GET", "POST"])
def save_reservation():
    reservation = {
        "name" : request.form.get("name"),
        "date" : request.form.get("date"),
        "time" : request.form.get("time"),
        "phone" : request.form.get("phone")
    }
    format_date = "%Y-%m-%d"
    datetime_date = datetime.datetime.strptime(reservation["date"], format_date)
    
    x = reservation["time"].split(":")
    datetime_time = datetime.time(hour=int(x[0]), minute=int(x[1]))
    
    new_client = Clients(name = reservation["name"], date = datetime_date, time = datetime_time, phone = int(reservation["phone"]))
    db.session.add(new_client)
    db.session.commit()
    
    return redirect(url_for("home"))

def get_reservation():
    with app.app_context():
        clients = db.session.query(Clients).all()
        return clients

@app.route("/delete/<int:id>")
def delete_client(id):
    to_delete = db.session.query(Clients).get(id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/change/<int:id>")
def change_reservation(id):
    to_change = db.session.query(Clients).get(id)
    print(to_change.name)

    
    
    
    return redirect(url_for("home"))


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


if app.name == "main":
    app.run(debug=True)