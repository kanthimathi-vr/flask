from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, JournalEntry
from forms import RegistrationForm, LoginForm, JournalEntryForm

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
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.', 'danger')
        else:
            hashed_pw = generate_password_hash(form.password.data)
            user = User(username=form.username.data, password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    entries = JournalEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', entries=entries)

@app.route('/entry/new', methods=['GET', 'POST'])
@login_required
def new_entry():
    form = JournalEntryForm()
    if form.validate_on_submit():
        entry = JournalEntry(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(entry)
        db.session.commit()
        flash('Journal entry created successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html', form=form)

@app.route('/entry/<int:entry_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    form = JournalEntryForm(obj=entry)
    if form.validate_on_submit():
        entry.title = form.title.data
        entry.content = form.content.data
        db.session.commit()
        flash('Journal entry updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_entry.html', form=form)

@app.route('/entry/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    db.session.delete(entry)
    db.session.commit()
    flash('Journal entry deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)