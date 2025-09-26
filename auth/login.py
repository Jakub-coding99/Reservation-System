from flask import Flask, Blueprint,render_template,url_for,redirect,request,jsonify
from db_model import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__,template_folder="templates")


@auth_bp.route("/home")
def home():
    return render_template("login.html")



@auth_bp.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "POST":
    
        user = {
            
            "name" : request.form["name"],
            "email" : request.form["email"],
            "password1" : request.form["password"],
            "password2" : request.form["pasword_repeat"],

        }
        
        if user["password1"] == user["password2"]:
            confirmed_pass = generate_password_hash(user["password1"], method="pbkdf2:sha256")
            new_user = User(user_name = user["name"], email = user["email"], password = confirmed_pass)
            db.session.add(new_user)
            db.session.commit()
        
        
        # if user["password1"] != user["password2"]:
        #     pass
        # #     return jsonify({"success": False, "message": "Passwords dont match!", "redirect": url_for("auth.home")})
        # # else:
        #      return jsonify({"success": True})          
    
    return redirect(url_for("auth.home"))
    
    

