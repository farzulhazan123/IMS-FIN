import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_session import Session

from helpers12 import login_required, usd, name_intials

# Configure application
mf = Blueprint('mutual_funds', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@mf.route("/mutual_funds")
@login_required
def mf_page():
    # Extracting intials to a variable
    nameintials = name_intials()

    # Extracting the mutual_funds owned by the user
    mutual_funds = db.execute("SELECT * FROM mutual_funds WHERE user_id = ?", session["user_id"])

    # Modifying the value to display on the webpage
    i = 1
    totalvalue = 0
    for mf in mutual_funds:
        mf["total_value_of_mf"] = usd(mf["price_of_mf"] * mf["quantity"])
        totalvalue += mf["price_of_mf"] * mf["quantity"]
        mf["price_of_mf"] = usd(mf["price_of_mf"])
        mf["number"] = i
        i += 1

    # Returning mutual-funds.html page
    return render_template("mutual-funds.html",
                           nameintials=nameintials,
                           page_title="Mutual Funds",
                           mutual_funds = mutual_funds,
                           totalvalue=usd(totalvalue))


@mf.route("/add-mf", methods=["GET", "POST"])
@login_required
def add_mf():
    nameintials = name_intials()

    # Verifying the input by the user
    if request.method == "POST":
        if not request.form.get("mfname"):
            return render_template("add-mutual-funds.html",
                                   nameintials=nameintials,
                                   page_title="Add Mutual Funds",
                                   mfname="Enter a MF name")

        if not request.form.get("quantity"):
            return render_template("add-mutual-funds.html",
                                   nameintials=nameintials,
                                   page_title="Add Mutual Funds",
                                   quantity="Must enter the number of shares")

        if not request.form.get("priceofmf"):
            return render_template("add-mutual-funds.html",
                                   nameintials=nameintials,
                                   page_title="Add Mutual Funds",
                                   priceofmf ="Must enter the price of MF")


        if int(request.form.get("quantity")) < 1:
            return render_template("add-mutual-funds.html",
                                   nameintials=nameintials,
                                   page_title="Add Mutual Funds",
                                   quantity="Enter valid number of shares")

        if int(request.form.get("priceofmf")) < 1:
            return render_template("add-mutual-funds.html",
                                   nameintials=nameintials,
                                   page_title="Add Mutual Funds",
                                   priceofmf="Enter valid price of MF")

        db.execute("INSERT INTO mutual_funds (user_id, mf_name, quantity, price_of_mf) VALUES (?, ?, ?, ?)",
                   session["user_id"], request.form.get("mfname"),
                   request.form.get("quantity"), request.form.get("priceofmf"))

        return redirect("/mutual_funds")

    else:
        # Returning add-mutual-funds.html page
        return render_template("add-mutual-funds.html",
                               nameintials=nameintials,
                               page_title="Add Mutual Funds")


@mf.route("/delete-mf", methods=["POST"])
@login_required
def delete_mf():
    # Deleting the mutual fund from the table
    db.execute("DELETE FROM mutual_funds WHERE id = ?", request.form.get("mf-id"))

    # Redirecting to mutual funds webpage
    return redirect("/mutual_funds")

