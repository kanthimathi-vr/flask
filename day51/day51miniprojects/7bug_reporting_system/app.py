from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Bug
from forms import RegisterForm, LoginForm, BugForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and check_password_hash(u.password, form.password.data):
            login_user(u)
            flash(f'Welcome, {u.username}!', 'info')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    bugs = Bug.query.filter_by(user_id=current_user.id).order_by(Bug.date_submitted.desc()).all()
    last_title = session.get('last_bug_title')
    return render_template('dashboard.html', bugs=bugs, last_title=last_title)

@app.route('/submit', methods=['GET','POST'])
@login_required
def submit_bug():
    form = BugForm()
    if form.validate_on_submit():
        bug = Bug(title=form.title.data,
                  description=form.description.data,
                  reporter=current_user)
        db.session.add(bug)
        db.session.commit()
        session['last_bug_title'] = form.title.data
        flash('Bug report submitted!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('submit_bug.html', form=form)
  
if __name__ == '__main__':
    app.run(debug=True)
