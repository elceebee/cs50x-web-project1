import os
import requests

from flask import Flask, flash, jsonify, redirect, render_template, request, session, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helperfunctions import login_required
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
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


@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # User completed register form
    if request.method == "POST":

        # Ensures username and password submitted
        if not request.form.get("username") or not request.form.get("password"):
            apology = "nouserpass"
            return render_template("register.html", APOLOGY = apology)
        
        # Checks password was confirmed and they are the same
        if request.form.get("password") != request.form.get("confirmpassword"):
            apology = "noconfirm"
            return render_template("register.html", APOLOGY = apology)

        # Checks username does not already exist
        check = db.execute("SELECT * FROM users WHERE username = :username", {"username": request.form.get("username")}).first()
        if check == None:
        
            # Store user information in database
            user = db.execute(
                "INSERT INTO users (passhash, username) VALUES (:passhash, :username) RETURNING id",
                {"passhash": generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8), 
                    "username": request.form.get("username")})
            db.commit()
            
            # Log user in
            row = user.first()
            session["userID"] = row["id"]
            reader = session["userID"]

            return render_template("search.html", READER=reader)
            
        else:
            apology = "inuse"
            return render_template("register.html", APOLOGY = apology)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget current user id
    session.clear()

    # User submitted login form
    if request.method == "POST":

        # Ensure username and password both submitted
        if not request.form.get("username"):
            apology = "nousername"
            return render_template("login.html", APOLOGY = apology)

        elif not request.form.get("password"):
            apology = "nopassword"
            return render_template("login.html", APOLOGY = apology)
        
        # Query database for username
        usernameRow = db.execute("SELECT * FROM users WHERE username = :username", 
            {"username": request.form.get("username")}).first()

        # Checks username exists
        if usernameRow == None:
            apology = "nosuch"
            return render_template("login.html", APOLOGY = apology)

        # Check password
        if not check_password_hash(usernameRow["passhash"], request.form.get("password")):
            apology = "nosuch"
            return render_template("login.html", APOLOGY = apology)

        # Remember which user has logged in, used throughout session
        session["userID"] = usernameRow["id"]

        # Redirect user to home page
        return redirect("/search")
    
    # User reached route via GET
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/search", methods = ["GET", "POST"])
@login_required
def search():

    # User submits text in the search box, by POST
    if request.method == "POST":
        searchterm = request.form.get("search").lower()

        # First look for the full string in the database
        firstResults = db.execute("SELECT * FROM books WHERE LOWER(isbn) = :search OR LOWER(title) = :search OR LOWER(author) = :search",
        {"search": searchterm}).fetchall()
        
        # Execute more detailed search if the full string is not found
        if len(firstResults) == 0:

            secondResults = db.execute("SELECT * FROM books WHERE LOWER(isbn) like :newsearch OR LOWER(title) like :newsearch OR LOWER(author) like :newsearch",
            {"newsearch": "%" + searchterm + "%"}).fetchall()

            # Apologise if no results
            if len(secondResults) == 0:
                apology = "noresults"
                return render_template("results.html", 
                    SEARCHTERM = searchterm,
                    APOLOGY = apology)

            # Store not-exact results
            else:
                whichone = "second"
                results = secondResults
                return render_template("results.html", 
                    RESULTS = results, 
                    WHICHONE = whichone,
                    SEARCHTERM = searchterm)
        
        # Store exact results
        else: 
            whichone = "first"
            results = firstResults
            return render_template("results.html", 
                RESULTS = results, 
                WHICHONE = whichone, 
                SEARCH = searchterm)

    # User reaches page by GET method
    else:
        return render_template("search.html")


@app.route("/reviews", methods=["GET", "POST"])
@login_required
def reviews():

    # User submits review form from reviews.html
    if request.method == "POST":
        # Add review to data base
        new_review = db.execute(
                "INSERT INTO reviews (book_id, user_id, review_text, review_star) VALUES (:book_id, :user_id, :review_text, :review_star) RETURNING review_text, review_star",
                {"book_id": request.form.get("bookid"),
                "user_id": session["userID"],
                "review_text": request.form.get("reviewtext"),
                "review_star": request.form.get("reviewstar")})
        db.commit()
        return redirect("/thanks")

    # Users have reached the reviews page via results page
    else:
        # Stores id, isbn or title for works found via the search page
        # Redirects to search if no id, isbn or title found 
        bookid = request.args.get("bookid")
        bookisbn = request.args.get("bookisbn")
        booktitle = request.args.get("booktitle")
        bookauthor = request.args.get("bookauthor")
        bookyear = request.args.get("bookyear")
        if bookid == None or bookisbn == None or booktitle == None:
            return redirect("/search")            

        # Retreives reviews from our database
        bookReviews = db.execute("SELECT user_id, review_text, review_star FROM reviews WHERE book_id = :book_id",
        {"book_id": bookid}).fetchall()
        
        # Assume that the user has not already reviewed the book
        reviewed = False
        
        if len(bookReviews) == 0:
            reviews = "Nothing"

        else:
            reviews = []

            for row in bookReviews:
                
                # Check the user hasn't reviewed the book
                if row[0] == session["userID"]:
                    reviewed = True
                
                # Appends review text and star rating to list
                reviews.append([row[1], row[2]])

        # Retreives average star rating and number of reviews from Goodreads
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
        params={"key": "TqaelOhF8LNELjeFCcOkQ", "isbns": bookisbn})

        if res.status_code == (404 or 422) :
            goodreadsError = "yes";
        else:
            goodreadsError = "no";
            data = res.json()
            ratings_count = data["books"][0]["work_ratings_count"]
            ave_count = data["books"][0]["average_rating"]
        return render_template("reviews.html",
            BOOKID = bookid,
            ISBN = bookisbn,
            TITLE = booktitle,
            AUTHOR = bookauthor,
            YEAR = bookyear,
            GOODREADSERR = goodreadsError,
            REVIEWED = reviewed,
            REVIEWS = reviews,
            RATINGS_COUNT = ratings_count,
            AVE_COUNT = ave_count)

@app.route("/thanks", methods=["GET"])
@login_required
def thanks():
    return render_template("thanks.html")


@app.route("/api/<string:isbn>", methods=["GET"])
def review_book_info(isbn):
    # Retrieve Book information
    bookinfo = db.execute("SELECT id, title, author, year, isbn FROM books WHERE isbn = :isbn",
        {"isbn": isbn}).fetchone()
    
    if bookinfo == None:
        abort(404)

    reviewinfo = db.execute("SELECT avg(review_star) AS average_score, count(review_star) AS review_count FROM reviews WHERE book_id=:book_id GROUP BY book_id",
        {"book_id": bookinfo.id}).fetchone()

    return jsonify({"title": bookinfo.title, 
        "author":bookinfo.author, 
        "year": bookinfo.year,
        "isbn": bookinfo.isbn, 
        "review_count": reviewinfo.review_count, 
        "average_score": float(reviewinfo.average_score)})
