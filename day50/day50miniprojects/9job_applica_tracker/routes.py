from flask import request, jsonify
from models import db, Application
import validators

VALID_STATUSES = ['applied', 'shortlisted', 'rejected']

def register_routes(app):

    @app.route('/applications', methods=['POST'])
    def add_application():
        data = request.get_json()
        if not validators.email(data.get('email')):
            return jsonify({'error': 'Invalid email format'}), 400

        application = Application(
            name=data['name'],
            email=data['email'],
            job_title=data['job_title'],
            status=data.get('status', 'applied')
        )

        if application.status not in VALID_STATUSES:
            return jsonify({'error': 'Invalid status'}), 400

        db.session.add(application)
        db.session.commit()
        return jsonify({'message': 'Application submitted', 'id': application.id}), 201

    @app.route('/applications', methods=['GET'])
    def get_applications():
        status = request.args.get('status')
        query = Application.query
        if status:
            query = query.filter_by(status=status)
        applications = query.all()
        return jsonify([{
            'id': a.id,
            'name': a.name,
            'email': a.email,
            'job_title': a.job_title,
            'status': a.status
        } for a in applications])

    @app.route('/applications/<int:app_id>', methods=['PUT'])
    def update_application_status(app_id):
        application = Application.query.get_or_404(app_id)
        data = request.get_json()
        new_status = data.get('status')

        if new_status not in VALID_STATUSES:
            return jsonify({'error': 'Invalid status'}), 400

        application.status = new_status
        db.session.commit()
        return jsonify({'message': 'Status updated successfully'})

    @app.route('/applications/<int:app_id>', methods=['DELETE'])
    def delete_application(app_id):
        application = Application.query.get_or_404(app_id)
        db.session.delete(application)
        db.session.commit()
        return jsonify({'message': 'Application deleted successfully'})
