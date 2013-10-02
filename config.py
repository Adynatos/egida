import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(basedir, 'app.db')
