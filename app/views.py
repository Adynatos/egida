from flask import render_template
from models import Post
from app import app

@app.route('/')
def index():
    return render_template('starter-template.html')

@app.route('/posts/')
def posts():
    posts = Post.query.all()
    return render_template('posts.html', title = 'Posts', posts = posts)
