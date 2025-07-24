from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from forms import LoginForm, RegisterForm, TaskForm
from models import db, User, Task

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        app.db_initialized = True



@app.route('/')
def home():
    return redirect(url_for('tasks'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if len(form.password.data) >= 8:
            flash("Password must be less than 8 characters.", "danger")
            return render_template('register.html', form=form)
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully. Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for('tasks'))
        flash("Invalid username or password.", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for('login'))

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, due_date=form.due_date.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash("Task added successfully.", "success")
        return redirect(url_for('tasks'))
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', form=form, tasks=tasks)

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('tasks'))
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash("Task updated successfully.", "success")
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', form=form)

@app.route('/task/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted.", "info")
    return redirect(url_for('tasks'))

@app.route('/task/<int:task_id>/toggle')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
        flash("Task status updated.", "info")
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True)
