import requests
import os


def send_message():
    ID	= os.getenv("ID")
    SECRET = os.getenv("SECRET")
    params = {
        "client_id" : ID,
        "client_secret" : SECRET,
        "grant_type" : "client_credentials"
    }

    new_token = requests.get(f"https://app.gosms.eu/oauth/v2/token", params=params).json()
    new_token.raise_for_status()
    print(new_token)

    token = {"access_token": new_token.json()["access_token"]}

    body = {
        
    "message": "testing sms",
    "recipients": os.getenv("MY_NUMBER"),
    "channel": 469663,


    }
    send = requests.post("https://app.gosms.eu/api/v1/messages", params = token, json = body).json()
    return send

