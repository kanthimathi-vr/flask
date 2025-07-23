from flask import request, jsonify
from models import db, User

def register_routes(app):

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([{
            'id': u.id,
            'name': u.name,
            'email': u.email,
            'joined_on': u.joined_on.strftime('%Y-%m-%d %H:%M:%S')
        } for u in users])

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'joined_on': user.joined_on.strftime('%Y-%m-%d %H:%M:%S')
        })

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        user = User(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created', 'id': user.id}), 201

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        db.session.commit()
        return jsonify({'message': 'User updated'})

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'})
