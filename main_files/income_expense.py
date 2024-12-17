import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_session import Session

from helpers12 import login_required, usd, name_intials

# Configure application
ie = Blueprint('ie', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Global variables
global income
global expense
global total_income
global total_expense
income_type = ["Post Tax Salary", "Business Income", "Rental Income", "Others"]
expense_type = ["Monthly Expense", "Loan", "Insurance Premiums", "Others"]

@ie.route("/income&expense")
@login_required
def income_expense():
    """Sell shares of stock"""
    # Extracting intials to a variable
    nameintials = name_intials()

    # Displaying income and expense on the table
    global income
    global expense
    income = db.execute("SELECT * FROM income WHERE user_id = ?", session["user_id"])
    expense = db.execute("SELECT * FROM expense WHERE user_id = ?", session["user_id"])

    # Convertin amound into us dollar
    for i in income:
        i["amount"] = usd(i["amount"])

    for j in expense:
        j["amount"] = usd(j["amount"])

    # Calculation total income and expense of the person
    global total_income
    global total_expense
    total_in = db.execute("SELECT SUM(amount) AS total_income FROM income WHERE user_id = ?", session["user_id"])
    total_income = usd(total_in[0]["total_income"])
    total_ex = db.execute("SELECT SUM(amount) AS total_expense FROM expense WHERE user_id = ?", session["user_id"])
    total_expense = usd(total_ex[0]["total_expense"])

    # Returning the template of income-expense.html
    return render_template("income-expense.html",
                           nameintials=nameintials,
                           page_title="Income & Expense",
                           expenses=expense,
                           incomes=income,
                           total_income = total_income,
                           total_expense = total_expense)


@ie.route("/add-expense", methods=["POST"])
@login_required
def add_expense():

    nameintials = name_intials()

    # Verifying input by the user
    if not request.form.get("expense-type"):
        return render_template("income-expense.html",
                               nameintials=nameintials,
                               page_title="Income & Expense",
                               incorrect_expense="Must select type of expense",
                               expenses=expense,
                               incomes=income,
                               total_income = total_income,
                               total_expense = total_expense)

    if request.form.get("expense-type") not in expense_type:
        return render_template("income-expense.html",
                               nameintials=nameintials,
                               page_title="Income & Expense",
                               incorrect_expense="Select type of expense available in the list",
                               expenses=expense,
                               incomes=income,
                               total_income = total_income,
                               total_expense = total_expense)

    # Adding expense to the expense-table
    db.execute("INSERT INTO expense (user_id, type, amount) VALUES (?, ?, ?)",
               session["user_id"], request.form.get("expense-type"), request.form.get("expense-input"))

    # Redirecting it to income & expense page
    return redirect("/income&expense")


@ie.route("/add-income", methods=["POST"])
@login_required
def add_income():

    nameintials = name_intials()

    # Verifying input by the user
    if not request.form.get("income-type"):
        return render_template("income-expense.html",
                               nameintials=nameintials,
                               page_title="Income & Expense",
                               incorrect_income="Must select type of income",
                               expenses=expense,
                               incomes=income,
                               total_income = total_income,
                               total_expense = total_expense)

    if request.form.get("income-type") not in income_type:
        return render_template("income-expense.html",
                               nameintials=nameintials,
                               page_title="Income & Expense",
                               incorrect_income="Select type of income available in the list",
                               expenses=expense,
                               incomes=income,
                               total_income = total_income,
                               total_expense = total_expense)

    # Adding expense to the income-table
    db.execute("INSERT INTO income (user_id, type, amount) VALUES (?, ?, ?)",
               session["user_id"], request.form.get("income-type"), request.form.get("income-input"))

    # Redirecting it to income & expense page
    return redirect("/income&expense")


@ie.route("/edit-expense-form", methods=["POST"])
@login_required
def edit_expense_form():
    nameintials = name_intials()
    # Returning edit expense form
    return render_template("/edit-expense.html",
                            nameintials=nameintials,
                            page_title="Income & Expense",
                            expense_type=request.form.get("expense-type"),
                            id=request.form.get("expense-id"))



@ie.route("/delete-expense", methods=["POST"])
@login_required
def delete_expense():
    # Deleting the expense row
    db.execute("DELETE FROM expense WHERE id = ?", request.form.get("expense-id"))

    # Redirecting it to income & expense page
    return redirect("/income&expense")


@ie.route("/edit-income-form", methods=["POST"])
@login_required
def edit_income_form():
    nameintials = name_intials()
    # Returning edit income form
    return render_template("/edit-income.html",
                            nameintials=nameintials,
                            page_title="Income & Expense",
                            income_type=request.form.get("income-type"),
                            id=request.form.get("income-id"))


@ie.route("/delete-income", methods=["POST"])
@login_required
def delete_income():
    # Deleting the income row
    db.execute("DELETE FROM income WHERE id = ?", request.form.get("income-id"))
    # Redirecting it to income & expense page
    return redirect("/income&expense")


@ie.route("/edit-income", methods=["POST"])
@login_required
def edit_income():
    # Editing the income in db
    

    # Redirecting to the income & expense page
    return redirect("/income&expense")


@ie.route("/edit-expense", methods=["POST"])
@login_required
def edit_expense():
    # Editing the expense in db
    db.execute("UPDATE expense SET amount = ? WHERE id = ?", request.form.get("new-expense"), request.form.get("expense-id"))

    # Redirecting to the income & expense page
    return redirect("/income&expense")
