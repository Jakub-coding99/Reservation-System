from db_model import db, Clients, User
import os
from flask import Flask
from dotenv import load_dotenv, find_dotenv


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")
    app.config["SECRET_KEY"] = os.getenv("secret_key")

    db.init_app(app)
    return app