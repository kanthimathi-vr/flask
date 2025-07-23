from flask import jsonify
from models import db, User, Product, Blog

def register_routes(app):

    # 1. Get all users
    @app.route('/users', methods=['GET'])
    def get_all_users():
        users = User.query.all()
        if users:
            return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users])
        else:
            return jsonify({'message': 'No users found'}), 404

    # 2. Get user by ID
    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
        else:
            return jsonify({'error': 'User not found'}), 404

    # 3. Get user by email
    @app.route('/users/email/<email>', methods=['GET'])
    def get_user_by_email(email):
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'id': user.id, 'name': user.name})
        else:
            return jsonify({'error': 'Email not found'}), 404

    # 4. All products in stock
    @app.route('/products/in-stock', methods=['GET'])
    def get_instock_products():
        products = Product.query.filter_by(in_stock=True).all()
        return jsonify([{'id': p.id, 'name': p.name, 'price': p.price} for p in products])

    # 5. Blogs by date desc
    @app.route('/blogs/recent', methods=['GET'])
    def get_recent_blogs():
        blogs = Blog.query.order_by(Blog.created_at.desc()).all()
        return jsonify([{
            'title': b.title,
            'content': b.content,
            'date': b.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for b in blogs])

    # 6. Count users
    @app.route('/users/count', methods=['GET'])
    def count_users():
        total = User.query.count()
        return jsonify({'total_users': total})

    # 7. User details like /user/<id>
    @app.route('/user/<int:id>', methods=['GET'])
    def user_detail(id):
        user = User.query.get(id)
        if user:
            return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
        return jsonify({'error': 'User not found'}), 404

    # 10. Convert query result to dict
    @app.route('/users/dict', methods=['GET'])
    def user_as_dict():
        user = User.query.first()
        if user:
            user_dict = {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
            print(user_dict)  # logs in terminal
            return jsonify(user_dict)
        return jsonify({'error': 'No user found'})
