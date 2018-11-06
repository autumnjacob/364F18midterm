import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


app = Flask(__name__)

app.config["DEBUG"] = True

app.config["CLIENT_ID"] = "s94u9AuOCALRJYkYAGe6iw"
app.config["API_KEY"] = "r3nrcxAhG2pdUaxTqmLTr1ZEAgZBzBSA02qktk0AHgH5vwEjEFhBiFcmfZVVSkvb\
b-7zqBKR48yrGmc3Ds3sQOI7eJJviuHB9wKbwpyZb_MyhFMPGtBEw0RZ0FrfW3Yx"


app.config['SECRET_KEY'] = 'secretstring364midterm'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://AutumnJacob@localhost/jacobau364midterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from modules import views
from modules import models
from modules import forms
