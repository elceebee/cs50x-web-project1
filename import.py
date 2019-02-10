# This programme imports the CSV file to my database

import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():

    # Open csv file
    f = open("/Users/lori.bailey/Code/elceebee/project1/books.csv")
    reader = csv.reader(f)
    
    # Skips first line, header
    next(reader)

    # Adds the rest of the lines into the database
    for isbn, title, author, year in reader:
        book = Books(isbn=isbn, title=title, author=author, year=int(year))
        db.session.add(book)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()