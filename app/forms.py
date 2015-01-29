"""
Web Forms

A collection of web forms used in html files.
"""


from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import *
#from models import Post

class RoomForm(Form):
    number = TextField('Title')
    floor = TextField('Floor')
    room_type = TextField('Room type')
    price_per_day = TextField('Price per day')
    room_state = TextField('Room state')

class OrderForm(Form):
    room = TextField("Room")
    client = TextField("Client")
    cost = TextField("Cost")
    is_paid = BooleanField("Is paid?")

class ClientForm(Form):
    name = TextField("Name")
    surname = TextField("Surname")
    phone = TextField("Phone")
    email = TextField("email")
    sex = TextField("Sex")
    age = TextField("Age")
    role= TextField("Role")

class EmployeeForm(Form):
    name = TextField("Name")
    surname = TextField("Surname")
    phone = TextField("Phone")
    email = TextField("email")
    sex = TextField("Sex")
    age = TextField("Age")
    role = TextField("Role")
    salary = TextField("Salary")

class RoleForm(Form):
    name = TextField("Name")
    job_grade = TextField("Job Grade")

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
