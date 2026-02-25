from flask.views import MethodView
from flask_mail import Message
from app.extensions import mail,db
import random
from datetime import datetime
from flask import render_template, request,redirect,url_for,flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import User,OTP

def generate_otp():
    return str(random.randint(100000,999999))

class SignupView(MethodView):

    def get(self):
        # show signup page
        return render_template("signup.html")

    def post(self):
        # get form data
        first_name = request.form.get("first_name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Password must be same", "error")
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for("signup"))

        if User.query.filter_by(username=username).first():
            flash("Username already taken")
            return redirect(url_for("signup"))

        # 🔐 hash password
        hashed_password = generate_password_hash(password)

        new_user = User(
            first_name=first_name,
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        otp_code = generate_otp()

        otp_entry = OTP(
            email = email,
            otp = otp_code
        )

        db.session.add(otp_entry)
        db.session.commit()

        msg = Message(
            subject= "Verify Your email",
            recipients= [email]
        )

        msg.body= f"Your OTP is  {otp_code}. It expires in 5 minutes."
        mail.send(msg)

        session['verify_email'] = email

        flash("Signup successful! Please verify your email.")
        return redirect(url_for("otp_page"))



class OTPView(MethodView):

    def get(self):
        return render_template("otp.html")
    
    def post(self):
        user_otp = request.form.get("otp")
        email = session.get("verify_email")

        if not email:
            flash("Session Expired !!!!")
            return redirect(url_for('signup'))

        record = OTP.query.filter_by(email = email,otp = user_otp).first()
        user = User.query.filter_by(email=email).first()
        if not record:
            flash("Invalid OTP")
            return redirect(url_for("otp_page"))
        
        if record.expires_at < datetime.now():
            db.session.delete(record)
            db.session.commit()
            db.session.delete(user)
            db.session.commit()
            flash("OTP Expired")
            return redirect(url_for("signup"))
        
        user.is_verified = True

        db.session.delete(record)
        db.session.commit()

        session.pop('verify_email', None)
        flash("Email verified successfully!")
        return redirect(url_for("login"))
    

class LoginView(MethodView):
    
    def get(self):
        return render_template("login.html")
    
    def post(self):

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username = username).first()

        if not user: 
            flash("User doesn't exists")
            return redirect(url_for("login"))
        
        if not check_password_hash(user.password, password):
            flash("Password is incorrect")
            return redirect(url_for("login"))
        
        if not user.is_verified:
            flash("User is not  verified")
            return redirect(url_for("login"))
        
        session["user_id"] = user.id
        session["role"] = user.role
        flash("Login Successful")
        return redirect(url_for("store"))


class LogoutView(MethodView):

    def get(self):
        session.clear()
        flash("Logout Successfully")
        return redirect(url_for("login"))