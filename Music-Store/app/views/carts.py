from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash,session
from app.extensions import db
from db import Album, Song, Cart,CartItem,Order,OrderItem, User
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
        total = 0
        for item in cart.items:
            if item.quantity > item.album.copies:
                flash(f"Not enough stock for {item.album.title}", "danger")
                return redirect(url_for("view_cart"))

            total += item.album.amount * item.quantity
        return render_template("view_cart.html",cart = cart,total = total)
    

class CheckoutView(MethodView):
    @login_required
    def post(self):
        user_id = session.get("user_id")
        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart or not cart.items:
            flash("Cart is empty", "danger")
            return redirect(url_for("cart"))
        
        total = 0

        for item in cart.items:
            if item.quantity > item.album.copies:
                item.quantity = item.album.copies 
                flash(
                f"Quantity adjusted for {item.album.title} due to stock limit.",
                "warning"
                )
                return redirect(url_for("cart"))
                
            
            total += item.album.amount * item.quantity
        db.session.commit()
        
        order = Order(
            user_id = user_id,
            total_amount = total,
            status = "Paid"
        )

        db.session.add(order)
        db.session.flush()

        for item in cart.items:
            order_item = OrderItem(
                order_id = order.id,
                album_id = item.album.id,
                quantity = item.quantity,
                price = item.album.amount
            )
            db.session.add(order_item)

            item.album.copies -= item.quantity
        
        db.session.delete(cart)
        db.session.commit()

        flash("Payment Successful Order Created", "success")
        return redirect(url_for("orders"))
    
class OrderHistoryView(MethodView):
    @login_required
    def get(self):
        user_id = session.get("user_id")

        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        return render_template("orders.html",orders=orders)
    
class ListOrderView(MethodView):
    @admin_required
    def get(self):
        page = request.args.get("page", 1, type=int)
        search = request.args.get("search", "")
        query = Order.query.join(User)
        if search:
            query = query.filter(
                or_(
                    User.username.ilike(f"%{search}%"),
                    Order.status.ilike(f"%{search}%"),
                )
            )
        orders = query.order_by(Order.id.desc()).paginate(
            page=page,
            per_page=1,
            error_out=False
        )
        return render_template("list_order.html", orders=orders)
    
    
class OrderDetailView(MethodView):
    @login_required
    def get(self,order_id):
        order = Order.query.get_or_404(order_id)
        return render_template("order_detail.html", order=order)