from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Book
from forms import RegistrationForm, LoginForm, BookForm, UpdateProgressForm

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
    session.pop('last_viewed_book', None)  # clear last viewed book on logout
    logout_user()
    flash("You've been logged out.", 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    book_count = Book.query.filter_by(user_id=current_user.id).count()
    last_viewed = session.get('last_viewed_book')
    return render_template('dashboard.html', book_count=book_count, last_viewed=last_viewed)

@app.route('/books')
@login_required
def books():
    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template('books.html', books=books)

@app.route('/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            total_pages=form.total_pages.data,
            user_id=current_user.id
        )
        db.session.add(book)
        db.session.commit()
        flash(f'Book "{book.title}" added!', 'success')
        return redirect(url_for('books'))
    return render_template('add_book.html', form=form)

@app.route('/books/<int:book_id>', methods=['GET', 'POST'])
@login_required
def view_book(book_id):
    book = Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    form = UpdateProgressForm(obj=book)
    if form.validate_on_submit():
        if form.pages_read.data > book.total_pages:
            flash("Pages read can't exceed total pages.", 'danger')
        else:
            book.pages_read = form.pages_read.data
            db.session.commit()
            flash("Progress updated!", "success")
    session['last_viewed_book'] = book.title
    return render_template('view_book.html', book=book, form=form)

if __name__ == '__main__':
    app.run(debug=True)