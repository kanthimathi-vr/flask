from flask import request, jsonify
from models import db, Expense
from datetime import datetime
from sqlalchemy import func

def register_routes(app):

    # Add new expense
    @app.route('/expenses', methods=['POST'])
    def add_expense():
        data = request.get_json()
        try:
            expense = Expense(
                name=data['name'],
                amount=data['amount'],
                category=data['category'],
                date=datetime.strptime(data['date'], '%Y-%m-%d').date()
            )
            db.session.add(expense)
            db.session.commit()
            return jsonify({'message': 'Expense added', 'id': expense.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # View all expenses
    @app.route('/expenses', methods=['GET'])
    def get_expenses():
        expenses = Expense.query.all()
        return jsonify([{
            'id': e.id,
            'name': e.name,
            'amount': e.amount,
            'category': e.category,
            'date': e.date.strftime('%Y-%m-%d')
        } for e in expenses])

    # Update expense
    @app.route('/expenses/<int:expense_id>', methods=['PUT'])
    def update_expense(expense_id):
        expense = Expense.query.get_or_404(expense_id)
        data = request.get_json()

        if 'name' in data:
            expense.name = data['name']
        if 'amount' in data:
            expense.amount = data['amount']
        if 'category' in data:
            expense.category = data['category']
        if 'date' in data:
            expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()

        db.session.commit()
        return jsonify({'message': 'Expense updated'})

    # Delete expense
    @app.route('/expenses/<int:expense_id>', methods=['DELETE'])
    def delete_expense(expense_id):
        expense = Expense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'Expense deleted'})

    # Group expenses by category
    @app.route('/expenses/group-by-category', methods=['GET'])
    def group_by_category():
        grouped = db.session.query(
            Expense.category,
            func.sum(Expense.amount).label('total')
        ).group_by(Expense.category).all()

        return jsonify([{ 'category': cat, 'total': float(total) } for cat, total in grouped])

    # Group expenses by date
    @app.route('/expenses/group-by-date', methods=['GET'])
    def group_by_date():
        grouped = db.session.query(
            Expense.date,
            func.sum(Expense.amount).label('total')
        ).group_by(Expense.date).all()

        return jsonify([{ 'date': d.strftime('%Y-%m-%d'), 'total': float(total) } for d, total in grouped])
