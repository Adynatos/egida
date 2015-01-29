"""
Models

Collection of classes that represents the SQL tables structure.
"""

from app import db
from app import app
import flask.ext.whooshalchemy as whooshalchemy


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    room_type = db.relationship("Room_type", backref="rooms")
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'))
    price_per_day = db.Column(db.Integer)
    room_state = db.relationship("Room_state", backref="rooms")
    room_state_id = db.Column(db.Integer, db.ForeignKey('room_state.id'))

    @property
    def r_type(self):
        return self.room_type.r_type

    @property
    def r_state(self):
        return self.room_state.state_name

class Room_state(db.Model):
    __tablename__ = 'room_state'
    id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(120))

class Room_type(db.Model):
    __tablename__ = 'room_type'
    id = db.Column(db.Integer, primary_key=True)
    r_type = db.Column(db.SmallInteger)

class Room_rental(db.Model):
    __tablename__ = 'room_rental'
    id = db.Column(db.Integer, primary_key=True)
    room = db.relationship("Room", backref="rentals")
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    client = db.relationship("Client", backref="rented")
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    ordered_features = db.relationship("Ordered_features", backref="rentals")
    ordered_features_id = db.Column(db.Integer, db.ForeignKey('ordered_features.id'))
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)

class Extra_features(db.Model):
    __tablename__ = 'extra_features'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    price = db.Column(db.Integer)

association_table = db.Table('order__features_asso',
            db.Column('ordered_id', db.Integer, db.ForeignKey('ordered_features.id')),
            db.Column('feature_id', db.Integer, db.ForeignKey('extra_features.id'))
                )

class Ordered_features(db.Model):
    __tablename__ = 'ordered_features'
    id = db.Column(db.Integer, primary_key=True)
    features = db.relationship("Extra_features", 
            secondary=association_table,
            backref="ordered")

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    room_rental = db.relationship("Room_rental", backref="orders")
    room_rental_id = db.Column(db.Integer, db.ForeignKey('room_rental.id'))
    client = db.relationship("Client", backref="orders")
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    cost = db.Column(db.Integer)
    is_paid = db.Column(db.Boolean)

    @property
    def client_name(self):
        return self.client.surname

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    surname = db.Column(db.String(60))
    phone = db.Column(db.String(60))
    email = db.Column(db.String(60))
    sex = db.relationship("Sex")
    sex_id = db.Column(db.Integer, db.ForeignKey("sex.id"))
    age = db.Column(db.SmallInteger)
    is_married = db.Column(db.Boolean)

    @property
    def sex_name(self):
        return self.sex.name

class Sex(db.Model):
    __tablename__ = 'sex'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    surname = db.Column(db.String(60))
    phone = db.Column(db.String(60))
    email = db.Column(db.String(60))
    sex = db.relationship("Sex")
    sex_id = db.Column(db.Integer, db.ForeignKey("sex.id"))
    age = db.Column(db.SmallInteger)
    role = db.relationship("Role")
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    salary = db.Column(db.Integer)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    job_grade = db.Column(db.SmallInteger)

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    """
    Model that represents user.

    Functions is_authenticated, is_active, is_anonymous and get_id are used by
    OpenID.
    """
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # next 4 functions are needed by OpenID
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.nickname


class Category(db.Model):
    """
    Model that represents Category.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name


class Comment(db.Model):
    """
    Model that represents comment.
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user = db.relationship('User',
                           backref=db.backref('comments', lazy='dynamic'))

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                )


class Tag(db.Model):
    """
    Model that represents tag.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Post(db.Model):
    """
    Model that represents post.
    """
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('posts', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.title

whooshalchemy.whoosh_index(app, Post)
