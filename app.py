
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime

import json
import ast

from scraper import amazon_scraper, lazada_scraper, shopee_scraper

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """"""
    return apology("TODO")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
    return apology("TODO")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
         # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("please repeat password", 400)

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password != confirmation:
            return apology("passwords not the same", 400)

        if len(db.execute("SELECT * FROM users WHERE username = ?", username)) != 0:
            return apology("username exists", 400)

        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username,hash) VALUES (?,?)", username, password_hash)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    return render_template("register.html")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        if not request.form.get("cur_password"):
            return apology("must provide current password", 400)
        actual_cur_hash = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])[0]["hash"]

        if not check_password_hash(actual_cur_hash, request.form.get("cur_password")):
            return apology("Current Password incorrect", 400)
        if not request.form.get("password"):
            return apology("must provide password", 400)
        if not request.form.get("confirmation"):
            return apology("please repeat password", 400)
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("passwords not the same", 400)
        password_hash = generate_password_hash(password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", password_hash, session["user_id"])
        return apology("Password Changed Successfully")


    return render_template("change_password.html")


@app.route("/wishlist", methods=["GET", "POST"])
@login_required
def wishlist():
    if request.method == "GET":
        return render_template("wishlist.html")
    else:
        if request.form.get("product"):
            product = request.form.get("product").lower().strip()
            # shopee_scraper = [{"name": " Razer DeathAdder Essential 6400DPI", "price": "$22.50", "location": "China", "url": "https://shopee.sg/Original-Razer-Mouse-DeathAdder-Essential-Essential-Gaming-For-PC-Laptop-Computer-Black-White--i.520130789.15306817355?sp_atk=96a4467b-db61-467e-b46a-49a4644ac18c&xptdk=96a4467b-db61-467e-b46a-49a4644ac18c"}]
            #lazada_scraper = [{"name": "airpods pro 2", "price": "358", "location": "Singapore", "url": "https://lazada.sg/search?=airpods pro 2"}]
            #amazon_scraper = [{"name": "airpods pro 2", "price": "358", "location": "Singapore", "url": "https://amazon.sg/search?=airpods pro 2"}]
            shopee_response = shopee_scraper(product)
            lazada_response = lazada_scraper(product)
            amazon_response = amazon_scraper(product)
            responses = [shopee_response, lazada_response, amazon_response]
            if shopee_response and lazada_response and amazon_response:
                return render_template("wishlist-confirm.html", shopee_response=shopee_response, lazada_response=lazada_response, amazon_response=amazon_response
                                       ,search=product)
            else:
                print(lazada_response)
                print(amazon_response)
                return apology("response error")

        elif request.form.get("submit-confirm"):
            search = request.form.get("search")
            shopee_response = ast.literal_eval(request.form.get('shopee_response'))
            lazada_response = ast.literal_eval(request.form.get("lazada_response"))
            amazon_response = ast.literal_eval(request.form.get("amazon_response"))
            responses = [shopee_response, lazada_response, amazon_response]
            wishlist = db.execute("SELECT * FROM wishlist ORDER BY item_id DESC")
            if len(wishlist) == 0:
                item_id = 0
            else:
                item_id = wishlist[0]["item_id"] + 1


            for response in responses:
                for item in response:
                    if request.form.get(f"{item['url']}"):
                        if response == shopee_response:
                            platform = "Shopee"
                        elif response == lazada_response:
                            platform = "Lazada"
                        elif response == amazon_response:
                            platform = "Amazon"
                        else:
                            return apology("response error")

                        db.execute("INSERT INTO wishlist (item_id, user_id, search, platform, url) VALUES (?,?,?,?,?)", item_id, session["user_id"], search, platform, item['url'])

            return apology("Wishlist successfully added")
        else:
            return apology("Error in entering wishlist")

@app.route("/check", methods=["GET", "POST"])
@login_required
def check():
    if request.method == "GET":
        data = db.execute("SELECT * FROM query WHERE user_id = ? ORDER BY item_id", session["user_id"])
        count = 0
        query = []
        #sort by item_id(wishlist_id)
        for i, row in enumerate(data):
            if i==0:
                query.append([row])
            else:
                if row["item_id"] == data[i-1]["item_id"]:
                    query[count].append(row)
                else:
                    count += 1
                    query.append([row])
        count = 0
        rows = []

#To specify the number of items per row
        for i, item in enumerate(query):
            if i == 0:
                rows.append([item])
            else:
                if i % 1 == 0:
                    count += 1
                    rows.append([item])
                else:
                    rows[count].append(item)

        return render_template("check.html", rows=rows)


@app.route("/refresh", methods=["GET", "POST"])
@login_required
def refresh():
    if request.method == "GET":
        return render_template("refresh.html")
    if request.method == "POST":
        # for testing purposes without the scraper function
        # db.execute("INSERT INTO query (item_id, user_id, search, platform, name, price, location, url, datetime) VALUES (?,?,?,?,?,?,?,?,?)"
        #            , 2, session["user_id"], "airpods pro", "lazada", "apple airpods pro", 198.00, "Singapore", "lazada.com/airpod", datetime.now())
        # db.execute("INSERT INTO query (item_id, user_id, search, platform, name, price, location, url, datetime) VALUES (?,?,?,?,?,?,?,?,?)"
        #            , 2, session["user_id"], "airpods pro", "shopee", "apple airpods pro", 198.00, "Singapore", "shopee.com/airpod", datetime.now())
        # db.execute("INSERT INTO query (item_id, user_id, search, platform, name, price, location, url, datetime) VALUES (?,?,?,?,?,?,?,?,?)"
        #            , 2, session["user_id"], "airpods pro", "amazon", "apple airpods pro", 198.00, "Singapore", "amazon.com/airpod", datetime.now())

        #for testing with the scraper
        shopee_scraper = [{"name": "airpods pro 2", "price": "358", "location": "Singapore", "url": "https://shopee.sg/search?=airpods pro 2"}]
        wishlist_rows = db.execute("SELECT * FROM wishlist WHERE user_id = ? ", session["user_id"])
        #wishlist_rows = [{"user_id":session["user_id"], "search": "airpods 2", "platform":"shopee", "url":"https://shopee.sg/search?=airpods pro 2", "item_id":4}]
        for row in wishlist_rows:
            if row["platform"] == "Shopee":
                responses= shopee_scraper
            elif row["platform"] == "Lazada":
                print(row["search"])
                responses = lazada_scraper(row["search"])
            elif row["platform"] == "Amazon":
                responses = amazon_scraper(row["search"])
            print(responses)
            # responses = [{"name": "airpods pro 2", "price": "358", "location": "Singapore", "url": "https://shopee.sg/search?=airpods pro 2"}]

            for response in responses:
                if row["url"] == response["url"]:
                    name = response["name"]
                    price = response["price"]
                    location = response["location"]
            if price and name and location:
                db.execute("INSERT INTO query (item_id, user_id, search, platform, name, price, location, url, datetime) VALUES (?,?,?,?,?,?,?,?,?)",
                           row["item_id"], session["user_id"], row["search"], row["platform"], name, price, location, row["url"], datetime.now())
            else:
                return apology("error in wishlist")


        return redirect("/check")








