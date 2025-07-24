from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Application
from forms import RegistrationForm, LoginForm, ApplicationForm

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'danger')
        else:
            hashed_pw = generate_password_hash(form.password.data)
            user = User(username=form.username.data, password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
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
            flash(f'Welcome {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application(
            job_title=form.job_title.data,
            company=form.company.data,
            user_id=current_user.id
        )
        db.session.add(application)
        db.session.commit()
        flash('Your application has been submitted successfully!', 'success')
        return redirect(url_for('my_applications'))
    return render_template('apply.html', form=form)

@app.route('/my-applications')
@login_required
def my_applications():
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.applied_at.desc()).all()
    return render_template('my_applications.html', applications=applications)

if __name__ == '__main__':
    app.run(debug=True)
