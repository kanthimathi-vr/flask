from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Entry
from forms import RegisterForm, LoginForm, EntryForm
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.before_first_request
def setup():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and check_password_hash(u.password, form.password.data):
            login_user(u)
            session['login_time'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            flash('Logged in successfully.', 'info')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    entries = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.timestamp.desc()).all()
    login_time = session.get('login_time')
    return render_template('dashboard.html', entries=entries, login_time=login_time)

@app.route('/entry/new', methods=['GET', 'POST'])
@login_required
def new_entry():
    form = EntryForm()
    if form.validate_on_submit():
        e = Entry(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(e); db.session.commit()
        flash('Entry created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('entry_form.html', form=form, action='New Entry')

@app.route('/entry/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    e = Entry.query.get_or_404(entry_id)
    if e.author != current_user:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('dashboard'))
    form = EntryForm(obj=e)
    if form.validate_on_submit():
        e.title = form.title.data
        e.content = form.content.data
        db.session.commit()
        flash('Entry updated.', 'info')
        return redirect(url_for('dashboard'))
    return render_template('entry_form.html', form=form, action='Edit Entry')

@app.route('/entry/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    e = Entry.query.get_or_404(entry_id)
    if e.author == current_user:
        db.session.delete(e); db.session.commit()
        flash('Entry deleted.', 'warning')
    else:
        flash('Unauthorized.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
