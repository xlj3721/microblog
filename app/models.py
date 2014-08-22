from app import db
from hashlib import md5	# constructs a secure hash 

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	""" attributes for the User database """
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
			# a one-to-many relationship

	def __repr__(self):
		return "<User %r>" % (self.nickname)

	def avatar(self, size):
		# returns the url of the user's avatar image with some options
		return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

	""" methods for the Flask_login extension """

	def is_authenticated(self):
	    return True

	def is_active(self):
	    return True

	def is_anonymous(self):
	    return False

	def get_id(self):
	    return unicode(self.id)

		
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
		return "<Post %r>" % (self.body)
    
    
    
    
