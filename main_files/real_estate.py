import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_session import Session

from helpers12 import login_required, usd, name_intials

# Configure application
rs = Blueprint('real_estate', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

type = ["Commercial Real Estate", "REITs", "Fractional Ownership", "Others"]

@rs.route("/real_estate")
@login_required
def rs_page():
    # Extracting intials to a variable
    nameintials = name_intials()

    # Extracting the real_estate owned by the user
    real_estate = db.execute("SELECT * FROM real_estate WHERE user_id = ?", session["user_id"])

    # Modifying the value to display on the webpage
    i = 1
    totalvalue = 0
    for rs in real_estate:
        totalvalue += rs["price_of_rs"]
        rs["price_of_rs"] = usd(rs["price_of_rs"])
        rs["number"] = i
        i += 1

    # Returning real-estate.html page
    return render_template("real-estate.html",
                           nameintials=nameintials,
                           page_title="Real Estate",
                           real_estate = real_estate,
                           totalvalue=usd(totalvalue))


@rs.route("/add-rs", methods=["GET", "POST"])
@login_required
def add_rs():
    nameintials = name_intials()

    # Verifying the input by the user
    if request.method == "POST":
        if not request.form.get("rsname"):
            return render_template("add-real-estate.html",
                                   nameintials=nameintials,
                                   page_title="Add Real Estate",
                                   rsname="Enter a title for your real estate")

        if not request.form.get("type"):
            return render_template("add-real-estate.html",
                                   nameintials=nameintials,
                                   page_title="Add Real Estate",
                                   type="Must choose one of the option")

        if not request.form.get("priceofrs"):
            return render_template("add-real-estate.html",
                                   nameintials=nameintials,
                                   page_title="Add Real Estate",
                                   priceofrs ="Must enter the value of real rstate")

        if int(request.form.get("priceofrs")) < 1:
            return render_template("add-real-estate.html",
                                   nameintials=nameintials,
                                   page_title="Add Real Estate",
                                   priceofrs="Enter a valid value")

        if request.form.get("type") not in type:
            return render_template("add-real-estate.html",
                                   nameintials=nameintials,
                                   page_title="Add Stocks",
                                   type="Choose a valid option from the list")

        db.execute("INSERT INTO real_estate (user_id, rs_name, type, price_of_rs) VALUES (?, ?, ?, ?)",
                   session["user_id"], request.form.get("rsname"),
                   request.form.get("type"), request.form.get("priceofrs"))

        return redirect("/real_estate")

    else:
        # Returning add-real-estate.html page
        return render_template("add-real-estate.html",
                               nameintials=nameintials,
                               page_title="Add Real Estate")


@rs.route("/delete-rs", methods=["POST"])
@login_required
def delete_rs():
    # Deleting the Real Estate from the table
    db.execute("DELETE FROM real_estate WHERE id = ?", request.form.get("rs-id"))

    # Redirecting to Real Estate webpage
    return redirect("/real_estate")

