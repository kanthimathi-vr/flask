from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, QuizResult
from forms import RegisterForm, LoginForm, QuizForm

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
            flash(f'Welcome back, {current_user.username}!', 'info')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    results = QuizResult.query.filter_by(user_id=current_user.id).order_by(QuizResult.date_taken.desc()).all()
    return render_template('dashboard.html', results=results)

@app.route('/quiz', methods=['GET','POST'])
@login_required
def quiz():
    form = QuizForm()
    if form.validate_on_submit():
        correct = 0
        answers = {'q1':'4','q2':'Paris'}
        for field, value in form.data.items():
            if field in answers and value == answers[field]:
                correct += 1
        total = len(answers)
        result = QuizResult(score=correct, total=total, user=current_user)
        db.session.add(result)
        db.session.commit()
        flash(f'Quiz completed! You scored {correct}/{total}.', 'success')
        return redirect(url_for('results', result_id=result.id))
    return render_template('quiz.html', form=form)

@app.route('/results/<int:result_id>')
@login_required
def results(result_id):
    result = QuizResult.query.get_or_404(result_id)
    if result.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('results.html', result=result)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
