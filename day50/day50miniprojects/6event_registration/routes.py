from flask import request, jsonify
from models import db, Attendee
import validators

def register_routes(app):

    @app.route('/attendees', methods=['POST'])
    def add_attendee():
        data = request.get_json()
        email = data.get('email')
        if not validators.email(email):
            return jsonify({'error': 'Invalid email address'}), 400

        attendee = Attendee(
            name=data['name'],
            email=email,
            event_name=data['event_name']
        )
        db.session.add(attendee)
        db.session.commit()
        return jsonify({'message': 'Attendee registered successfully', 'id': attendee.id}), 201

    @app.route('/attendees', methods=['GET'])
    def get_attendees():
        attendees = Attendee.query.all()
        return jsonify([
            {
                'id': a.id,
                'name': a.name,
                'email': a.email,
                'event_name': a.event_name
            } for a in attendees
        ])

    @app.route('/attendees/<int:attendee_id>', methods=['GET'])
    def get_attendee(attendee_id):
        attendee = Attendee.query.get_or_404(attendee_id)
        return jsonify({
            'id': attendee.id,
            'name': attendee.name,
            'email': attendee.email,
            'event_name': attendee.event_name
        })

    @app.route('/attendees/<int:attendee_id>', methods=['PUT'])
    def update_attendee(attendee_id):
        attendee = Attendee.query.get_or_404(attendee_id)
        data = request.get_json()
        
        email = data.get('email', attendee.email)
        if not validators.email(email):
            return jsonify({'error': 'Invalid email address'}), 400

        attendee.name = data.get('name', attendee.name)
        attendee.email = email
        attendee.event_name = data.get('event_name', attendee.event_name)

        db.session.commit()
        return jsonify({'message': 'Attendee updated successfully'})

    @app.route('/attendees/<int:attendee_id>', methods=['DELETE'])
    def delete_attendee(attendee_id):
        attendee = Attendee.query.get_or_404(attendee_id)
        db.session.delete(attendee)
        db.session.commit()
        return jsonify({'message': 'Attendee deleted successfully'})
