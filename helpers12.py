import csv
import datetime
import pytz
from functools import wraps
from flask import redirect, render_template, session
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


def login_required(f):
    """
    Decorator to require login for routes.

    Wraps a function to enforce that the user is logged in. If the user isn't logged in,
    they are redirected to the login page.

    Reference: https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def usd(value):
    if value is None:
        return "Rs. 0.00"

        # Just use ₹ symbol for formatting
    return f"Rs. {value:,.2f}"

def name_intials():
    """
    Return the initials of the currently logged-in user.

    Extracts and formats the initials (uppercase) based on the user's
    first and last names stored in the `users` table in the database.
    """
    user = db.execute("SELECT first_name, last_name FROM users WHERE id = ?", session["user_id"])
    if user:
        initials = (user[0]["first_name"][0] + user[0]["last_name"][0]).upper()
        return initials
    return "NN"  # Default for No Name
