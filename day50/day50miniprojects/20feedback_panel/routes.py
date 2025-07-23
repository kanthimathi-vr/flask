from flask import request, jsonify
from models import db, Feedback

def register_routes(app):
    
    # Add feedback
    @app.route('/feedback', methods=['POST'])
    def add_feedback():
        data = request.get_json()
        user_name = data.get('user_name')
        rating = data.get('rating')
        comment = data.get('comment', '')

        if not user_name or rating is None:
            return jsonify({'error': 'user_name and rating are required'}), 400

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400

        feedback = Feedback(user_name=user_name, rating=rating, comment=comment)
        db.session.add(feedback)
        db.session.commit()
        return jsonify({'message': 'Feedback submitted', 'id': feedback.id}), 201

    # View all feedback
    @app.route('/feedback', methods=['GET'])
    def get_feedback():
        feedback_list = Feedback.query.all()
        return jsonify([{
            'id': fb.id,
            'user_name': fb.user_name,
            'rating': fb.rating,
            'comment': fb.comment
        } for fb in feedback_list])

    # Update feedback
    @app.route('/feedback/<int:id>', methods=['PUT'])
    def update_feedback(id):
        feedback = Feedback.query.get_or_404(id)
        data = request.get_json()

        feedback.user_name = data.get('user_name', feedback.user_name)
        feedback.comment = data.get('comment', feedback.comment)

        rating = data.get('rating')
        if rating is not None:
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
            feedback.rating = rating

        db.session.commit()
        return jsonify({'message': 'Feedback updated'})

    # Delete feedback
    @app.route('/feedback/<int:id>', methods=['DELETE'])
    def delete_feedback(id):
        feedback = Feedback.query.get_or_404(id)
        db.session.delete(feedback)
        db.session.commit()
        return jsonify({'message': 'Feedback deleted'})
