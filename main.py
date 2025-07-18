from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

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


if app.name == "main":
    app.run(debug=True)