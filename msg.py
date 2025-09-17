import requests
import os


def send_message(clients):
    ID	= "53156_3zyy5dif4604wg84osko8gkswkosoc00ws08k4o8cccc48kk80"
    SECRET = "1ew86von3edc8s0wsog0kg40swk4s80oc4w0k4o48o8o0k8oww"
    
    params = {
        "client_id" : ID,
        "client_secret" : SECRET,
        "grant_type" : "client_credentials"
    }

    new_token = requests.get(f"https://app.gosms.eu/oauth/v2/token", params=params)
    print(new_token)
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
        send = requests.post("https://app.gosms.eu/api/v1/messages", params = token, json = body).json()
        print(send)
        print("message sent")

# cl = [{"reservation_time": "20:30","phone":730671753}]
# send_message(cl)
