from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Book, Borrow
from forms import LoginForm

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
    # Create some sample books if none exist
    if Book.query.count() == 0:
        sample_books = [
            Book(title='1984', author='George Orwell'),
            Book(title='To Kill a Mockingbird', author='Harper Lee'),
            Book(title='The Great Gatsby', author='F. Scott Fitzgerald'),
        ]
        db.session.bulk_save_objects(sample_books)
        db.session.commit()
    # Create admin user if none
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', password=generate_password_hash('adminpass'), is_admin=True)
        db.session.add(admin_user)
        db.session.commit()

@app.route('/')
@login_required
def dashboard():
    borrowed = Borrow.query.filter_by(user_id=current_user.id).order_by(Borrow.borrow_date.desc()).all()
    recent = session.get('recently_borrowed', [])
    return render_template('dashboard.html', borrowed=borrowed, recent=recent)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'info')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You've been logged out.", 'info')
    return redirect(url_for('login'))

@app.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
    books = Book.query.filter_by(available=True).all()
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        book = Book.query.get(book_id)
        if book and book.available:
            # Mark book unavailable
            book.available = False
            # Add borrow record
            borrow = Borrow(user_id=current_user.id, book_id=book.id)
            db.session.add(borrow)
            db.session.commit()
            # Store recently borrowed books in session
            recent = session.get('recently_borrowed', [])
            recent.insert(0, {'title': book.title, 'author': book.author})
            session['recently_borrowed'] = recent[:5]  # keep last 5
            flash(f'You borrowed "{book.title}".', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Book not available.', 'warning')
    return render_template('borrow.html', books=books)

@app.route('/admin/borrowed')
@login_required
def admin_borrowed():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    borrows = Borrow.query.order_by(Borrow.borrow_date.desc()).all()
    return render_template('admin_borrowed.html', borrows=borrows)
