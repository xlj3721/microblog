from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from app import views, models
# tells flask to import views.py and models.py from app the folder

import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

app = Flask(__name__) # creates a flask web application
app.config.from_object('config') # tells flask to configure app with config.py

db = SQLAlchemy(app)	# creates an SQLAlchemy instance of app for a database

lm = LoginManager() # creates an object that lets app and Flask_Login work together
lm.init_app(app) # configures the Flask_Login application object to app
lm.login_view = 'login' # informs lm what the login view is 

oid = OpenID(app, os.path.join(basedir,'tmp')) # tmp folder for OpenID to store files
