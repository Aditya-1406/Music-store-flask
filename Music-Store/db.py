from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

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
    created_at = db.Column(db.DateTime,default=datetime.now())


    def __repr__(self):
        return f"<User {self.email}>"