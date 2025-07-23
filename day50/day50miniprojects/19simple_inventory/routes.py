from flask import request, jsonify
from models import db, Item
from datetime import datetime

def register_routes(app):

    # Add new item
    @app.route('/items', methods=['POST'])
    def add_item():
        data = request.get_json()
        name = data.get('name')
        quantity = data.get('quantity')

        if not name or quantity is None:
            return jsonify({'error': 'Name and quantity required'}), 400

        if not isinstance(quantity, int) or quantity < 0:
            return jsonify({'error': 'Quantity must be a non-negative integer'}), 400

        item = Item(name=name, quantity=quantity, updated_on=datetime.utcnow())
        db.session.add(item)
        db.session.commit()
        return jsonify({'message': 'Item added', 'id': item.id}), 201

    # Update quantity (and timestamp)
    @app.route('/items/<int:id>', methods=['PUT'])
    def update_item(id):
        item = Item.query.get_or_404(id)
        data = request.get_json()
        quantity = data.get('quantity')

        if quantity is None:
            return jsonify({'error': 'Quantity required'}), 400
        if not isinstance(quantity, int) or quantity < 0:
            return jsonify({'error': 'Quantity must be a non-negative integer'}), 400

        if quantity == 0:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': 'Item deleted because quantity reached zero'})

        item.quantity = quantity
        item.updated_on = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Item quantity updated'})

    # Delete item manually
    @app.route('/items/<int:id>', methods=['DELETE'])
    def delete_item(id):
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted'})

    # Get all items
    @app.route('/items', methods=['GET'])
    def list_items():
        items = Item.query.order_by(Item.updated_on.desc()).all()
        result = []
        for i in items:
            result.append({
                'id': i.id,
                'name': i.name,
                'quantity': i.quantity,
                'updated_on': i.updated_on.strftime('%Y-%m-%d %H:%M:%S')
            })
        return jsonify(result)
