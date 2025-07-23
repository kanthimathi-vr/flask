from flask import request, jsonify
from models import db, Complaint
from sqlalchemy import func

def register_routes(app):

    # Submit complaint
    @app.route('/complaints', methods=['POST'])
    def submit_complaint():
        data = request.get_json()
        complaint = Complaint(
            name=data['name'],
            message=data['message']
        )
        db.session.add(complaint)
        db.session.commit()
        return jsonify({'message': 'Complaint submitted', 'id': complaint.id}), 201

    # View all complaints
    @app.route('/complaints', methods=['GET'])
    def view_complaints():
        complaints = Complaint.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'message': c.message,
            'resolved': c.resolved
        } for c in complaints])

    # Mark complaint as resolved
    @app.route('/complaints/<int:complaint_id>/resolve', methods=['PUT'])
    def mark_resolved(complaint_id):
        complaint = Complaint.query.get_or_404(complaint_id)
        complaint.resolved = True
        db.session.commit()
        return jsonify({'message': 'Complaint marked as resolved'})

    # Delete complaint
    @app.route('/complaints/<int:complaint_id>', methods=['DELETE'])
    def delete_complaint(complaint_id):
        complaint = Complaint.query.get_or_404(complaint_id)
        db.session.delete(complaint)
        db.session.commit()
        return jsonify({'message': 'Complaint deleted'})

    # Get stats: total vs resolved
    @app.route('/complaints/stats', methods=['GET'])
    def get_stats():
        total = db.session.query(func.count(Complaint.id)).scalar()
        resolved = db.session.query(func.count(Complaint.id)).filter_by(resolved=True).scalar()
        return jsonify({
            'total_complaints': total,
            'resolved_complaints': resolved,
            'unresolved_complaints': total - resolved
        })
