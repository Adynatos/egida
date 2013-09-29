from app import db

ROLE_USER=0
ROLE_ADMIN=1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, \
            unique=True)
    email = db.Column(db.String(120), index=True, \
            unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    
    posts = db.relationship('Post', backref='author', \
            lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.nickname


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    posts = db.relationship('Post', backref='category', \
            lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, \
            db.ForeignKey('category.id'))

    def __repr__(self):
        return '<Post %r>' % self.title