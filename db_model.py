from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Clients(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    date= db.Column(db.Date)
    time = db.Column(db.Time)
    phone = db.Column(db.Integer)
    msg_sent = db.Column(db.Boolean)