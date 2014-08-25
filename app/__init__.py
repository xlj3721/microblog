from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__) # creates a flask web application
app.config.from_object('config') # tells flask to configure app with config.py

db = SQLAlchemy(app)	# creates an SQLAlchemy instance of app for a database


import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

lm = LoginManager() # creates an object that lets app and Flask_Login work together
lm.init_app(app) # configures the Flask_Login application object to app
lm.login_view = 'login' # informs lm what the login view is needed for 

oid = OpenID(app, os.path.join(basedir,'tmp')) 
# creates an openid object with tmp folder for OpenID to store files

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

from app import views, models
# tells flask to import views.py and models.py from app the folder
# the order is important: this needs to be at the end
# import everything above the app folder first and call them and then import app