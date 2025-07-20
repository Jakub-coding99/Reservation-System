from flask import Flask, render_template, redirect, url_for, request
from db_model import db, Clients
import os
from dotenv import load_dotenv, find_dotenv
import datetime
from twilio.rest import Client
import time
from apscheduler.schedulers.background import BackgroundScheduler



dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")
app.config["SECRET_KEY"] = os.getenv("secret_key")

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
    
    new_client = Clients(name = reservation["name"], date = datetime_date, time = datetime_time, phone = int(reservation["phone"]), msg_sent = False)
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

@app.route("/change/<int:id>", methods = ["GET","POST"])
def change_reservation(id):
    to_change = db.session.query(Clients).get(id)
    
    
    if request.method == "POST":
        new_client_info = {
            "name" : request.form.get("name"),
            "date" : request.form.get("date"),
            "time" : request.form.get("time"),
            "phone" : request.form.get("phone")

        }
        
        time = new_client_info["time"].split(":")
        new_date = datetime.datetime.strptime(new_client_info["date"],"%Y-%m-%d")
        new_time = datetime.time(hour=int(time[0]), minute=int(time[1]))
        to_change.name = new_client_info["name"]
        to_change.date = new_date
        to_change.time = new_time
        to_change.phone = new_client_info["phone"]
        db.session.commit()

            
        return redirect(url_for("home"))

    return render_template("edit_form.html", id = id, to_change = to_change )
    
def choose_tomorrow_reservation():
    time_now = datetime.datetime.now().date()
    day_after_today = time_now + datetime.timedelta(days=1)
    clients_to_send_notification = []
    
    with app.app_context():
        all_clients = Clients.query.filter_by(date = day_after_today,msg_sent = False).all()
        for client in all_clients:
            str_time = client.time.strftime("%H:%M")
            client_info = {
                    "phone" : client.phone,
                    "reservation_time" : str_time
                }
            client.msg_sent = True
            db.session.commit()
            clients_to_send_notification.append(client_info)
        return clients_to_send_notification

       
def automatic_sending_msg():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(simulate,"cron",hour = 0,minute = 55, second = 20)
    scheduler.add_job(simulate,"interval",seconds = 20, id = "job1")
    scheduler.start()
    

def simulate():
    clients = choose_tomorrow_reservation()
    for client in clients:
        print("Dobrý den,\n"
        f"Připomínam vám rezervaci na zítra v {client['reservation_time']}.\n"
        "S pozdravem kadeřnice")
        

if app.name == "main":
    automatic_sending_msg()
    app.run(use_reloader = False)



# def send_message():
#     acc_sid = os.getenv("acc_sid")
#     auth_token = os.getenv("auth_token")
#     client = Client(acc_sid, auth_token)

#     message = client.messages.create(
#         body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#         from_="+18483595203",
#         to="+420730671753",
#     )

#     print(message.body)