import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from controller import format_date, format_score, format_vscore, login_required, lookup


# Configure application
app = Flask(__name__)

# Set a mandatory secret key for the application (session use)
app.secret_key = b'Nk(*jsdh@#y%-a!,.<]{'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure a connection and create a Cursor object to call its execute() method
db = SQL("sqlite:///winexp.db", connect_args={'check_same_thread': False}, echo=True)

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():

    return redirect("/search")


# Login 
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":
        
        # Ensure email was submitted
        if not request.form.get("email"):
            flash("Please enter email")
            return render_template("login.html")

        # Ensure password was submitted
        if not request.form.get("password"):
            flash("Please enter password")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """
    
    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":
        
        # Ensure email was submitted
        if not request.form.get("email"):
            flash("Please enter email")
            return render_template("register.html")
        
        # Query database for username to ensure username does NOT exist
        email = request.form.get("email") 
        rows = db.execute("SELECT * FROM users WHERE email = :email", email=email)
        print(email)
        print(rows)
        
        if len(rows) != 0:
            flash('Username not available')
            return render_template("register.html")
           
        # Ensure password was submitted
        if not request.form.get("password"):
            flash("Please enter password")
            return render_template("register.html")

        # Ensure password and confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            flash(f"Passwords do not match.")
            return render_template("register.html")

        # Set password hash values into hash
        hash = generate_password_hash(request.form.get("password"))

        # Run query to insert in users the values for username and password hash
        db.execute("INSERT INTO users (email, hash) VALUES (:email, :hash)", email=email, hash=hash)

        # Remember which user has logged in
        user_id = db.execute("SELECT id FROM users WHERE email = :email", email=email)
        session["user_id"] = user_id[0]["id"]

        # Redirect user to home page
        flash('Registered!')
        return redirect("/")        

    # User reached route via GET 
    else:
        return render_template("register.html")


# Search Wine and Vintage
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():

    # User reaches route via POST
    if request.method == "POST":
        
        wine = request.form.get("wine")

        vintage = request.form.get("vintage")
        print(f"*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!!*!*!*!*!*!*!*!*!*!*!*!*!**!** {wine}, {vintage}")
        
        rows, winevint = lookup(wine, vintage)
       
        # Ensure if a valid date was returned
        date = ""       
        
        if rows:
            date_month = winevint['date'][5:7]
            date_year = winevint['date'][0:4]
            date = format_date(date_month, date_year)

            # Run a query to store search data into winesearches table
            db.execute("INSERT INTO winesearches (user_id, wine, region, vintage, score, confidence_index, journalist_count, datetime) \
                        VALUES (:user_id, :wine, :region, :vintage, :score, :confidence_index, :journalist_count, datetime('now'))" \
                        , user_id=session["user_id"], wine=winevint['wine'], region=winevint['regions'], vintage=winevint['vintage'], score=winevint['score'], confidence_index=winevint['confidence_index'], journalist_count=winevint['journalist_count'])
        
        return render_template("searched.html", rows=rows, winevint=winevint, date=date)

    if request.method == "GET":  
        return render_template("search.html")


# Display active user search log 
@app.route("/searchlog", methods=["GET", "POST"])
@login_required
def searchlog():
    """ Dispalys wine search history"""
    
    # User reached via GET
    if request.method == "GET":
    
        rows = db.execute("SELECT * FROM winesearches WHERE user_id = :user_id ORDER BY datetime DESC LIMIT 25", user_id=session["user_id"])

        if not rows:
            return redirect("/search")

    return render_template("searchlog.html", rows=rows)


@app.route("/vintages", methods=["GET", "POST"])
@login_required
def vintages():
    region = None
    scores = []
    # User reached route via POST
    if request.method == "POST":     
        region = request.form.get("region")
        
        # Render template for countries with multi regions when a region is selected 
        if region != None:
            rows = db.execute("SELECT country, region, vintage, score, status FROM vintages WHERE region = :region", region=region)
            country = rows[0]['country']

            for i in range(len(rows)):
                score = rows[i]['score']
                scores.append(format_vscore(score))
                
            for i in range(len(rows)):
                rows[i]['score'] = scores[i]

            return render_template("vintagedsingle.html", rows=rows, country=country, region=region)
       
        else:
            country = request.form.get("country")

            # Query for distinct regions in selected country
            rows = db.execute("SELECT DISTINCT region FROM vintages WHERE country = :country", country=country)  
            region = rows[0]['region']

        # Render template for countries with only one region
        if len(rows) == 1:
            rows = db.execute("SELECT country, region, vintage, score, status FROM vintages WHERE country = :country", country=country)
      
            for i in range(len(rows)):
                score = rows[i]['score']
                scores.append(format_vscore(score))
                
            for i in range(len(rows)):
                rows[i]['score'] = scores[i]

            return render_template("vintagedsingle.html", rows=rows, country=country, region=region)

        # Render template for countries multi regions
        else:
            
            return render_template(f"vintagedmulti.html", rows=rows, country=country)      

    # User reached via GET
    else:
        return render_template("vintages.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("apology.html", e_name=e.name, e_code=e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
