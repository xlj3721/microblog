from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid # import the object app, db, lm, oid from __init__.py
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

@lm.user_loader
def load_user(id):
    # loads a user from the database, to be used by Flask-Login, converting Flask_login
    # unicode string to integer is necessary
    return User.query.get(int(id)) 

@app.before_request
# any function decorated with before_request runs before the view function for every request
def before_request():
	# g is a global setup by Flask, current_user isa global setup by Flask_Login
	# g global is a place to store/share data during the life of a request
	g.user = current_user
	# gives better access; all requests can access the logged in user even inside templates
	# a global within Flask_login just got made into a global within Flask the entire app


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
        session['remember_me'] = form.remember_me.data
        # once data is stored in flask.session it will be available during the that request
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


