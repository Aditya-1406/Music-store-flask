from flask.views import MethodView
from flask import render_template, request,redirect,url_for,flash
from werkzeug.security import generate_password_hash
from db import db, User

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

        flash("Signup successful! Please verify your email.")
        return redirect(url_for("signup"))


        # temporary print (later we save to DB)
        print(username, email, password)

        return "Signup Successful (DB saving next step)"