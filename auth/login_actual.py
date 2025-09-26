from flask_login import UserMixin,login_user,logout_user,LoginManager,login_required, current_user
from flask import Flask,redirect,render_template,url_for,request,flash,Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer as Serializer
from db_model import db, User



auth_bp = Blueprint("auth", __name__,template_folder="templates")



@auth_bp.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        logged_user = {

        "name" :  request.form["name"],
        "password" : request.form["password"]
        }
        
        if logged_user["name"] == "" and logged_user["password"] == "":
            flash("Zadejte přihlašovací údaje.")
            return redirect(url_for("auth.login"))
        
        

        find_user = User.query.filter_by(name = logged_user["name"]).first()
        if find_user:
            check_password = check_password_hash(find_user.password_hash,logged_user["password"])
            if check_password:
                login_user(find_user, remember=True)
                return redirect(url_for("render_calendar"))
            else:
                flash("Zadané heslo není správné.")
                return redirect(url_for("auth.login"))

        
        
        else:
            flash("Špatné uživatelské jméno nebo heslo.")
            return redirect(url_for("auth.login"))
        
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    
    return render_template("test.html")



@auth_bp.route("/forgotpass" ,methods = ["GET","POST"])
def forgot_password():
    user = User.query.first()
    token = get_token(user.id)
    reset_url = url_for("auth.change_pass",token = token, _external = True)
    generate_new_pass(reset_url)
    flash("Do emailu Vám byly zaslány informace pro reset hesla.")
    return redirect(url_for("auth.login"))
    
def get_token(user_id):
    s = Serializer("secret")
    token = s.dumps(user_id,salt="password_reset")
    return token
        


def verify(token,expiration = 929):
    from itsdangerous import SignatureExpired,BadSignature
    s = Serializer("secret")
    try:
      
        data = s.loads(s = token,salt="password_reset" ,max_age=expiration)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
    else:
        return data
    

@auth_bp.route("/change_pass/<token>", methods = ["GET","POST"])
def change_pass(token):
    user_id = verify(token = token )
    if user_id == None:
        flash("Relace pro změnu hesla vypršela.")
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        password1 = request.form["password1"].strip().replace(" ","")
        password2 = request.form["password2"].strip().replace(" ","")
        print(password1)
        
        if len(password1) == 0 and len(password2) == 0:
            flash("Zadejte nové heslo")
            return render_template("forgot_pass.html")
        
        if len(password1) < 7:
            flash("Zadejte heslo obsahující nejméně 7 znaků.")
            return render_template("forgot_pass.html")


        
        if password1 == password2:
            user = User.query.filter_by(id = user_id).first()
            hashed_pass = generate_password_hash(password1,method= "pbkdf2:sha1")
            user.password_hash = hashed_pass
            db.session.commit()
            flash("Heslo bylo úspěšně změněno.")
            return redirect(url_for("auth.login"))
    
        else:
            flash("Zadané hesla se neshodují.")
            return render_template("forgot_pass.html")
    
    return render_template("forgot_pass.html")
    
    
    
def generate_new_pass(url):
    import os
    web_email = os.getenv("web_email")
    my_password = os.getenv("my_password")
    my_email = os.getenv("my_email")

    msg = MIMEMultipart()
    msg['From'] = web_email
    msg['To'] = my_email
    msg['Subject'] = "Reset Hesla"
    message = f"Pro reset hesla v Rezervaci klikněte zde: {url} \n\nPokud jste o reset hesla nežádali, tak zprávu ignorujte."
    
        
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(user=web_email, password=my_password)

    mailserver.sendmail(from_addr=web_email,to_addrs=my_email,msg=msg.as_string())

    mailserver.quit()
