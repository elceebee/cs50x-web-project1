import os


from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helperfunctions import login_required
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget current user id
    session.clear()

    # User submitted login form
    if request.method == "POST":

        # Ensure username and password both submitted
        if not request.form.get("username"):
            APOLOGY = "nousername"
            return render_template("login.html", APOLOGY)

        elif not request.form.get("password"):
            APOLOGY = "nopassword"
            return render_template("login.html", APOLOGY)
        
        # Query database for username
        usernameRow = Users.query.filter_by(user="username").first()

        # Checks username exists
        if usernameRow == None:
            APOLOGY = "nosuch"
            return render_template("login.html", APOLOGY)

        # Check password
        if not check_password_hash(usernameRow[0]["passhash"], request.form.get("password")):
            APOLOGY = "nosuch"
            return ("login.html", APOLOGY)

        # Remember which user has logged in, used throughout session
        user_id = usernameRow[0]["id"]
        session["user_id"]

        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET
    else:
        return render_template("login.html", APOLOGY)


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # User completed register form
    if request.method == "POST":

        # Ensures username and password submitted
        if not request.form.get("username") or not request.form.get("password"):
            APOLOGY = "nouserpass"
            return render_template("register.html", APOLOGY)
        
        # Checks password was confirmed and they are the same
        if request.form.get("password") != request.form.get("confirmpassword"):
            APOLOGY = "noconfirm"
            return render_template("register.html", APOLOGY)

        # Checks username does not already exist
        if not Users.query.filter_by(user="username").first():
            APOLOGY = "inuse"
            return render_template("register.html", APOLOGY)

        # Store user information in database
        user = User(passhash = generate_password_hash(request.form.get("password"),
                method='pbkdf2:sha256',
                salt_length=8), 
                username = request.form.get(username))
        db.session.commit()
        å
        # Redirect user to login form
        return redirect("/login")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
