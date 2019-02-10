# This programme describes the tables used in the databse. 
# The file create.py creates will create the tables.
# The file import.py will import the book data from a csv file provided


import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)


class Users(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True)
    passhash = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)


class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    book_ID = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_ID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reviewText = db.Column(db.String, nullable=True)
    reviewStar = db.Column(db.Integer, nullable=False)
