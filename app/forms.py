from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import DataRequired, Length # used to be Required but is deprecated, now called DataRequired

class LoginForm(Form):
    openid = TextField('openid', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)

class EditForm(Form):
    nickname = TextField('nickname', validators = [DataRequired()])
    about_me = TextField('about_me', validators = [Length(min= 0, max = 140)])

    def __init__(self, original_nickname, *args, **kwargs):
        # the form takes the argument original_nickname
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        # first checks if nickname is changed or not
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        # then checks if the changed nickname is already taken or not
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append("This nickname is already in use. Please choose another one.")
            return False
        return True

