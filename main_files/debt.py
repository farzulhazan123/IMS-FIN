import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_session import Session

from helpers12 import login_required, usd, name_intials

# Configure application
db = Blueprint('debt', __name__)

# Configure CS50 Library to use SQLite database
db1 = SQL("sqlite:///finance.db")

#type = ["Debt Mutual Funds", "Bonds", "Fixed Deposit", "Government Securities", "Saving Acc Balance", "Others"]

@db.route("/debt")
@login_required
def db_page():
    # Extracting intials to a variable
    nameintials = name_intials()

    # Extracting the debt owned by the user
    debt = db1.execute("SELECT * FROM debt WHERE user_id = ?", session["user_id"])

    # Modifying the value to display on the webpage
    i = 1
    totalvalue = 0
    for db in debt:
        totalvalue += db["price_of_db"]
        db["price_of_db"] = usd(db["price_of_db"])
        db["number"] = i
        i += 1

    # Returning debt.html page
    return render_template("debt.html",
                           nameintials=nameintials,
                           page_title="Fixed Deposit",
                           debt = debt,
                           totalvalue=usd(totalvalue))


@db.route("/add-db", methods=["GET", "POST"])
@login_required
def add_db():
    nameintials = name_intials()

    # Verifying the input by the user
    if request.method == "POST":
        if not request.form.get("dbname"):
            return render_template("add-debt.html",
                                   nameintials=nameintials,
                                   page_title="Add Fixed Deposit",
                                   dbname="Enter a title")

        if not request.form.get("tenure"):
            return render_template("add-debt.html",
                                   nameintials=nameintials,
                                   page_title="Add Fixed Deposit",
                                   type="Must choose one of the option")

        if not request.form.get("priceofdb"):
            return render_template("add-debt.html",
                                   nameintials=nameintials,
                                   page_title="Add Fixed Deposit",
                                   priceofdb ="Must enter the value")

        if int(request.form.get("priceofdb")) < 1:
            return render_template("add-debt.html",
                                   nameintials=nameintials,
                                   page_title="Add Fixed Deposit",
                                   priceofdb="Enter a valid value")

        '''if request.form.get("type") not in type:
            return render_template("add-debt.html",
                                   nameintials=nameintials,
                                   page_title="Add Stocks",
                                   type="Choose a valid option from the list")'''

        db1.execute("INSERT INTO debt (user_id, db_name,price_of_db,tenure) VALUES (?, ?, ?, ?)",
                   session["user_id"], request.form.get("dbname"),
                    request.form.get("priceofdb"),request.form.get("tenure"))

        return redirect("/debt")

    else:
        # Returning add-debt.html page
        return render_template("add-debt.html",
                               nameintials=nameintials,
                               page_title="Add Fixed Deposit")


@db.route("/delete-db", methods=["POST"])
@login_required
def delete_db():
    # Deleting the Debt from the table
    db1.execute("DELETE FROM debt WHERE id = ?", request.form.get("db-id"))

    # Redirecting to Debt webpage
    return redirect("/debt")

