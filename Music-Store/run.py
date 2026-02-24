from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from app.views.auth import SignupView
from db import db


app = Flask(__name__,template_folder="app/templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password@localhost:3306/music_store'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "supersecretkeydontknowwh@tiswrllten"

csrf = CSRFProtect(app)

db.init_app(app)

# create tables
with app.app_context():
    db.create_all()


app.add_url_rule(
    "/",
    view_func=SignupView.as_view("signup"),
    methods = ["GET","POST"]
)


if __name__=="__main__":
    app.run(debug=True)