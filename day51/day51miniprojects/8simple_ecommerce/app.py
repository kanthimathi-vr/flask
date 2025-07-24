from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Product
from forms import LoginForm, ProductForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.before_first_request
def init():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('admin123'), is_admin=True)
        db.session.add(admin)
        db.session.commit()

def admin_only(func):
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and check_password_hash(u.password, form.password.data):
            login_user(u)
            flash('Logged in successfully.', 'info')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
@login_required
@admin_only
def dashboard():
    products = Product.query.all()
    return render_template('dashboard.html', products=products)

@app.route('/product/new', methods=['GET','POST'])
@login_required
@admin_only
def product_new():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(name=form.name.data, description=form.description.data, price=form.price.data)
        db.session.add(p); db.session.commit()
        flash('Product added.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('product_form.html', form=form, action='New Product')

@app.route('/product/edit/<int:pid>', methods=['GET','POST'])
@login_required
@admin_only
def product_edit(pid):
    p = Product.query.get_or_404(pid)
    form = ProductForm(obj=p)
    if form.validate_on_submit():
        form.populate_obj(p); db.session.commit()
        flash('Product updated.', 'info')
        return redirect(url_for('dashboard'))
    return render_template('product_form.html', form=form, action='Edit Product')

@app.route('/product/delete/<int:pid>', methods=['POST'])
@login_required
@admin_only
def product_delete(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p); db.session.commit()
    flash('Product deleted.', 'warning')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
