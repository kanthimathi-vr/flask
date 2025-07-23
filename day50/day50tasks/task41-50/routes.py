from flask import request, jsonify
from models import db, User, Product, AuditLog

def log_change(entity, field, before, after):
    log = AuditLog(entity=entity, field=field, before=str(before), after=str(after))
    db.session.add(log)

def register_routes(app):

    # 1. Update user info
    @app.route('/user/<int:id>/edit', methods=['PUT'])
    def update_user(id):
        user = User.query.get(id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        before = {'name': user.name, 'email': user.email}

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)

        log_change('User', 'name', before['name'], user.name)
        log_change('User', 'email', before['email'], user.email)

        db.session.commit()
        return jsonify({'message': 'User updated', 'updated': {'name': user.name, 'email': user.email}})

    # 3. Update product stock status
    @app.route('/product/<int:id>/stock', methods=['PUT'])
    def update_stock(id):
        product = Product.query.get(id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        data = request.get_json()
        before = product.in_stock
        product.in_stock = data.get('in_stock', product.in_stock)

        log_change('Product', 'in_stock', before, product.in_stock)
        db.session.commit()

        return jsonify({'message': 'Stock status updated', 'in_stock': product.in_stock})

    # 8. Change password (check current password)
    @app.route('/user/<int:id>/password', methods=['PUT'])
    def change_password(id):
        user = User.query.get(id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if user.password != current_password:
            return jsonify({'error': 'Incorrect current password'}), 401

        log_change('User', 'password', '***', '***')
        user.password = new_password
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'})

    # 9. Update profile (multi-field)
    @app.route('/user/<int:id>/profile', methods=['PUT'])
    def update_profile(id):
        user = User.query.get(id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        changes = {}

        if 'name' in data and data['name'] != user.name:
            log_change('User', 'name', user.name, data['name'])
            user.name = data['name']
            changes['name'] = user.name

        if 'email' in data and data['email'] != user.email:
            log_change('User', 'email', user.email, data['email'])
            user.email = data['email']
            changes['email'] = user.email

        db.session.commit()
        return jsonify({'message': 'Profile updated', 'changes': changes})

    # 10. View audit logs
    @app.route('/audit', methods=['GET'])
    def get_audit_logs():
        logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
        return jsonify([{
            'entity': l.entity,
            'field': l.field,
            'before': l.before,
            'after': l.after,
            'timestamp': l.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for l in logs])
