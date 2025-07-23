from flask import request, jsonify
from datetime import datetime, date
from models import db, Appointment

def register_routes(app):

    # Book appointment
    @app.route('/appointments', methods=['POST'])
    def book_appointment():
        data = request.get_json()
        try:
            appointment = Appointment(
                name=data['name'],
                date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
                time=datetime.strptime(data['time'], '%H:%M').time(),
                status=data.get('status', 'pending')
            )
            db.session.add(appointment)
            db.session.commit()
            return jsonify({'message': 'Appointment booked', 'id': appointment.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # View all appointments
    @app.route('/appointments', methods=['GET'])
    def get_appointments():
        appointments = Appointment.query.all()
        return jsonify([
            {
                'id': a.id,
                'name': a.name,
                'date': a.date.strftime('%Y-%m-%d'),
                'time': a.time.strftime('%H:%M'),
                'status': a.status
            } for a in appointments
        ])

    # Update appointment status
    @app.route('/appointments/<int:appt_id>', methods=['PUT'])
    def update_status(appt_id):
        appointment = Appointment.query.get_or_404(appt_id)
        data = request.get_json()
        if 'status' in data and data['status'] in ['confirmed', 'canceled']:
            appointment.status = data['status']
            db.session.commit()
            return jsonify({'message': 'Status updated'})
        return jsonify({'error': 'Invalid status'}), 400

    # Delete expired appointments (past date)
    @app.route('/appointments/cleanup', methods=['DELETE'])
    def delete_expired():
        today = date.today()
        expired = Appointment.query.filter(Appointment.date < today).all()
        count = len(expired)
        for a in expired:
            db.session.delete(a)
        db.session.commit()
        return jsonify({'message': f'{count} expired appointments deleted'})
