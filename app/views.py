from flask import render_template 
# this function takes a template name and a variable list of parameters and returns 
# the rendered template with all arguments in place, it invokes Jinja2 templating 
# engine under the hood
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'} # fake user
    return render_template('index.html',
        title = None,
        user = user)
