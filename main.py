from flask import Flask, render_template, request,jsonify,Blueprint,redirect,url_for
from db_model import db, Clients, User,Errors
import os
from dotenv import load_dotenv, find_dotenv
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from msg import send_message
import time
from auth.login_actual import auth_bp
from flask_login import UserMixin,login_user,logout_user,LoginManager,login_required, current_user
from app_factory import create_app






app = create_app()
app.register_blueprint(auth_bp,url_prefix="/auth")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

with app.app_context():
    db.create_all()



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



@app.route("/")
@login_required
def render_calendar():
    print(f"Current user: {current_user.name}")
    
    return render_template("index.html",user = current_user)

@app.route("/api_python/submit", methods = ["POST"])
@login_required
def submit_data():
    reservation = request.get_json()
    if reservation is None:
        return jsonify({"error":"data is missing"}),400
    

    # print(reservation)
    # work_types = {"1" : "Stříhání", "2" : "Barva + Melír","3" : "Tónování", "4" : "Barva + Melír + Foukání"}
    # work = work_types[reservation["work"]]

    format_date = "%Y-%m-%d"
    datetime_date = datetime.datetime.strptime(reservation["date"], format_date)
    
    x = reservation["time"].split(":")
    datetime_time = datetime.time(hour=int(x[0]), minute=int(x[1]))
    
    new_client = Clients(name = reservation["name"], date = datetime_date, time = datetime_time, phone = int(reservation["phone"]),work_type = reservation["work"], msg_sent = False)
    
    
    db.session.add(new_client)
    db.session.commit()
    # test_user = [{"reservation_time" : datetime_time,"phone": int(reservation["phone"])}]
    # send_message(test_user)
    return jsonify({"status" : "successfuly created new user"}),201

@app.route("/send_event", methods = ["GET","POST"])
@login_required
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
                "work" : client.work_type
            }
            list_of_clients.append(clients)
            
        
        
        return jsonify(list_of_clients)


@app.route("/delete_id", methods = ["POST"])
@login_required
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
@login_required
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
        
        if all_clients.work_type != data["work"]:
            all_clients.work_type = data["work"]
        
        
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


@app.route("/checkerrors")
@login_required
def check_errors():
    err_logs = Errors.query.all()
    
    return render_template("errors_log.html", err_logs = err_logs)

@app.route("/checkerrors/<id>")
def delete_error(id):
    error = Errors.query.get(id)
    db.session.delete(error)
    db.session.commit()
    return redirect(url_for("check_errors"))





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
    


