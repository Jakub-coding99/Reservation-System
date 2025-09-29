import requests
import os
from json import JSONDecodeError
import time
from app_factory import create_app
from db_model import Errors,db
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
            print("pokus" +  str(x))
            request = requests.post("https://app.gosms.eu/api/v1/messages/test", headers=headers, json = body)
            request.raise_for_status()
            if request.status_code == 200:
                break
            
        except requests.exceptions.HTTPError as err:
            time.sleep(5)
        



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
           
            try:
                
                body = {
                    
                "message": "Dobrý den,\n"
                            f"Připomínam vám rezervaci na zítra v {clients[x]['reservation_time']}.\n"
                            f"S pozdravem {os.getenv("sender")}",
                
                "recipients": clients[x]["phone"],
                
                "channel": 469663,


                }
     
                request = requests.post("https://app.gosms.eu/api/v1/messages/test", headers=headers, json = body)
                request.raise_for_status()
                print("sms sent")
                time.sleep(2)
            
        
            except requests.exceptions.HTTPError as err:
                status_code = err.response.status_code
                time_now = datetime.now()
                formated_time = time_now.strftime("%d-%m-%Y, %H:%M:%S")
                dt_obj = datetime.strptime(formated_time,"%d-%m-%Y, %H:%M:%S")
                
                if status_code  == 400:
                    
                    with app.app_context():        
                        new_error = Errors(client = clients[x], response_error = err.response.text,datetime = dt_obj)
                        db.session.add(new_error)
                        db.session.commit()
                  
                    # retry(x,clients,token)
                    
                    data_to_save = err.response.text
                    
                    
                    print(clients[x])
                    print(data_to_save)
                    
                    
                elif (status_code == 429 or status_code == 500 or status_code == 502
                    or status_code == 503 or status_code == 504):
                    retry(x,clients,token)
    

            except JSONDecodeError as json_err:
                print(json_err)   

    
    except requests.exceptions.HTTPError as err:
        status_code = err.response.status_code
        print(status_code)
        if status_code == 400:
            print(err.response.text)
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
  

clients = [
    {"phone": "abc123", "reservation_time": "14:00"},  # invalid
    {"phone": "730671753", "reservation_time": "15:00"}  # valid
]



# send_message(clients = clients)








        
