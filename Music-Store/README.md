# 🎵 Music Store – Flask Web Application

A full-featured Music Store web application built using **Flask**, **MySQL**, and Bootstrap.  
This project includes user authentication, album management, cart system, order processing, and an admin dashboard with analytics charts.

---

## 🚀 Features

### 👤 User Features
- User Registration & Login with real time OTP
- Browse Albums
- Add to Cart
- Place Orders
- Order History
- Search Orders
- Email Notifications

### 🛠 Admin Features
- Admin Dashboard
- Monthly Sales Chart
- Top Selling Albums Chart
- Manage Users
- Manage Albums
- View Orders
- Revenue Statistics

---

## 🏗 Tech Stack

- **Backend:** Flask  
- **Database:** MySQL  
- **ORM:** SQLAlchemy  
- **Frontend:** Bootstrap 5  
- **Charts:** Chart.js  
- **Authentication:** Flask Session  

---

# 📦 Project Setup Guide

Follow these steps carefully to run the project locally.

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/music-store.git
cd music-store
```

---

## 2️⃣ Create Virtual Environment

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, generate it:

```bash
pip freeze > requirements.txt
```

---

## 4️⃣ Setup MySQL Database

Login to MySQL and create database:

```sql
CREATE DATABASE music_store;
```

Update your database configuration inside your Flask app:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://username:password@localhost/music_store"
```

Replace:
- `username`
- `password`

with your MySQL credentials.

---

## 5️⃣ Initialize Database

Start Flask shell:

```bash
flask shell
```

Then run:

```python
from app import db
db.create_all()
```

---

## 6️⃣ Run the Application

```bash
flask run
```

OR

```bash
python run.py
```

Open browser:

```
http://127.0.0.1:5000/
```

---

# 🔐 Admin Access

To create an admin user manually:

update an existing user’s `role` field to `admin` in the database.

---

# 📊 Dashboard Analytics

The Admin Dashboard includes:

- Total Users
- Total Albums
- Total Orders
- Total Revenue
- Monthly Revenue Chart
- Top Selling Albums Pie Chart

Charts are powered by **Chart.js**.

---

# ⚙️ Optional: Use Environment Variables (Recommended)

Create a `.env` file:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=mysql+pymysql://username:password@localhost/music_store
```

Install dotenv:

```bash
pip install python-dotenv
```

---

# 🧪 Common Issues & Fixes

### ❌ Charts Not Showing
- Ensure Chart.js CDN is included
- Convert Decimal values to `int` or `float` before sending to template

### ❌ MySQL strftime Error
If using MySQL, use:

```python
func.month()
func.year()
```

NOT:

```python
func.strftime()
```

---

# 🌟 Future Improvements

- Payment Gateway Integration
- Order Status Tracking
- Product Reviews
- Deployment (Render / Railway / AWS)

---

# 📜 License

This project is created for educational purposes.

---

# 👨‍💻 Author

Developed as a Full Stack Flask Project.