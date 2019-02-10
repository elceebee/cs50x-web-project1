# Functions references in application.py

from functools import wraps
from flask import g, request, redirect, url_for, Flask, session
from flask_session import Session

# Login required function referred to in CS50, 
# And found here: http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userID") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

