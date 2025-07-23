from flask import request, jsonify
from models import db, Product

def register_routes(app):

    @app.route('/products', methods=['POST'])
    def add_product():
        data = request.get_json()
        product = Product(
            name=data['name'],
            price=data['price'],
            in_stock=data.get('in_stock', True),
            description=data.get('description', '')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully', 'id': product.id}), 201

    @app.route('/products', methods=['GET'])
    def get_all_products():
        products = Product.query.all()
        return jsonify([
            {
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'in_stock': p.in_stock,
                'description': p.description
            } for p in products
        ])

    @app.route('/products/in-stock', methods=['GET'])
    def get_in_stock_products():
        products = Product.query.filter_by(in_stock=True).all()
        return jsonify([
            {
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'description': p.description
            } for p in products
        ])

    @app.route('/products/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'in_stock': product.in_stock,
            'description': product.description
        })

    @app.route('/products/<int:product_id>', methods=['PUT'])
    def update_product(product_id):
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.in_stock = data.get('in_stock', product.in_stock)
        product.description = data.get('description', product.description)
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})

    @app.route('/products/<int:product_id>', methods=['DELETE'])
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
