import requests
import os
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

def send_message(clients):
    
    
    params = {
        "client_id" : os.getenv("ID"),
        "client_secret" : os.getenv("SECRET"),
        "grant_type" : "client_credentials"
    }
   
    new_token = requests.get(f"https://app.gosms.eu/oauth/v2/token", params=params)
    new_token.raise_for_status()
    token = {"access_token": new_token.json()["access_token"]}
    for client in clients:
        print(client)
        body = {
            
        "message": "Dobrý den,\n"
                    f"Připomínam vám rezervaci na zítra v {client['reservation_time']}.\n"
                    "S pozdravem Markéta Jurajdová",
        
        "recipients": client["phone"],
        
        "channel": 469663,


        }
        requests.post("https://app.gosms.eu/api/v1/messages", params = token, json = body).json()
        
        print("message sent")
    


