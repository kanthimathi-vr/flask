from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Event, RSVP
from forms import RegistrationForm, LoginForm, RSVPForm

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
    # Create some sample events if none exist
    if not Event.query.first():
        sample_events = [
            Event(name="Tech Conference 2025", date="2025-10-10", location="New York"),
            Event(name="Music Festival", date="2025-08-20", location="Los Angeles"),
            Event(name="Art Expo", date="2025-09-15", location="San Francisco"),
        ]
        db.session.bulk_save_objects(sample_events)
        db.session.commit()

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
    session.pop('recent_rsvp_event', None)
    logout_user()
    flash("You've been logged out.", 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    rsvps = RSVP.query.filter_by(user_id=current_user.id).all()
    recent = session.get('recent_rsvp_event')
    return render_template('dashboard.html', rsvps=rsvps, recent=recent)

@app.route('/events')
@login_required
def events():
    all_events = Event.query.all()
    return render_template('events.html', events=all_events)

@app.route('/events/<int:event_id>/rsvp', methods=['GET', 'POST'])
@login_required
def rsvp(event_id):
    event = Event.query.get_or_404(event_id)
    form = RSVPForm()

    existing_rsvp = RSVP.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if existing_rsvp:
        form.status.data = existing_rsvp.status

    if form.validate_on_submit():
        if existing_rsvp:
            existing_rsvp.status = form.status.data
            flash(f'Updated RSVP for "{event.name}" to "{form.status.data}".', 'success')
        else:
            new_rsvp = RSVP(user_id=current_user.id, event_id=event_id, status=form.status.data)
            db.session.add(new_rsvp)
            flash(f'RSVP’d "{form.status.data}" for "{event.name}"!', 'success')
        db.session.commit()
        session['recent_rsvp_event'] = event.name
        return redirect(url_for('dashboard'))

    return render_template('rsvp.html', event=event, form=form)

if __name__ == '__main__':
    app.run(debug=True)