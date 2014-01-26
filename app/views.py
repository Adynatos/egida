from flask import render_template, url_for, redirect, session, g, request, flash
from models import Post, User, Comment, Tag, ROLE_USER, ROLE_ADMIN
from app import lm, app, db, oid
from forms import LoginForm, PostForm, CommentForm, SearchingForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from config import MAX_SEARCH_RESULTS

def get_or_create_tag(tag):
    t = Tag.query.filter_by(name=tag)
    if t.count() == 0:
        t = Tag(name=tag)
        db.session.add(t)
        db.session.commit()
    else:
        t = t.first()

    return t

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    g.searching_form = SearchingForm()


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    tags = Tag.query.all()
    return render_template('index.html', user=user, tags=tags)


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():

    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, 
                pub_date=datetime.utcnow(), user_id=g.user.id)

        for tag in form.tags.data.split():
            tag = get_or_create_tag(tag)
            post.tags.append(tag)

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


@app.route('/posts/<post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.pub_date.asc())

    form = CommentForm()
    if form.validate_on_submit():
        user = User.query.get(g.user.id)
        comment = Comment(body=form.body.data, pub_date=datetime.utcnow(),
                         user_id=g.user.id, post_id= post_id, user=user)
        db.session.add(comment)
        db.session.commit()
        flash('You have succesfully added your comment.')
        return redirect(url_for('view_post', post_id=post_id))

    return render_template('view_post.html', post=post,
                            comments=comments, form=form)

@app.route('/tags/<tag_name>')
@login_required
def posts_with_tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    posts = tag.posts.all()
    return render_template('posts.html', posts=posts, user=g.user)


@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.searching_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.searching_form.search.data))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html', query=query, results=results)


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
