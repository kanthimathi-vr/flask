from flask import request, jsonify
from models import db, User, Product, Blog
from sqlalchemy.exc import IntegrityError

def register_routes(app):

    # 1. Create a user
    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        try:
            user = User(name=data['name'], email=data['email'])
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'User created', 'id': user.id}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Email already exists'}), 400

    # 2. Create product (default in_stock=True)
    @app.route('/products', methods=['POST'])
    def create_product():
        data = request.get_json()
        product = Product(
            name=data['name'],
            price=data['price'],
            in_stock=data.get('in_stock', True)
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product created', 'id': product.id})

    # 3. Blog post (as form-style JSON)
    @app.route('/blogs', methods=['POST'])
    def create_blog():
        data = request.get_json()
        blog = Blog(title=data['title'], content=data['content'])
        db.session.add(blog)
        db.session.commit()
        return jsonify({'message': 'Blog post created', 'id': blog.id})

    # 4. Route to insert dummy users/products
    @app.route('/dummy-data', methods=['POST'])
    def add_dummy():
        try:
            u1 = User(name='Alice', email='alice@test.com')
            u2 = User(name='Bob', email='bob@test.com')
            p1 = Product(name='Mouse', price=10.5)
            p2 = Product(name='Keyboard', price=20.0)
            db.session.add_all([u1, u2, p1, p2])
            db.session.commit()
            return jsonify({'message': 'Dummy data added'})
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Duplicate email in dummy users'}), 400

    # 5. Bulk insert items
    @app.route('/bulk-products', methods=['POST'])
    def bulk_products():
        data = request.get_json()
        products = [
            Product(name=item['name'], price=item['price'], in_stock=item.get('in_stock', True))
            for item in data
        ]
        db.session.add_all(products)
        db.session.commit()
        return jsonify({'message': f'{len(products)} products inserted'})

    # 6. Simulated Flask-WTF form insert (API only)
    @app.route('/create-user-form', methods=['POST'])
    def form_user():
        data = request.get_json()
        if 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and Email required'}), 400
        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created via form', 'id': user.id})

    # 7. Test commit failure
    @app.route('/test-commit-fail', methods=['POST'])
    def test_commit():
        user = User(name='Test User', email='alice@test.com')  # duplicate email
        db.session.add(user)
        try:
            db.session.commit()
            return jsonify({'message': 'Commit success'})
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Commit failed — likely duplicate email'}), 409

    # 8. View blog timestamps
    @app.route('/blogs', methods=['GET'])
    def get_blogs():
        blogs = Blog.query.all()
        return jsonify([{
            'title': b.title,
            'created_at': b.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for b in blogs])
