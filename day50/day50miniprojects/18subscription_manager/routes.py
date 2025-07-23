from flask import request, jsonify
from models import db, Subscriber
from email_validator import validate_email, EmailNotValidError
from datetime import datetime

def register_routes(app):

    # Add subscriber
    @app.route('/subscribers', methods=['POST'])
    def add_subscriber():
        data = request.get_json()
        print("Received data:", data)  # Debug print
        email = data.get('email')
        plan = data.get('plan')
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            return jsonify({'error': str(e)}), 400

        if not plan:
            print("Missing plan")
            return jsonify({'error': 'Subscription plan required'}), 400

        # Check if already subscribed
        if Subscriber.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already subscribed'}), 400

        subscriber = Subscriber(email=email, plan=plan, subscribed_on=datetime.utcnow())
        db.session.add(subscriber)
        db.session.commit()
        return jsonify({'message': 'Subscriber added', 'id': subscriber.id}), 201

    # List active subscribers
    @app.route('/subscribers', methods=['GET'])
    def list_subscribers():
        subscribers = Subscriber.query.all()
        return jsonify([{
            'id': s.id,
            'email': s.email,
            'plan': s.plan,
            'subscribed_on': s.subscribed_on.strftime('%Y-%m-%d %H:%M:%S')
        } for s in subscribers])

    # Update subscription plan
    @app.route('/subscribers/<int:id>', methods=['PUT'])
    def update_plan(id):
        subscriber = Subscriber.query.get_or_404(id)
        data = request.get_json()
        plan = data.get('plan')
        if not plan:
            return jsonify({'error': 'Subscription plan required'}), 400
        subscriber.plan = plan
        db.session.commit()
        return jsonify({'message': 'Subscription plan updated'})

    # Delete subscriber
    @app.route('/subscribers/<int:id>', methods=['DELETE'])
    def delete_subscriber(id):
        subscriber = Subscriber.query.get_or_404(id)
        db.session.delete(subscriber)
        db.session.commit()
        return jsonify({'message': 'Subscriber deleted'})
