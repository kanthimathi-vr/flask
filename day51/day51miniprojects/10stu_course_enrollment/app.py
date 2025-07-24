from flask import Flask, render_template, redirect, url_for, flash
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Course, Enrollment
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.before_first_request
def init():
    db.create_all()
    if not Course.query.first():
        sample = [
            Course(name='Math 101', description='Basic Mathematics'),
            Course(name='History 201', description='World History'),
            Course(name='Physics 301', description='Advanced Physics')
        ]
        db.session.bulk_save_objects(sample)
        db.session.commit()

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data,
                 password=generate_password_hash(form.password.data))
        db.session.add(u); db.session.commit()
        flash('Welcome! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and check_password_hash(u.password, form.password.data):
            login_user(u)
            flash('Logged in successfully.', 'info')
            return redirect(url_for('courses'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/courses')
@login_required
def courses():
    courses = Course.query.all()
    enrolled_ids = {e.course_id for e in current_user.enrollments}
    return render_template('courses.html', courses=courses, enrolled_ids=enrolled_ids)

@app.route('/enroll/<int:cid>')
@login_required
def enroll(cid):
    if not Enrollment.query.filter_by(user_id=current_user.id, course_id=cid).first():
        e = Enrollment(user_id=current_user.id, course_id=cid)
        db.session.add(e); db.session.commit()
        flash('Enrolled successfully!', 'success')
    else:
        flash('Already enrolled.', 'warning')
    return redirect(url_for('courses'))

@app.route('/history')
@login_required
def history():
    return render_template('history.html', enrollments=current_user.enrollments)

if __name__ == '__main__':
    app.run(debug=True)
