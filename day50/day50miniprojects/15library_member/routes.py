from flask import request, jsonify
from models import db, Member
from datetime import datetime

def register_routes(app):

    # Add a member
    @app.route('/members', methods=['POST'])
    def add_member():
        data = request.get_json()
        try:
            member = Member(
                name=data['name'],
                email=data['email'],
                join_date=datetime.strptime(data['join_date'], '%Y-%m-%d').date()
            )
            db.session.add(member)
            db.session.commit()
            return jsonify({'message': 'Member added', 'id': member.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # View all members (sorted by join_date)
    @app.route('/members', methods=['GET'])
    def view_members():
        members = Member.query.order_by(Member.join_date.asc()).all()
        return jsonify([{
            'id': m.id,
            'name': m.name,
            'email': m.email,
            'join_date': m.join_date.strftime('%Y-%m-%d')
        } for m in members])

    # Delete a member
    @app.route('/members/<int:member_id>', methods=['DELETE'])
    def delete_member(member_id):
        member = Member.query.get_or_404(member_id)
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Member deleted'})
