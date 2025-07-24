from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Note
from forms import LoginForm, RegisterForm, NoteForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Registered successfully!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome {current_user.username}!", "info")
            return redirect(url_for('dashboard'))
        flash("Login failed. Check username and password.", "danger")
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', notes=notes)

@app.route('/note/new', methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, owner=current_user)
        db.session.add(note)
        db.session.commit()
        flash("Note created!", "success")
        return redirect(url_for('dashboard'))
    return render_template('note_form.html', form=form)

@app.route('/note/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.owner != current_user:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('dashboard'))
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash("Note updated!", "info")
        return redirect(url_for('dashboard'))
    return render_template('note_form.html', form=form)

@app.route('/note/delete/<int:note_id>')
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.owner != current_user:
        flash("Unauthorized access!", "danger")
    else:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted!", "warning")
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
