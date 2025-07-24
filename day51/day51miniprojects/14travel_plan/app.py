from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from config import Config
from models import db, User, TravelPlan
from forms import RegistrationForm, LoginForm, TravelPlanForm, SearchForm

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

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = SearchForm()
    plans_query = TravelPlan.query.filter_by(user_id=current_user.id)

    if form.validate_on_submit():
        search_country = form.country.data.strip()
        session['last_search_country'] = search_country
        if search_country:
            plans_query = plans_query.filter(TravelPlan.place.ilike(f'%{search_country}%'))
        else:
            flash('Please enter a country to search.', 'warning')
    else:
        if 'last_search_country' in session:
            last_search = session['last_search_country']
            if last_search:
                plans_query = plans_query.filter(TravelPlan.place.ilike(f'%{last_search}%'))
                form.country.data = last_search

    plans = plans_query.order_by(TravelPlan.travel_date).all()
    total_plans = TravelPlan.query.filter_by(user_id=current_user.id).count()

    return render_template('dashboard.html', plans=plans, total_plans=total_plans, form=form)

@app.route('/add_plan', methods=['GET', 'POST'])
@login_required
def add_plan():
    form = TravelPlanForm()
    if form.validate_on_submit():
        plan = TravelPlan(
            place=form.place.data,
            travel_date=form.travel_date.data,
            reason=form.reason.data,
            user_id=current_user.id
        )
        db.session.add(plan)
        db.session.commit()
        flash(f'Travel plan to {plan.place} added.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_plan.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
