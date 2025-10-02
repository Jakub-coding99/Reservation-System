import requests
import os
from json import JSONDecodeError
import time
from app_factory import create_app
from db_model import Log,db,Clients
from datetime import datetime

from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = create_app()

def retry(client_num,clients,token):
    
    import time
    headers = {"Authorization": f"Bearer {token}"}
    for x in range(3):
        try:
        
            body = {
                        
                    "message": "Dobrý den,\n"
                                f"Připomínam vám rezervaci na zítra v {clients[client_num]['reservation_time']}.\n"
                                "S pozdravem Markéta Jurajdová",
                    
                    "recipients": clients[client_num]["phone"],
                    
                    "channel": 469663,


                    }
           
            request = requests.post("https://app.gosms.eu/api/v1/messages/test", headers=headers, json = body)
            request.raise_for_status()
            
            with app.app_context():
                clients_id = Clients.query.get(clients[client_num]["id"])
                
                if request.status_code == 200:
                    clients_id.msg_sent = True
                    db.session.commit()
                    msg_log(client_num[client_num],None,request.status_code)
                
                if x == 2:
                    clients_id.delete_error = True
                    db.session.commit()
            
        except requests.exceptions.HTTPError as err:
            time.sleep(60)
        



def send_message(clients):
    
    
    params = {
        "client_id" : os.getenv("ID"),
        "client_secret" : os.getenv("SECRET"),
        "grant_type" : "client_credentials"
    }
   
    try:
        new_token = requests.get(f"https://app.gosms.eu/oauth/v2/token", params=params)
        new_token.raise_for_status()
        token = new_token.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        for x in range(len(clients)):
            
            with app.app_context():
                clients_id = Clients.query.get(clients[x]["id"])
                try:
                    
                    body = {
                        
                    "message": "Dobrý den,\n"
                                f"Připomínam vám rezervaci na zítra v {clients[x]['reservation_time']}.\n"
                                f"S pozdravem {os.getenv("sender")}",
                    
                    "recipients": clients[x]["phone"],
                    
                    "channel": 469663,
                    "status" : "READY_TO_SEND"


                    }
        
                    request = requests.post("https://app.gosms.eu/api/v1/messages/test", headers=headers, json = body)
                    request.raise_for_status()
                    msg_log(clients[x],None,request.status_code)
                    clients_id.msg_sent = True
                    db.session.commit()
                    time.sleep(2)

                
            
                except requests.exceptions.HTTPError as err:
                    msg_log(clients[x],err,err.response.status_code)
                    status_code = err.response.status_code

                    if status_code == 400:
                        clients_id.delete_error = True
                        db.session.commit()
                        
                    elif (status_code == 429 or status_code == 500 or status_code == 502
                        or status_code == 503 or status_code == 504):
                        retry(x,clients,token)
        

                except JSONDecodeError as json_err:
                    print(json_err)   
    
    except requests.exceptions.HTTPError as err:
        status_code = err.response.status_code
        if status_code == 400:
            msg_log(clients[x],err,None,status_code)
           
    except JSONDecodeError as json_err:
        print(json_err)   
    
    finally:
        
        check_credit(token)


def send_info_email(credit):
    import smtplib
    from email.mime.multipart import MIMEMultipart 
    from email.mime.text import MIMEText
        
    
    web_email = os.getenv("web_email")
    my_password = os.getenv("my_password")
    my_email = os.getenv("my_email")

    msg = MIMEMultipart()
    msg['From'] = web_email
    msg['To'] = my_email
    msg['Subject'] = "Nízky kredit GOSMS - python"
    message = "„Upozornění: Kredit na vašem GoSMS účtu klesl pod stanovený limit. Doporučujeme dobít co nejdříve, aby nedošlo k přerušení odesílání zpráv.“\n\n" \
    f"Vás současný kredit je: {credit} CZK"
    
        
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(user=web_email, password=my_password)

    mailserver.sendmail(from_addr=web_email,to_addrs=my_email,msg=msg.as_string())
    print("credit info sent to email")

    mailserver.quit()
    


def check_credit(token):
    headers = {"Authorization": f"Bearer {token}"}
    credit_url = "https://app.gosms.eu/api/v1"
    credit_request = requests.get(credit_url,headers=headers)
    
    credit_request.raise_for_status()
    credit_data = credit_request.json()

    
    credit = credit_data["currentCredit"]
    
    print(f"současný kredit: {credit}")
    if credit < 20:
        # send_info_email(credit)
        print("email sent")
  

# clients = [
#          {"phone": "abc123", "reservation_time": "14:00"},  # invalid
#         {"phone": "730671753", "reservation_time": "15:00"},  # valid
   

# ]




def msg_log(client,error,code):
    time_now = datetime.now()
    formated_time = time_now.strftime("%d-%m-%Y, %H:%M:%S")
    dt_obj = datetime.strptime(formated_time,"%d-%m-%Y, %H:%M:%S")
    
    if code in (200,201):
        response = {"status":"sent ok"}
    
    else:
        response = error.response.text
        
    with app.app_context():        
        new_response = Log(client = client, response = response,datetime = dt_obj)
        db.session.add(new_response)
        db.session.commit()
   

        
# send_message(clients = clients)