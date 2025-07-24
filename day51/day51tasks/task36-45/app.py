from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from config import Config
from models import db, User, ActivityLog
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to continue.'
login_manager.login_message_category = 'danger'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
        else:
            hashed = generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, email=form.email.data, password=hashed)
            db.session.add(new_user)
            db.session.commit()
            flash('Registered successfully!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            session['last_login'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            session['visits'] = session.get('visits', 0) + 1
            user.login_count += 1
            db.session.commit()
            log = ActivityLog(user_id=user.id, action="Login")
            db.session.add(log)
            db.session.commit()
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    log = ActivityLog(user_id=current_user.id, action="Logout")
    db.session.add(log)
    db.session.commit()
    logout_user()
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    app.run(debug=True)
