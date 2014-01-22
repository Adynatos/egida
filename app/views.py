from flask import render_template, url_for, redirect, session, g, request, flash
from models import Post, User, Comment, ROLE_USER, ROLE_ADMIN
from app import lm, app, db, oid
from forms import LoginForm, PostForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    return render_template('index.html', user=user)


@app.route('/new_post', methods=['GET', 'POST'])
#@login_required
def new_post():
    # for testing purposes only
    g.user.role = 1

    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data,
                    pub_date=datetime.utcnow(), user_id=g.user.id)
        db.session.add(post)
        db.session.commit()
        flash('You have succesfuly added your post.')
        return redirect(url_for('index'))

    return render_template('new_post.html', form=form, user=g.user)


@app.route('/posts/')
#@login_required
def posts():
    posts = Post.query.order_by(Post.pub_date.desc())
    return render_template('posts.html', posts=posts, user=g.user)


@app.route('/posts/<post_id>')
@login_required
def view_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    comments = Comment.query.filter_by(post_id=post_id)
    return render_template('view_post.html', post=post, comments=comments)
    #return


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', title='Sign In', form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))
