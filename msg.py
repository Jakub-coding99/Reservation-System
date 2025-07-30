import requests
import os


def send_message(clients):
    ID	= os.getenv("ID")
    SECRET = os.getenv("SECRET")
    params = {
        "client_id" : ID,
        "client_secret" : SECRET,
        "grant_type" : "client_credentials"
    }

    new_token = requests.get(f"https://app.gosms.eu/oauth/v2/token", params=params).json()
    new_token.raise_for_status()
    
    token = {"access_token": new_token.json()["access_token"]}
    for client in clients:
        body = {
            
        "message": "Dobrý den,\n"
                    f"Připomínam vám rezervaci na zítra v {client['reservation_time']}.\n"
                    "S pozdravem kadeřnice",
        
        "recipients": client["phone"],
        
        "channel": 469663,


        }
        send = requests.post("https://app.gosms.eu/api/v1/messages", params = token, json = body).json()
        print(send)
        print("message sent")


