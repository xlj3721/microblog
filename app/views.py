from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid # import the object app from __init__.py
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN

@app.route('/')
@app.route('/index')

def index():
    user = {'nickname': 'Miguel'} # fake user
    posts = [ # fake list of posts
        {
            'author': {'nickname':'John'},
            'body': "Beautiful day in Portland!"
        },
        {
            'author': {'nickname':'Susan'},
            'body': "The Avengers movie was so cool!"
        },
        {   
            'author': {'nickname':'Kate'},
            'body': "Kate from base, how can I help?"
        }
    ]
    
    return render_template('index.html',
        title = 'Home',
        user = user,
        posts = posts)


@app.route('/login/', methods = ['GET', 'POST']) 
# methods tells Flask that this view function accepts GET and POST requests
# default is just GET
@oid.loginhandler
# tells Flask-OpenID that this is our login view function

def login():

    if g.user is not None and g.user.is_authenticated():
        # if g.user is already set as an authenticated user, no need to login again
        # g global is a setup by flask as a place to store/share data during the 
        # life of a request
        return redirect(url_for('index')) # url_for function lets flask generate the url
         

    form = LoginForm() # the class LoginForm() imported from forms.py
    
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        # once data is stored in flask.session it will be available during the that request
        # and any future requests made by the same client 
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
        # openid function triggers authentication, takes 2 arguments; openid and list of data

    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    # loads a user from the database, conversion from Flask_login unicode string to 
    # integer is necessary
    return User.query.get(int(id)) 
    
