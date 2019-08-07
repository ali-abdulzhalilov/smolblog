from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, CommentForm
from app.models import User, Post, Comment

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = None
    if current_user.is_authenticated:
        form = PostForm()

    if not form is None and form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is live!')
        return redirect(url_for('index'))

    posts = Post.query.all() #sort by date
    return render_template('index.html', title='Home', form=form, posts=posts)

# post stuff
@app.route('/view/p/<post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id).all()

    if current_user.is_authenticated:
        form = CommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated: #sanity check
            return redirect(url_for('index'))

        new_comment = Comment(body=form.body.data, author=current_user, post=post)
        db.session.add(new_comment)
        db.session.commit()
        flash('Your comment is live!')
        return redirect(url_for('view_post', post_id=post.id))

    return render_template('view_post.html', post=post, form=form, comments=comments)

@app.route('/edit/p/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()

    if current_user != post.author: #sanity check
        return redirect(url_for('index'))

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for('view_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('edit_post.html', form=form, post=post)

@app.route('/delete/p/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if current_user != post.author: #sanity check
        return redirect(url_for('index'))

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted')

    return redirect(url_for('index'))

# login stuff
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next = request.args.get('next')

        if not next or url_parse(next).netloc != '':
            return redirect(url_for('index'))

        return redirect(next)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Now you\'re registred.')

        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)
