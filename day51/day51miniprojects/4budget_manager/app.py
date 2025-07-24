from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Expense
from forms import RegisterForm, LoginForm, ExpenseForm, LimitForm
from datetime import datetime

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
        hashed = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Welcome, {current_user.username}!', 'info')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    exp_form = ExpenseForm()
    lim_form = LimitForm()

    if lim_form.validate_on_submit() and lim_form.set_limit.data:
        session['monthly_limit'] = lim_form.monthly_limit.data
        flash('Monthly limit set.', 'success')
        return redirect(url_for('dashboard'))

    if exp_form.validate_on_submit() and exp_form.submit.data:
        expense = Expense(amt=exp_form.amt.data,
                          category=exp_form.category.data,
                          user=current_user)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added.', 'success')
        return redirect(url_for('dashboard'))

    # Get current month total
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)
    total = sum(e.amt for e in Expense.query.filter(
        Expense.user_id==current_user.id,
        Expense.date >= month_start
    ))

    limit = session.get('monthly_limit')
    if limit and total > limit:
        flash(f'⚠️ You have exceeded your monthly limit of {limit:.2f}!', 'warning')

    return render_template('dashboard.html',
                           exp_form=exp_form,
                           lim_form=lim_form,
                           total=total,
                           limit=limit)

@app.route('/summary')
@login_required
def summary():
    # Group by category
    data = {}
    for e in Expense.query.filter_by(user_id=current_user.id).all():
        data[e.category] = data.get(e.category, 0) + e.amt
    return render_template('summary.html', summary=data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
