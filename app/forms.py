from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required
from wtforms.ext.appengine.db import model_form
from models import Post


class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class PostForm(Form):
    title = TextField('title', validators=[Required()])
    body = TextField('post', validators=[Required()])

#MyForm = model_form(Post, Form)
