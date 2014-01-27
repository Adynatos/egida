"""
Configuration file

A collection of constans which define application settings:

DATABASE - location of database file.
DEBUG - debug mode
CSRF_ENABLED - cross site request forgery protection
SECRET_KEY - used to create cryptographic token, that is used to validate a
form.
SQLALCHEMY_DATABASE_URI - path to the database file
WHOOSH_BASE - path to
MAX_SEARCH_RESULTS - maximum number of viewed search results
OPENID_PROVIDERS - list of OpenID providers which can be used to log in
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'tmp/flaskr.db'
DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
                          + os.path.join(basedir, 'app.db')
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
