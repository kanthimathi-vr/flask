from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from config import Config
from models import db, User, Appointment
from forms import LoginForm, AppointmentForm

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
    # Create a default user if none exist
    if not User.query.filter_by(username='user1').first():
        user = User(username='user1', password=generate_password_hash('password'))
        db.session.add(user)
        db.session.commit()

@app.route('/')
@login_required
def dashboard():
    appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.appointment_date).all()
    return render_template('dashboard.html', appointments=appointments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
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

@app.route('/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(
            title=form.title.data,
            description=form.description.data,
            appointment_date=form.appointment_date.data,
            user_id=current_user.id
        )
        db.session.add(appointment)
        db.session.commit()
        flash(f'Appointment "{appointment.title}" booked for {appointment.appointment_date.strftime("%Y-%m-%d %H:%M")}.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('book_appointment.html', form=form)

@app.route('/update/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.user_id != current_user.id:
        flash("You don't have permission to edit this appointment.", "danger")
        return redirect(url_for('dashboard'))
    
    form = AppointmentForm(obj=appointment)
    if form.validate_on_submit():
        appointment.title = form.title.data
        appointment.description = form.description.data
        appointment.appointment_date = form.appointment_date.data
        db.session.commit()
        flash('Appointment updated successfully.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('update_appointment.html', form=form)

@app.route('/cancel/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.user_id != current_user.id:
        flash("You don't have permission to cancel this appointment.", "danger")
        return redirect(url_for('dashboard'))
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment canceled successfully.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
