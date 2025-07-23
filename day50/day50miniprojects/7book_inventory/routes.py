from flask import request, jsonify
from models import db, Book

def register_routes(app):

    @app.route('/books', methods=['POST'])
    def add_book():
        data = request.get_json()
        book = Book(
            title=data['title'],
            author=data['author'],
            quantity=data['quantity'],
            published_year=data['published_year']
        )
        db.session.add(book)
        db.session.commit()
        return jsonify({'message': 'Book added successfully', 'id': book.id}), 201

    @app.route('/books', methods=['GET'])
    def get_books():
        books = Book.query.order_by(Book.published_year.asc()).all()
        return jsonify([{
            'id': b.id,
            'title': b.title,
            'author': b.author,
            'quantity': b.quantity,
            'published_year': b.published_year
        } for b in books])

    @app.route('/books/<int:book_id>', methods=['PUT'])
    def update_book_quantity(book_id):
        book = Book.query.get_or_404(book_id)
        data = request.get_json()
        book.quantity = data.get('quantity', book.quantity)
        db.session.commit()
        return jsonify({'message': 'Book quantity updated successfully'})

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
