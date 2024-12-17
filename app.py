import matplotlib
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import logging
logging.basicConfig(level=logging.DEBUG)

import matplotlib.pyplot as plt
matplotlib.use('Agg')

from io import BytesIO
import base64

from helpers12 import login_required, usd, name_intials
from main_files.income_expense import ie
from main_files.stocks import stocks
from main_files.mutual_funds import mf
from main_files.real_estate import rs

from main_files.debt import db
from main_files.gold import gl
from main_files.crypto import ct
from main_files.liabilities import lb
#from main_files.fixed_deposit import fd

# Configure application
app = Flask(__name__)

# Register blueprints or routes from other files
app.register_blueprint(ie)
app.register_blueprint(stocks)
app.register_blueprint(mf)
app.register_blueprint(rs)

app.register_blueprint(db)
app.register_blueprint(gl)
app.register_blueprint(ct)
app.register_blueprint(lb)
#app.register_blueprint(fd)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", incorrect_username = "Username field cannot be empty")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", incorrect_password = "Must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return render_template("login.html", incorrect_username = "Invalid username")

        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", incorrect_password =  "Invalid password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/forget-password", methods=["GET", "POST"])
def forget_password():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure First Name was submitted
        if not request.form.get("firstname"):
            return render_template("forget-password.html", incorrect_firstname = "Enter your first name")

        # Ensure First Name was submitted
        elif not request.form.get("lastname"):
            return render_template("forget-password.html", incorrect_lastname = "Enter your last name")

         # Ensure username was submitted
        elif not request.form.get("username"):
            return render_template("forget-password.html", incorrect_username = "Username field cannot be empty")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("forget-password.html", incorrect_password = "Must provide password")

        # Ensure data matches
        user_info = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username is valid
        if len(user_info) != 1:
            return render_template("forget-password.html", incorrect_username = "Username doesn't exists")

        # Ensure name matches as the input
        elif request.form.get("firstname").lower() != user_info[0]["first_name"] or request.form.get("lastname").lower() != user_info[0]["last_name"]:
            return render_template("forget-password.html", incorrect_username = "Details do not match")

        # Change password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("password")), user_info[0]["id"])

        # Login user
        session["user_id"] = user_info[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("forget-password.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure First Name was submitted
        if not request.form.get("firstname"):
            return render_template("register.html", incorrect_firstname = "Enter your first name")

        # Ensure First Name was submitted
        elif not request.form.get("lastname"):
            return render_template("register.html", incorrect_lastname = "Enter your last name")

         # Ensure username was submitted
        elif not request.form.get("username"):
            return render_template("register.html", incorrect_username = "Username field cannot be empty")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("register.html", incorrect_password = "Must provide password")

        # Ensure username does not exsist already
        username = request.form.get("username")
        usernames = db.execute("SELECT username FROM users;")

        for i in usernames:
            if i["username"] == username:
                return render_template("register.html", incorrect_username = "Username already exists")

        # Add data to the database
        db.execute("INSERT INTO users (username, hash, first_name, last_name) VALUES (?, ?, ?, ?)",
                   username, generate_password_hash(request.form.get("password")),
                   request.form.get("firstname").lower(), request.form.get("lastname").lower())

        # Login user
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = user_id[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    nameintials = name_intials()
    firstname = db.execute("SELECT first_name FROM users WHERE id = ?", session["user_id"])

    # Variables to store values of investments
    liabilities = calculate_lb()
    stocks_value = calculate_stocks()
    mutual_funds = calculate_mf_value()
    real_estate = calculate_rf()
    #international = calculate_inter()
    debt_value = calculate_db1()  # Rename variable for clarity
    gold = calculate_gl()
    crypto = calculate_ct()


    sum_values = (stocks_value + mutual_funds + real_estate +
                  debt_value + gold + crypto)
    networth = sum_values - liabilities

    # Saving pie-chart image to base64 for HTML display
    if sum_values != 0:
        image_base64 = pie_chart(stocks_value, mutual_funds, real_estate,
                                 debt_value, gold, crypto)
    else:
        image_base64 = pie_chart(1, 1, 1, 1, 1, 1)

    # Redirect user to index page
    return render_template("index.html",
                           nameintials=nameintials,
                           page_title="Home",
                           first_name=firstname[0]["first_name"].upper(),
                           networth=usd(networth),
                           liabilities=usd(liabilities),
                           stocks_value=usd(stocks_value),
                           mutual_funds=usd(mutual_funds),
                           real_estate=usd(real_estate),
                           #international=usd(international),
                           debt=usd(debt_value),  # Send as 'debt'
                           gold=usd(gold),
                           crypto=usd(crypto),
                           image_base64=image_base64)


# Functions to display the stats on index page
def calculate_stocks():
    stocks = db.execute("SELECT price_of_stock, quantity FROM stocks WHERE user_id = ?", session["user_id"])
    totalstockvalue = sum(stock["price_of_stock"] * stock["quantity"] for stock in stocks)
    return totalstockvalue

def calculate_mf_value():
    mutual_funds = db.execute("SELECT price_of_mf, quantity FROM mutual_funds WHERE user_id = ?", session["user_id"])
    totalmfvalue = sum(mf["price_of_mf"] * mf["quantity"] for mf in mutual_funds)
    return totalmfvalue



def calculate_rf():
    real_estate = db.execute("SELECT price_of_rs FROM real_estate WHERE user_id = ?", session["user_id"])
    totalrsvalue = sum(rs["price_of_rs"] for rs in real_estate)
    return totalrsvalue

# def calculate_inter():
#     international = db.execute("SELECT price_of_inter, quantity FROM international WHERE user_id = ?", session["user_id"])
#     totalintervalue = sum(inter["price_of_inter"] * inter["quantity"] for inter in international)
#     return totalintervalue

def calculate_db1():
    # Fetch Fixed Deposit/debt data
    debt = db.execute("SELECT price_of_db, tenure FROM debt WHERE user_id = ?", session["user_id"])
    total_db_value = sum(db_item["price_of_db"] * int(db_item["tenure"]) for db_item in debt)
    return total_db_value


def calculate_gl():
    gold = db.execute("SELECT price_of_gl FROM gold WHERE user_id = ?", session["user_id"])
    totalglvalue = sum(gl["price_of_gl"] for gl in gold)
    return totalglvalue

def calculate_ct():
    crypto = db.execute("SELECT price_of_ct, quantity FROM crypto WHERE user_id = ?", session["user_id"])
    totalctvalue = sum(ct["price_of_ct"] * ct["quantity"] for ct in crypto)
    return totalctvalue

def calculate_lb():
    liabilities = db.execute("SELECT price_of_lb FROM liabilities WHERE user_id = ?", session["user_id"])
    totallbvalue = sum(lb["price_of_lb"] for lb in liabilities)
    return totallbvalue

def pie_chart(stocks_value, mutual_funds, real_estate,  debt, gold, crypto):
    labels = ['Stocks', 'Mutual Funds', 'Real Estate',  'Fixed Deposit', 'Gold', 'Crypto']
    values = [stocks_value, mutual_funds, real_estate,  debt, gold, crypto]

    custom_colors = ['#e6e6fa', 'pink', '#90ee90', '#ffdab9', 'gold', '#f08080']

    plt.figure(figsize=(4, 4))  # 4x4 inches for display consistency
    plt.pie(values, labels=None, autopct=None, startangle=90, colors=custom_colors)
    plt.axis('equal')

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight', pad_inches=0)
    image_stream.seek(0)

    return base64.b64encode(image_stream.read()).decode('utf-8')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)


