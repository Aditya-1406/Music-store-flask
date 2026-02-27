from flask.views import MethodView
from flask_mail import Message
from app.extensions import db
from flask import render_template, request,redirect,url_for,flash, session
from db import User,OTP
from app.utils import admin_required,send_mail
from sqlalchemy import or_,func
from db import User,Order,Album,OrderItem
from datetime import datetime



class DashboardView(MethodView):
    @admin_required
    def get(self):

        total_users = User.query.count()
        total_albums = Album.query.count()
        total_orders = Order.query.count()

        total_revenue = db.session.query(
            func.sum(Order.total_amount)
        ).scalar() or 0

        # 📊 Monthly Sales (Current Year)
        current_year = datetime.now().year

        monthly_sales = (
            db.session.query(
            func.month(Order.created_at).label("month"),
            func.sum(Order.total_amount).label("total")
            )
            .filter(func.year(Order.created_at) == current_year)
            .group_by(func.month(Order.created_at))
            .all()
            )

        # Create 12 months structure
        sales_data = {i: 0 for i in range(1, 13)}

        for month, total in monthly_sales:
            sales_data[month] = float(total)

        sales_data_list = list(sales_data.values())

        # 🏆 Top Selling Albums
        top_albums = (
            db.session.query(
                Album.title,
                func.sum(OrderItem.quantity)
            )
            .join(OrderItem)
            .group_by(Album.id)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(5)
            .all()
        )

        return render_template(
            "dashboard.html",
            total_users=total_users,
            total_albums=total_albums,
            total_orders=total_orders,
            total_revenue=total_revenue,
            sales_data=sales_data_list,
            top_album_labels=[a[0] for a in top_albums],
            top_album_data=[a[1] for a in top_albums],
        )