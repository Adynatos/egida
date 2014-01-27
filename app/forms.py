"""
Web Forms

A collection of web forms used in html files.
"""


from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required
#from wtforms.ext.appengine.db import model_form
#from models import Post


class LoginForm(Form):
    """
    A form that handles the OpenID string and remember me boolean field.
    """
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class PostForm(Form):
    """
    A form that handles the creation of new post - captures title, body and tag
    strings.
    """
    title = TextField('title', validators=[Required()])
    body = TextField('post', validators=[Required()])
    tags = TextField('tags', validators=[Required()])


class CommentForm(Form):
    """
    A form that handles the creation of new comment - captures the comment's
    body string.
    """
    body = TextField('comment', validators=[Required()])


class SearchingForm(Form):
    """
    A form that handles the new search query - captures the search string.
    """
    search = TextField('search', validators=[Required()])
