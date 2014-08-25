CSRF_ENABLED = True # prevents cross-site request forgery 
SECRET_KEY = 'you-will-never-guess'# creates a cryptographic token used to validate a form

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = 'altshift5372'
MAIL_PASSWORD = 'whatever7'

# administrator list
ADMINS = ['altshift5372@aol.com']



import os
basedir = os.path.abspath(os.path.dirname(__file__)) 
# dirname name gets the firstpart of the file and abspath makes it an absolute ref
# in this case /home/dcreekp/microblog

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# join function joins the parts /home/dcreekp/microblog and app.db
# all up sqlite:////home/dcreekp/microblog/app.db
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# looks like /home/dcreekp/microblog/db_repository                                   
