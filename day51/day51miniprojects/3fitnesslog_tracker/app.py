from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Workout
from forms import RegisterForm, LoginForm, WorkoutForm, ProfileForm
from config import Config
from datetime import date

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def setup():
    db.create_all()

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Welcome back, {current_user.username}!', 'info')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    form = WorkoutForm()
    last_type = session.get('last_type', '')
    if request.method == 'GET' and last_type:
        form.type.data = last_type

    if form.validate_on_submit():
        workout = Workout(
            user=current_user,
            type=form.type.data,
            steps=form.steps.data,
            hours=form.hours.data
        )
        db.session.add(workout)
        db.session.commit()
        session['last_type'] = form.type.data
        flash('Workout logged!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', form=form)

@app.route('/history')
@login_required
def history():
    logs = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    return render_template('history.html', logs=logs)

@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    form = ProfileForm(username=current_user.username)
    if form.validate_on_submit():
        if not check_password_hash(current_user.password, form.current_password.data):
            flash('Incorrect current password.', 'danger')
        else:
            current_user.username = form.username.data
            if form.new_password.data:
                current_user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Profile updated successfully.', 'success')
            return redirect(url_for('dashboard'))
    return render_template('profile.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
