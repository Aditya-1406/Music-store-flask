from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from app.views.auth import SignupView,OTPView,LoginView,LogoutView
from app.views.album import AlbumCreateView,AlbumDetailView,StoreView,ListAlbumAdView,UpdateAlbum,DeleteAlbumView
from app.extensions import db,mail


app = Flask(__name__,template_folder="app/templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:PD40123@localhost:3306/music_store'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "supersecretkeydontknowwh@tiswrllten"

csrf = CSRFProtect(app)
db.init_app(app)

# create tables
with app.app_context():
    db.create_all()

# Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gargaditya674@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'gargaditya674@gmail.com'
app.config['MAIL_PASSWORD'] = 'PS'
mail.init_app(app)


# Routes 

# Auth routes 
app.add_url_rule("/signup",view_func=SignupView.as_view("signup"),methods = ["GET","POST"])
app.add_url_rule("/otp_page",view_func=OTPView.as_view("otp_page"),methods=["GET","POST"])
app.add_url_rule("/login",view_func=LoginView.as_view("login"),methods=["GET","POST"])
app.add_url_rule("/logout",view_func=LogoutView.as_view("logout"),methods=["GET"])

# Album routes
app.add_url_rule("/create-album", view_func=AlbumCreateView.as_view("create_album"))
app.add_url_rule("/", view_func=StoreView.as_view("store"))
app.add_url_rule("/album/<int:album_id>", view_func=AlbumDetailView.as_view("album_detail"))
app.add_url_rule("/list-albums", view_func=ListAlbumAdView.as_view("list_albums"))
app.add_url_rule("/update-album/<int:album_id>", view_func=UpdateAlbum.as_view("update_album"),methods=["GET","POST"])
app.add_url_rule("/delete-album/<int:album_id>", view_func=DeleteAlbumView.as_view("delete_album"),methods=["GET","POST"])




if __name__=="__main__":
    app.run(debug=True)