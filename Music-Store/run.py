from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from app.views.auth import SignupView,OTPView,LoginView,LogoutView,ListUserView,UpdateRoleView,DeleteUserView
from app.views.album import AlbumCreateView,AlbumDetailView,StoreView,ListAlbumAdView,UpdateAlbum,DeleteAlbumView,HomeView
from app.views.carts import AddCartView,ViewCartView,CheckoutView,OrderHistoryView,ListOrderView,OrderDetailView
from app.extensions import db,mail


app = Flask(__name__,template_folder="app/templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:PAS%40123@localhost:3306/music_store'
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
app.config['MAIL_PASSWORD'] = 'PAS'
mail.init_app(app)


# Routes 

# Auth routes 
app.add_url_rule("/signup",view_func=SignupView.as_view("signup"),methods = ["GET","POST"])
app.add_url_rule("/otp_page",view_func=OTPView.as_view("otp_page"),methods=["GET","POST"])
app.add_url_rule("/login",view_func=LoginView.as_view("login"),methods=["GET","POST"])
app.add_url_rule("/logout",view_func=LogoutView.as_view("logout"),methods=["GET"])
app.add_url_rule("/list-users",view_func=ListUserView.as_view("list_users"),methods=["GET"])
app.add_url_rule("/update-user/<int:user_id>",view_func=UpdateRoleView.as_view("update_user"),methods=["GET","POST"])
app.add_url_rule("/delete-user/<int:user_id>",view_func=DeleteUserView.as_view("delete_user"),methods=["GET","POST"])


# Album routes
app.add_url_rule("/create-album", view_func=AlbumCreateView.as_view("create_album"))
app.add_url_rule("/", view_func=StoreView.as_view("store"))
app.add_url_rule("/album/<int:album_id>", view_func=AlbumDetailView.as_view("album_detail"))
app.add_url_rule("/list-albums", view_func=ListAlbumAdView.as_view("list_albums"))
app.add_url_rule("/update-album/<int:album_id>", view_func=UpdateAlbum.as_view("update_album"),methods=["GET","POST"])
app.add_url_rule("/delete-album/<int:album_id>", view_func=DeleteAlbumView.as_view("delete_album"),methods=["GET","POST"])
app.add_url_rule("/home", view_func=HomeView.as_view("home"),methods=["GET","POST"])


# Cart and Order Routes
app.add_url_rule("/add-cart/<int:album_id>", view_func=AddCartView.as_view("add_cart"),methods=["GET","POST"])
app.add_url_rule("/cart", view_func=ViewCartView.as_view("view_cart"),methods=["GET"])
app.add_url_rule("/checkout", view_func=CheckoutView.as_view("checkout"),methods=["POST"])
app.add_url_rule("/orders", view_func=OrderHistoryView.as_view("orders"),methods=["GET"])
app.add_url_rule("/list-orders",view_func=ListOrderView.as_view("list_order"),methods=["GET"])
app.add_url_rule("/order-detail/<int:order_id>", view_func=OrderDetailView.as_view("order_detail"),methods=["GET"])
if __name__=="__main__":
    app.run(debug=True)