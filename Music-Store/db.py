from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from app.extensions import db

# =========================
# USER MODEL
# =========================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique = True,nullable=False,)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20),default="member")
    created_at = db.Column(db.DateTime,default=datetime.now)


    def __repr__(self):
        return f"<User {self.email}>"
    


# =========================
# OTP MODEL
# =========================
class OTP(db.Model):
    __tablename__ = "otp_codes"

    id = db.Column(db.Integer,primary_key= True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    otp = db.Column(db.String(6),nullable=False)
    created_at = db.Column(db.DateTime,default = datetime.now)
    expires_at = db.Column(db.DateTime,default = lambda : datetime.now() + timedelta(minutes=5) )

    def __repr__(self):
        return f"<OTP {self.email}>"
    


# =========================
# Album MODEL
# =========================

class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    artist = db.Column(db.String(150), nullable=False)
    cover_image = db.Column(db.String(255), nullable=False)
    copies = db.Column(db.Integer,default=1)
    amount = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    songs = db.relationship(
        "Song",
        backref="album",
        lazy="select",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Album {self.title}>"

class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)

    album_id = db.Column(
        db.Integer,
        db.ForeignKey("albums.id"),
        nullable=False,
        index=True
    )

    def __repr__(self):
        return f"<Song {self.title}>"
    



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    items = db.relationship(
        "CartItem",
        backref="cart",
        cascade="all, delete-orphan"
    )


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    quantity = db.Column(db.Integer, default=1)

    album = db.relationship("Album")



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(50), default="Paid")
    created_at = db.Column(db.DateTime, default=datetime.now)

    items = db.relationship(
        "OrderItem",
        backref="order",
        cascade="all, delete-orphan"
    )


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    album = db.relationship("Album")