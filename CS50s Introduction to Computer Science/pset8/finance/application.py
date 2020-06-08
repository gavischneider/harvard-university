import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        stocks = db.execute("SELECT * FROM stocks WHERE user_id = :user_id", user_id=session["user_id"])
        total = 0
        for stock in stocks:
            stock["name"] = lookup(stock["symbol"])["name"]
            stock["price"] = lookup(stock["symbol"])["price"]
            stock["total"] = usd(float(stock["price"]) * int(stock["shares"]))
            total = total + (float(stock["price"]) * int(stock["shares"]))
        cash = float(db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])[0]["cash"])
        total = total + cash
        return render_template('index.html', cash=usd(cash), stocks=stocks, total=usd(total))
    else:
        # Add more money
        amount = float(request.form.get("amount"))
        cash = float(db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])[0]["cash"])

        newcash = db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash+amount, id=session["user_id"])
        if not newcash:
            apology("Something went wrong with the cash")
        return redirect("/")



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Enter a stock")
        shares = int(request.form.get("shares"))
        if not shares:
            return apology("Enter how many shared you would like")
        shares = int(shares)
        quote = lookup(symbol)
        if quote == None:
            return apology("Stock not found", 400)
        price = float(quote["price"]) * int(shares)
        cash = float(db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])[0]["cash"])

        if price > cash:
            return apology("You do not have enough money")

        ownstock = db.execute("SELECT * FROM stocks WHERE user_id = :user_id AND symbol = :symbol AND shares > 0", user_id=session["user_id"], symbol = symbol)
        if ownstock:
            updatestock = db.execute("UPDATE stocks SET shares=(shares + :shares) WHERE user_id=:user_id AND symbol=:symbol", shares=shares, user_id=session["user_id"], symbol=symbol)
        else:
            newstock = db.execute("INSERT INTO stocks (user_id, symbol, shares, operation) VALUES (:user_id, :symbol, :shares, :operation)", user_id=session["user_id"], symbol=symbol, shares=int(shares), operation='buy')


        updatecash = db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash-price, id=session["user_id"])
        return redirect("/")
    else:
        return render_template("buy.html")




@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM stocks WHERE user_id = :user_id", user_id=session["user_id"])

    # Get stocks current prices
    for transaction in transactions:
        curPrice = lookup(transaction['symbol'])
        transaction['price'] = curPrice['price'] * transaction['shares']

    return render_template('history.html', transactions=transactions)





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


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure stock name was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock name", 403)

        # Search for stock -  return a js object`
        stock = lookup(request.form.get("symbol"))

        if stock == None:
            return apology("could not find stock", 403)

        # Redirect to quoted.html
        return render_template("quoted.html", stock=stock)

    else:
        # GET method
        return render_template("quote.html")








@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password and password-confimation fields match
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords don't match", 403)

        # Check if username is already taken
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) != 0 :
            return apology("username is alreacy taken", 403)

        # Everything checks out, now hash the password before saving new user
        hashedPass = generate_password_hash(request.form.get("password"), "pbkdf2:sha256", 8)

        # Now store the new user
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hashedPass)

        # Redirect to home page
        return redirect("/")

    else:
        # GET method
        return render_template("register.html")







@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Check whether the user's input is correct
        symbol = request.form.get("symbol")
        shares = (db.execute("SELECT shares FROM stocks WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=symbol)[0]["shares"])
        sharessold = (request.form.get("shares"))
        quote = lookup(symbol)
        amount = float(quote["price"]) * int(sharessold)

        if (int(shares) - int(sharessold)) < 0:
            return apology("You do not have that many shares", 400)
        if not symbol:
            return apology("Choose a stock's symbol to sell")
        if not shares:
            return apology("Enter an amount of shares")
        if not sharessold:
            return apology("Something went wrong with the sold shares")



        if int(shares) == int(sharessold):
            newshares = db.execute("DELETE FROM stocks WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=symbol)
        else:
            newshares = db.execute("UPDATE stocks SET shares = (shares - :shares) WHERE user_id = :user_id AND symbol = :symbol", shares = sharessold, user_id=session["user_id"], symbol=symbol)
        if not newshares:
            apology('Something went wrong with the shares')
        newcash = db.execute("UPDATE users SET cash = (cash + :amount) WHERE id = :id", amount = amount, id = session["user_id"])
        if not newcash:
            apology("Something went wrong with the cash")

        return redirect("/")

    else:
        stocks = db.execute("SELECT * FROM stocks WHERE user_id = :user_id", user_id=session["user_id"])
        return render_template("sell.html", stocks=stocks)












def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
