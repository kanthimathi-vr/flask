from flask import request, jsonify
from models import db, User, Product, Category, Blog, Review, Subscription

def register_routes(app):

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created', 'id': user.id}), 201

    @app.route('/products', methods=['POST'])
    def create_product():
        data = request.get_json()
        product = Product(
            name=data['name'],
            price=data['price'],
            in_stock=data.get('in_stock', True),
            category_id=data.get('category_id')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product created', 'id': product.id}), 201

    @app.route('/categories', methods=['POST'])
    def create_category():
        data = request.get_json()
        category = Category(name=data['name'])
        db.session.add(category)
        db.session.commit()
        return jsonify({'message': 'Category added', 'id': category.id})

    @app.route('/blogs', methods=['POST'])
    def create_blog():
        data = request.get_json()
        blog = Blog(title=data['title'], content=data['content'])
        db.session.add(blog)
        db.session.commit()
        return jsonify({'message': 'Blog posted', 'id': blog.id})

    @app.route('/reviews', methods=['POST'])
    def create_review():
        data = request.get_json()
        review = Review(
            rating=data['rating'],
            comment=data.get('comment'),
            user_id=data['user_id'],
            product_id=data['product_id']
        )
        db.session.add(review)
        db.session.commit()
        return jsonify({'message': 'Review added', 'id': review.id})

    @app.route('/subscriptions', methods=['POST'])
    def create_subscription():
        data = request.get_json()
        sub = Subscription(
            user_name=data['user_name'],
            is_active=data.get('is_active', True),
            plan=data.get('plan', 'Free')
        )
        db.session.add(sub)
        db.session.commit()
        return jsonify({'message': 'Subscription created', 'id': sub.id})

    # Optional: list route
    @app.route('/models', methods=['GET'])
    def list_models():
        return jsonify({
            'users': [u.email for u in User.query.all()],
            'products': [p.name for p in Product.query.all()],
            'categories': [c.name for c in Category.query.all()]
        })
