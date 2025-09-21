from flask import Flask, render_template, request,jsonify
from db_model import db, Clients
import os
from dotenv import load_dotenv, find_dotenv
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from msg import send_message
import time

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")
app.config["SECRET_KEY"] = os.getenv("secret_key")

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def render_calendar():
    return render_template("calendar.html")

@app.route("/api_python/submit", methods = ["POST"])
def submit_data():
    reservation = request.get_json()
    if reservation is None:
        return jsonify({"error":"data is missing"}),400
    
    format_date = "%Y-%m-%d"
    datetime_date = datetime.datetime.strptime(reservation["date"], format_date)
    
    x = reservation["time"].split(":")
    datetime_time = datetime.time(hour=int(x[0]), minute=int(x[1]))
    
    new_client = Clients(name = reservation["name"], date = datetime_date, time = datetime_time, phone = int(reservation["phone"]), msg_sent = False)
    db.session.add(new_client)
    db.session.commit()
    # test_user = [{"reservation_time" : datetime_time,"phone": int(reservation["phone"])}]
    # send_message(test_user)
    return jsonify({"status" : "successfuly created new user"}),201

@app.route("/send_event", methods = ["GET","POST"])
def event_send():
    with app.app_context():
        all_clients = Clients.query.all()
        list_of_clients = []
        for client in all_clients:
            
            combine_dt = datetime.datetime.combine(client.date, client.time)
            date_to_iso = combine_dt.isoformat()
            
            
            
            
            clients = {
                "id" : client.id,
                "name" : client.name,
                "start" : date_to_iso,
                "phone" : client.phone,
            }
            list_of_clients.append(clients)
            
        
        
        return jsonify(list_of_clients)


@app.route("/delete_id", methods = ["POST"])
def delete_user():
    data = request.get_json()
    if data is None:
        return jsonify({"status":"missing user data"}),400
    id = data["userID"]
    with app.app_context():
        client_to_del = Clients.query.get(id)
        if client_to_del is None:
            return jsonify({"error":"user not found"}),404
        db.session.delete(client_to_del)
        db.session.commit()
        return jsonify({"status":"user succesfuly deleted"}),204
        
@app.route("/update_db", methods = ["PATCH"])
def patch_user():
    data = request.get_json()
    if data is None:
        return jsonify({"error":"missing user data"}),400
    id = data["id"]
    format_date = "%Y-%m-%d"
    datetime_date = datetime.datetime.strptime(data["date"], format_date)
    
    t = data["time"].split(":")
    datetime_time = datetime.time(hour=int(t[0]), minute=int(t[1]))

    with app.app_context():
        all_clients = Clients.query.get(id)
        if all_clients.name != data["name"]:
            all_clients.name = data["name"]
        
        if all_clients.date != datetime_date:
            all_clients.date = datetime_date
        
        if all_clients.time != datetime_time:
            all_clients.time = datetime_time

        if all_clients.phone != data["phone"]:
            all_clients.phone = data["phone"]
        db.session.commit()
    
    return jsonify({"status":"user succesfuly updated"}),200
    
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

       
def delete_after_reservation():
        today = datetime.datetime.now().date()
        time_now = datetime.datetime.now().time()
        
        with app.app_context():
            clients = Clients.query.filter_by(date = today).all()
            for client in clients:
                reservation_cl = client.time
                dt = datetime.datetime.combine(datetime.datetime.now(), reservation_cl)
                dt_plus = dt + datetime.timedelta(minutes=30)
                reservation = dt_plus.time()
                time_now_toformat = datetime.datetime.now().time()
                time_now = time_now_toformat.replace(microsecond=0)
                
                if time_now > reservation:
                    db.session.delete(client)
                    db.session.commit()
                time.sleep(1)
            

def automatic_sending_msg():
    scheduler = BackgroundScheduler()
    scheduler.add_job(automate_msg, "interval",  minutes = 30, id="job1")
    scheduler.add_job(delete_after_reservation, "interval", minutes=30, id="job2")
    scheduler.start()


def automate_msg():
    # clients = choose_tomorrow_reservation()
    # if clients:
    #     send_message(clients=clients)
    print("sent")



if __name__ == "__main__":
    automatic_sending_msg()
    app.run(host="0.0.0.0", port=5000)
    


