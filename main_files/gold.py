import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_session import Session

from helpers12 import login_required, usd, name_intials

# Configure application
gl = Blueprint('gold', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

type = ["SGB", "Physical Gold", "Digital Gold", "Others"]

@gl.route("/gold")
@login_required
def gl_page():
    # Extracting intials to a variable
    nameintials = name_intials()

    # Extracting the gold owned by the user
    gold = db.execute("SELECT * FROM gold WHERE user_id = ?", session["user_id"])

    # Modifying the value to display on the webpage
    i = 1
    totalvalue = 0
    for gl in gold:
        totalvalue += gl["price_of_gl"]
        gl["price_of_gl"] = usd(gl["price_of_gl"])
        gl["number"] = i
        i += 1

    # Returning gold.html page
    return render_template("gold.html",
                           nameintials=nameintials,
                           page_title="Gold",
                           gold = gold,
                           totalvalue=usd(totalvalue))


@gl.route("/add-gl", methods=["GET", "POST"])
@login_required
def add_gl():
    nameintials = name_intials()

    # Verifying the input by the user
    if request.method == "POST":
        if not request.form.get("glname"):
            return render_template("add-gold.html",
                                   nameintials=nameintials,
                                   page_title="Add Gold",
                                   glname="Enter a title")

        if not request.form.get("type"):
            return render_template("add-gold.html",
                                   nameintials=nameintials,
                                   page_title="Add Gold",
                                   type="Must choose one of the option")

        if not request.form.get("priceofgl"):
            return render_template("add-gold.html",
                                   nameintials=nameintials,
                                   page_title="Add Gold",
                                   priceofgl ="Must enter a value")

        if int(request.form.get("priceofgl")) < 1:
            return render_template("add-gold.html",
                                   nameintials=nameintials,
                                   page_title="Add Gold",
                                   priceofgl="Enter a valid value")

        if request.form.get("type") not in type:
            return render_template("add-gold.html",
                                   nameintials=nameintials,
                                   page_title="Add Stocks",
                                   type="Choose a valid option from the list")

        db.execute("INSERT INTO gold (user_id, gl_name, type, price_of_gl) VALUES (?, ?, ?, ?)",
                   session["user_id"], request.form.get("glname"),
                   request.form.get("type"), request.form.get("priceofgl"))

        return redirect("/gold")

    else:
        # Returning add-gold.html page
        return render_template("add-gold.html",
                               nameintials=nameintials,
                               page_title="Add Gold")


@gl.route("/delete-gl", methods=["POST"])
@login_required
def delete_gl():
    # Deleting the Gold from the table
    db.execute("DELETE FROM gold WHERE id = ?", request.form.get("gl-id"))

    # Redirecting to Gold webpage
    return redirect("/gold")

