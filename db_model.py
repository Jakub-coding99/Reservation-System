from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import JSON


db = SQLAlchemy()

class Clients(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    date= db.Column(db.Date)
    time = db.Column(db.Time)
    phone = db.Column(db.Integer)
    work_type = db.Column(db.String)
    msg_sent = db.Column(db.Boolean)
    delete_error = db.Column(db.Boolean)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(200))

class Log(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    client = db.Column(db.JSON)
    response = db.Column(db.JSON)
    datetime = db.Column(db.String)