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
    form = LoginForm()
    return render_template('login.html',
        title = 'Sign In',
        form = form)
