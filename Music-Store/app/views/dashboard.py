from flask.views import MethodView
from flask_mail import Message
from app.extensions import mail,db
import random
from datetime import datetime
from flask import render_template, request,redirect,url_for,flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import User,OTP
from app.utils import admin_required,send_mail
from sqlalchemy import or_



class DashboardView(MethodView):
    @admin_required
    def get(self):
        return render_template("dashboard.html")