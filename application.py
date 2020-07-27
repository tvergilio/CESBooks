import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show all books"""

    rows = db.execute("SELECT * FROM books WHERE stock_new > 0 OR stock_used > 0 ORDER BY level, title")
    bookstock =[]
    for row in rows:
        bookstock.append([row['title'], row['level'], row['edition'], row['isbn'], row['stock_new'], row['stock_used']])
    return render_template("index.html", bookstock=bookstock)


@app.route("/transactions")
@login_required
def transactions():
    """Show history of transactions"""
    # get transaction history
    rows = db.execute("SELECT * FROM transactions ORDER BY date DESC")
    history =[]
    for row in rows:
        history.append([row['date'], row['transaction_type'], row['book_id'],
                        row['price'], row['student'],row['user_id']])

    # redirect user to index page
    return render_template("transactions.html", transactions=history)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        # Display form for user to create account
        return render_template("register.html")
    else:
        # register the new user
        # check username is not blank
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # check password id not blank
        if not request.form.get("password"):
            return apology('must provide password', 403)
        # check username is unique
        if db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username")):
            return apology("username already taken", 403)
        # check password and confirmation are same
        if request.form.get("password") != request.form.get("confirm-password"):
            return apology("password and confirmation do not match", 403)
        # hash the password and create row in db
        db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)",
            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        # make sure that the new user is logged in
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # set the session so we know who is logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell a book"""
    rows = db.execute("SELECT * FROM books WHERE stock_new > 0 OR stock_used > 0 ORDER BY level")
    bookstock =[]
    transaction = "SELL"
    for row in rows:
        bookstock.append([row['title'], row['level'], row['edition'], row['isbn'], row['stock_new'], row['stock_used'], row['price_new'], row['price_used']])
    if request.method == "GET":
        return render_template("sell.html", stocks=bookstock)
    else:
        isbn = request.form.get("isbn")
        used = request.form.get("used")
        number_to_sell = int(request.form.get("number_to_sell"))
        student = request.form.get("student")
        # check database to make sure book is in stock
        if used:
            book_in_stock = db.execute("SELECT stock_used, price_used from books WHERE isbn = :isbn", isbn = isbn)
        else:
            book_in_stock = db.execute("SELECT stock_new, price_new from books WHERE isbn = :isbn", isbn = isbn)

        if not book_in_stock:
            return apology('sorry, out of stock')
        elif used:
            db.execute("UPDATE books SET stock_used = :books_left WHERE isbn = :isbn", isbn = isbn,
                    books_left = int(book_in_stock[0]["stock_used"]) - 1)
            db.execute("INSERT INTO transactions(transaction_type, user_id, book_id, price, date, student) VALUES (:trans, :user, :book, :price, :date, :student)",
                        trans=transaction, user=session["user_id"], book=isbn, price=(book_in_stock[0]["price_used"]), date=date.today(), student=student)
        else:
            db.execute("UPDATE books SET stock_new = :books_left WHERE isbn = :isbn", isbn = isbn,
                    books_left = int(book_in_stock[0]["stock_new"]) - 1)
            db.execute("INSERT INTO transactions(transaction_type, user_id, book_id, price, date, student) VALUES (:trans, :user, :book, :price, :date, :student)",
                    trans=transaction, user=session["user_id"], book=isbn, price=(book_in_stock[0]["price_new"]), date=date.today(), student=student)

        flash("Sold!")
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy a book"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        isbn = request.form.get("isbn")
        student = request.form.get("student")
        used = request.form.get("used")
        transaction = "BUY"
        # get current stock level
        book_in_stock = db.execute("SELECT * from books WHERE isbn = :isbn", isbn = isbn)
        try:
            # add one to stock level and write to database
            db.execute("UPDATE books SET stock_used = :books WHERE isbn = :isbn", isbn = isbn, books = book_in_stock[0]["stock_used"] + 1)        
            # record in transactions database
            db.execute("INSERT INTO transactions(transaction_type, user_id, book_id, price, date, student) VALUES (:trans, :user, :book, :price, :date, :student)",
                            trans=transaction, user=session["user_id"], book=isbn, price= -10, date=date.today(), student=student)
            flash("Bought!")
            return redirect("/")
        except IndexError:
            flash("Not in database. Please add details of new book.")
            return render_template("add.html")



@app.route("/swap", methods=["GET", "POST"])
@login_required
def swap():
    if request.method == "GET":
        # Display form for user to enter stock to search
        return render_template("swap.html")
    else:
        book_in = request.form.get("book_in")
        book_in_used = request.form.get("book_in_used")
        book_out = request.form.get("book_out")
        book_out_used = request.form.get("book_out_used")
        student = request.form.get("student")
        # update table by adding book coming in
        if book_in_used:
            stock_used = db.execute("SELECT stock_used from books WHERE isbn = :isbn", isbn = book_in)[0]['stock_used']
            db.execute("UPDATE books SET stock_used = :number WHERE isbn = :isbn", number = stock_used + 1, isbn = book_in)
        else:    
            stock_new = db.execute("SELECT stock_new from books WHERE isbn = :isbn", isbn = book_in)[0]['stock_new']
            db.execute("UPDATE books SET stock_new = :number WHERE isbn = :isbn", number = stock_new + 1, isbn = book_in)

        # update table by subtracting book going out
        if book_out_used:
            stock_used = db.execute("SELECT stock_used from books WHERE isbn = :isbn", isbn = book_out)[0]['stock_used']
            db.execute("UPDATE books SET stock_used = :number WHERE isbn = :isbn", number = stock_used -1, isbn = book_out)
        else:    
            stock_new = db.execute("SELECT stock_new from books WHERE isbn = :isbn", isbn = book_out)[0]['stock_new']
            db.execute("UPDATE books SET stock_new = :number WHERE isbn = :isbn", number = stock_new - 1, isbn = book_out)
        
        #update the transactions table
        db.execute("INSERT INTO transactions(transaction_type, user_id, book_id, price, date, student) VALUES (:trans, :user, :book, :price, :date, :student)",
                    trans="SWAP IN", user=session["user_id"], book=book_in, price=0, date=date.today(), student=student)
        db.execute("INSERT INTO transactions(transaction_type, user_id, book_id, price, date, student) VALUES (:trans, :user, :book, :price, :date, :student)",
                    trans="SWAP OUT", user=session["user_id"], book=book_out, price=0, date=date.today(), student=student)                    
        flash('Swap completed')
        return redirect('/')


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Get stock quote."""
    if request.method == "GET":
        # Display form for user to enter stock to search
        return render_template("add.html")
    else:
        print("HERE")
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        level = request.form.get("level")
        edition = request.form.get("edition")
        price_new = float(request.form.get("price_new"))
        price_used = float(request.form.get("price_used"))
        stock_new = request.form.get("stock_new")
        stock_used = request.form.get("stock_used")
        db.execute("INSERT INTO books(isbn, title, level, edition, stock_new, stock_used, price_new, price_used) VALUES(:isbn, :title, :level, :edition, :stock_new, :stock_used, :price_new, :price_used)",
                    isbn = isbn, title=title, level=level, edition=edition, stock_new=stock_new, stock_used=stock_used, price_new=price_new, price_used = price_used)          
        flash("Title added")  
        return redirect("/")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
