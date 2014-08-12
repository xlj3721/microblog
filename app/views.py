from flask import render_template, flash, redirect
from app import app
from forms import LoginForm

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

def login():
    form = LoginForm() # the class LoginForm() imported from forms.py
    
    if form.validate_on_submit():
        # validate_on_submit function will be False if form is empty, if form is filled
        # and valid (True) Flask will gather the data, invalid fill (False)
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' +
        str(form.remember_me.data))
        # flash function is a quick way to show a message
        return redirect('/index')
        
    return render_template('login.html',
        title = 'Sign In',
        form = form)
