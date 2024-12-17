import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_session import Session

from helpers12 import login_required, usd, name_intials

# Configure application
ct = Blueprint('crypto', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@ct.route("/crypto")
@login_required
def ct_page():
    # Extracting intials to a variable
    nameintials = name_intials()

    # Extracting the crypto owned by the user
    crypto = db.execute("SELECT * FROM crypto WHERE user_id = ?", session["user_id"])

    # Modifying the value to display on the webpage
    i = 1
    totalvalue = 0
    for ct in crypto:
        ct["total_value_of_ct"] = usd(ct["price_of_ct"] * ct["quantity"])
        totalvalue += ct["price_of_ct"] * ct["quantity"]
        ct["price_of_ct"] = usd(ct["price_of_ct"])
        ct["number"] = i
        i += 1

    # Returning crypto.html page
    return render_template("crypto.html",
                           nameintials=nameintials,
                           page_title="Crypto",
                           crypto = crypto,
                           totalvalue=usd(totalvalue))


@ct.route("/add-ct", methods=["GET", "POST"])
@login_required
def add_ct():
    nameintials = name_intials()

    # Verifying the input by the user
    if request.method == "POST":
        if not request.form.get("ctname"):
            return render_template("add-crypto.html",
                                   nameintials=nameintials,
                                   page_title="Add Crypto",
                                   ctname="Enter a token name")

        if not request.form.get("quantity"):
            return render_template("add-crypto.html",
                                   nameintials=nameintials,
                                   page_title="Add Crypto",
                                   quantity="Must enter a number")

        if not request.form.get("priceofct"):
            return render_template("add-crypto.html",
                                   nameintials=nameintials,
                                   page_title="Add Crypto",
                                   priceofct ="Must enter the price of 1 crypto")


        if float(request.form.get("quantity")) < 0:
            return render_template("add-crypto.html",
                                   nameintials=nameintials,
                                   page_title="Add Crypto",
                                   quantity="Enter valid number of token")

        if float(request.form.get("priceofct")) < 0:
            return render_template("add-crypto.html",
                                   nameintials=nameintials,
                                   page_title="Add Crypto",
                                   priceofct="Enter valid price of crypto")

        db.execute("INSERT INTO crypto (user_id, ct_name, quantity, price_of_ct) VALUES (?, ?, ?, ?)",
                   session["user_id"], request.form.get("ctname"),
                   request.form.get("quantity"), request.form.get("priceofct"))

        return redirect("/crypto")

    else:
        # Returning add-crypto.html page
        return render_template("add-crypto.html",
                               nameintials=nameintials,
                               page_title="Add Crypto")


@ct.route("/delete-ct", methods=["POST"])
@login_required
def delete_ct():
    # Deleting the Crypto from the table
    db.execute("DELETE FROM crypto WHERE id = ?", request.form.get("ct-id"))

    # Redirecting to Crypto webpage
    return redirect("/crypto")

