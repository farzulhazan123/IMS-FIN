import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_session import Session

from helpers12 import login_required, usd, name_intials

# Configure application
stocks = Blueprint('stocks', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

classifications = ["Large Cap", "Mid Cap", "Small Cap", "Others"]

@stocks.route("/stocks")
@login_required
def stock():
    # Extracting intials to a variable
    nameintials = name_intials()

    # Extracting the stocks owned by the user
    stocks = db.execute("SELECT * FROM stocks WHERE user_id = ?", session["user_id"])

    # Modifying the value to display on the webpage
    i = 1
    totalvalue = 0
    for stock in stocks:
        stock["total_value_of_stock"] = usd(stock["price_of_stock"] * stock["quantity"])
        totalvalue += stock["price_of_stock"] * stock["quantity"]
        stock["price_of_stock"] = usd(stock["price_of_stock"])
        stock["number"] = i
        i += 1

    # Returning stocks.html page
    return render_template("stocks.html",
                           nameintials=nameintials,
                           page_title="Stocks",
                           stocks = stocks,
                           totalvalue=usd(totalvalue))


@stocks.route("/add-stocks", methods=["GET", "POST"])
@login_required
def add_stock():
    nameintials = name_intials()

    # Verifying the input by the user
    if request.method == "POST":
        if not request.form.get("stockname"):
            return render_template("add-stocks.html",
                                   nameintials=nameintials,
                                   page_title="Add Stocks",
                                   stockname="Enter a stock name")

        if not request.form.get("classifications"):
            return render_template("add-stocks.html",
                                   nameintials=nameintials,
                                   page_title="Add Stocks",
                                   classifications="Must choose one of the options")

        if not request.form.get("quantity"):
            return render_template("add-stocks.html",
                                   nameintials=nameintials,
                                   page_title="Add Stocks",
                                   quantity="Must enter the number of shares")

        if not request.form.get("priceofstock"):
            return render_template("add-stocks.html",
                                   nameintials=nameintials,
                                   page_title="Add Stocks",
                                   priceofstock="Must enter the price of stock")

        if request.form.get("classifications") not in classifications:
            return render_template("add-stocks.html",
                                   nameintials=nameintials,
                                   page_title="Add Stocks",
                                   classifications="Choose a valid option from the list")


        if int(request.form.get("quantity")) < 1:
            return render_template("add-stocks.html",
                                   nameintials=nameintials,
                                   page_title="Add Stocks",
                                   quantity="Enter valid number of shares")

        if float(request.form.get("priceofstock")) < 0:
            return render_template("add-stocks.html",
                                   nameintials=nameintials,
                                   page_title="Add Stocks",
                                   priceofstock="Enter valid price of stock")

        db.execute("INSERT INTO stocks (user_id, stock_name, classification, quantity, price_of_stock) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], request.form.get("stockname"), request.form.get("classifications"),
                   request.form.get("quantity"), request.form.get("priceofstock"))

        return redirect("/stocks")

    else:
        # Returning add-stocks.html page
        return render_template("add-stocks.html",
                               nameintials=nameintials,
                               page_title="Add Stocks")


@stocks.route("/delete-stock", methods=["POST"])
@login_required
def delete_stock():
    # Deleting the stock from the table
    db.execute("DELETE FROM stocks WHERE id = ?", request.form.get("stock-id"))

    # Redirecting to stock webpage
    return redirect("/stocks")

