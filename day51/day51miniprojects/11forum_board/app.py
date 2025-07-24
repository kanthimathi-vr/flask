from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Thread, Comment
from forms import RegisterForm, LoginForm, ThreadForm, CommentForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
@login_required
def dashboard():
    # Show only threads created by the current user
    threads = Thread.query.filter_by(user_id=current_user.id).order_by(Thread.timestamp.desc()).all()
    return render_template('dashboard.html', threads=threads)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'info')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", 'info')
    return redirect(url_for('login'))

@app.route('/new_thread', methods=['GET', 'POST'])
@login_required
def new_thread():
    form = ThreadForm()
    if form.validate_on_submit():
        thread = Thread(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(thread)
        db.session.commit()
        flash('Thread posted successfully.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('new_thread.html', form=form)

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
@login_required
def thread(thread_id):
    thread = Thread.query.filter_by(id=thread_id, user_id=current_user.id).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, thread_id=thread.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted.', 'success')
        return redirect(url_for('thread', thread_id=thread.id))
    comments = Comment.query.filter_by(thread_id=thread.id).order_by(Comment.timestamp.asc()).all()
    return render_template('thread.html', thread=thread, comments=comments, form=form)
