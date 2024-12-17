import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_session import Session

from helpers12 import login_required, usd, name_intials

# Configure application
lb = Blueprint('liabilities', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@lb.route("/liabilities")
@login_required
def lb_page():
    # Extralbing intials to a variable
    nameintials = name_intials()

    # Extralbing the liabilities owned by the user
    liabilities = db.execute("SELECT * FROM liabilities WHERE user_id = ?", session["user_id"])

    # Modifying the value to display on the webpage
    i = 1
    totalvalue = 0
    for lb in liabilities:
        totalvalue += lb["price_of_lb"]
        lb["price_of_lb"] = usd(lb["price_of_lb"])
        lb["number"] = i
        i += 1

    # Returning liabilities.html page
    return render_template("liabilities.html",
                           nameintials=nameintials,
                           page_title="Liabilities",
                           liabilities = liabilities,
                           totalvalue=usd(totalvalue))


@lb.route("/add-lb", methods=["GET", "POST"])
@login_required
def add_lb():
    nameintials = name_intials()

    # Verifying the input by the user
    if request.method == "POST":
        if not request.form.get("lbname"):
            return render_template("add-liabilities.html",
                                   nameintials=nameintials,
                                   page_title="Add liabilities",
                                   lbname="Enter a title")

        if not request.form.get("priceoflb"):
            return render_template("add-liabilities.html",
                                   nameintials=nameintials,
                                   page_title="Add liabilities",
                                   priceoflb ="Must enter a value")

        if int(request.form.get("priceoflb")) < 1:
            return render_template("add-liabilities.html",
                                   nameintials=nameintials,
                                   page_title="Add liabilities",
                                   priceoflb="Enter a valid value")

        db.execute("INSERT INTO liabilities (user_id, lb_name, price_of_lb) VALUES (?, ?, ?)",
                   session["user_id"], request.form.get("lbname"),
                   request.form.get("priceoflb"))

        return redirect("/liabilities")

    else:
        # Returning add-liabilities.html page
        return render_template("add-liabilities.html",
                               nameintials=nameintials,
                               page_title="Add liabilities")


@lb.route("/delete-lb", methods=["POST"])
@login_required
def delete_lb():
    # Deleting the liabilities from the table
    db.execute("DELETE FROM liabilities WHERE id = ?", request.form.get("lb-id"))

    # Redirecting to liabilities webpage
    return redirect("/liabilities")

@lb.route("/edit-lb", methods=["POST"])
@login_required
def edit_lb():

    # Editing the liabilities from the table
    db.execute("UPDATE liabilities SET price_of_lb = ? WHERE id = ?", request.form.get("priceoflb"), request.form.get("lb-id"))

    # Redirecting to liabilities webpage
    return redirect("/liabilities")
