from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash,session
from app.extensions import db
from db import Album, Song, Cart,CartItem
from app.utils import save_cover_image,login_required, admin_required
from sqlalchemy import or_



class AddCartView(MethodView):
    @login_required
    def post(self,album_id):
        user_id = session.get("user_id")
        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
        
        item = CartItem.query.filter_by(
            cart_id = cart.id,
            album_id=album_id
        ).first()

        if item:
            item.quantity +=1
        else:
            item = CartItem(
                cart_id= cart.id,
                album_id=album_id,
                quantity = 1
            )
            db.session.add(item)
        db.session.commit()

        flash("Album added to cart!", "success")
        return redirect(url_for("home"))
    

class ViewCartView(MethodView):
    @login_required
    def get(self):
        user_id = session.get("user_id")
        cart = Cart.query.filter_by(user_id=user_id).first()
        return render_template("view_cart.html",cart = cart)