from datetime import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid # import the object app, db, lm, oid from __init__.py
from forms import LoginForm, EditForm
from models import User, ROLE_USER, ROLE_ADMIN


@app.before_request
# any function decorated with before_request runs before the view function for every request

def before_request():
	# g is a global setup by Flask, current_user is a global setup by Flask_Login
	# g global is a place to store/share data during the life of a request
    g.user = current_user
	# gives better access; all requests can access the logged in user even inside templates
	# a global within Flask_login just got made into a global within Flask the entire app

    if g.user.is_authenticated():
    # each time browser makes a request the time in the database will be updated
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required # ensures page will only be seen by logged in users

def index():
    user = g.user
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


@lm.user_loader

def load_user(id):
    # loads a user from the database, to be used by Flask-Login, converting Flask_login
    # unicode string to integer is necessary
    return User.query.get(int(id)) 


@app.route('/login', methods = ['GET', 'POST']) 
# methods tells Flask that this view function accepts GET and POST requests
# default is just GET
@oid.loginhandler
# tells Flask-OpenID that this is our login view function

def login():

    if g.user is not None and g.user.is_authenticated():
        # if g.user is already set as an authenticated user, no need to login again
        return redirect(url_for('index')) # url_for function lets flask generate the url
         

    form = LoginForm() # the class LoginForm() imported from forms.py
    
    if form.validate_on_submit():
    # checks if it is a post request and whether it is valid
        session['remember_me'] = form.remember_me.data
        # once data is stored in flask.session it will be available during that request
        # and any future requests made by the same client 
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
        # openid function triggers authentication, takes 2 arguments; openid and list of data

    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])


@oid.after_login

def after_login(resp):
	# resp contains information returned by the OpenID provider

	if resp.email is None or resp.email == "":
	# checking for email otherwise cannot log the user in
		flash("Invalid login. Please try again.")
		return redirect(url_for('login'))

	user = User.query.filter_by(email = resp.email).first()
	# searches the db for the provided email

	if user is None:
    # if nothing found, new user is added
        nickname = resp.nickname

        if nickname is None or nickname == "":
        # if the new user doesn't have nickname, one is pulled from their email address
            nickname = resp.email.split('@')[0] # name@email.com becomes ['name', 'email.com']
        
        nickname = User.make_unique_nickname(nickname) 
        # calls a User method to make a unique name if nickname is not already unique
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
    	# added into the db through User() imported from models.py 
    	db.session.add(user)
    	db.session.commit()

	remember_me = False
	# sets the LoginForm().remember_me

	if 'remember_me' in session:
		# if there is a remember_me key in session dict, it resets LoginForm().remember_me and then pops it
		remember_me = session['remember_me']
		session.pop('remember_me', None)

	login_user(user, remember = remember_me)
	# Flask-Login function to register a valid login
	return redirect(request.args.get('next') or url_for('index'))
	# redirect back to the view which sent the user to the login view or to the index view 


@app.route('/logout')

def logout():
	logout_user()
	# Flask_Login function to logout; that's all
	return redirect(url_for('index'))


@app.route('/user/<nickname>') # takes an argument nickname, and is passed to the user function
@login_required

def user(nickname):
    # looks for the user in database and if not found,; redirects
    user = User.query.filter_by(nickname = nickname).first()

    if user == None: 
        flash('User' + nickname + ' not found.')
        return redirect(url_for('index'))

    posts = [   # fake posts but correct user
        { 'author': user, 'body': "Test post #1"},
        { 'author': user, 'body': "Test post #2"}
    ]

    return render_template('user.html',
        user = user,
        posts = posts)


@app.route('/edit', methods = ['GET', 'POST'])
@login_required

def edit():
    form = EditForm()

    if form.validate_on_submit():
    # checks if it is a post request and whether it is valid
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me

    return render_template('edit.html',
        form = form)


@app.errorhandler(404)

def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)

def internal_error(error):
    db.session.rollback() 
    # if the exception was triggered by a database error, the database session will arrive
    # in an invalid state, so need to roll it back in case a working session is needed to 
    # render the template below
    return render_template('500.html'), 500