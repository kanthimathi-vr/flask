from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Review
from forms import RegisterForm, LoginForm, ReviewForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.before_first_request
def init_db():
    db.create_all()

@app.route('/')
def index():
    reviews = Review.query.order_by(Review.date.desc()).all()
    return render_template('index.html', reviews=reviews)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        u = User(username=form.username.data, password=hashed)
        db.session.add(u)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and check_password_hash(u.password, form.password.data):
            login_user(u)
            flash(f'Welcome back, {u.username}!', 'info')
            return redirect(url_for('index'))
        flash('Invalid login.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/movie/<title>', methods=['GET','POST'])
def movie(title):
    form = ReviewForm()
    reviews = Review.query.filter_by(movie_title=title).order_by(Review.date.desc()).all()
    return render_template('movie.html', title=title, reviews=reviews, form=form)

@app.route('/add_review', methods=['POST'])
@login_required
def add_review():
    form = ReviewForm()
    if form.validate_on_submit():
        rev = Review(
            movie_title=form.movie_title.data,
            rating=form.rating.data,
            comment=form.comment.data,
            author=current_user
        )
        db.session.add(rev)
        db.session.commit()
        flash('Review submitted!', 'success')
    else:
        flash('Failed to submit review. Please check inputs.', 'danger')
    return redirect(url_for('movie', title=form.movie_title.data))

if __name__ == '__main__':
    app.run(debug=True)
