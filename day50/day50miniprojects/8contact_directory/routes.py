from flask import request, jsonify
from models import db, Contact
import validators
import re

def is_valid_phone(phone):
    return re.fullmatch(r'^[0-9]{10,15}$', phone)

def register_routes(app):

    @app.route('/contacts', methods=['POST'])
    def add_contact():
        data = request.get_json()

        if not validators.email(data.get('email', '')):
            return jsonify({'error': 'Invalid email format'}), 400

        if not is_valid_phone(data.get('phone', '')):
            return jsonify({'error': 'Invalid phone number'}), 400

        contact = Contact(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            address=data.get('address', '')
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify({'message': 'Contact added successfully', 'id': contact.id}), 201

    @app.route('/contacts', methods=['GET'])
    def get_contacts():
        contacts = Contact.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'phone': c.phone,
            'email': c.email,
            'address': c.address
        } for c in contacts])

    @app.route('/contacts/<int:contact_id>', methods=['PUT'])
    def update_contact(contact_id):
        contact = Contact.query.get_or_404(contact_id)
        data = request.get_json()

        if 'email' in data and not validators.email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400

        if 'phone' in data and not is_valid_phone(data['phone']):
            return jsonify({'error': 'Invalid phone number'}), 400

        contact.name = data.get('name', contact.name)
        contact.phone = data.get('phone', contact.phone)
        contact.email = data.get('email', contact.email)
        contact.address = data.get('address', contact.address)

        db.session.commit()
        return jsonify({'message': 'Contact updated successfully'})

    @app.route('/contacts/<int:contact_id>', methods=['DELETE'])
    def delete_contact(contact_id):
        contact = Contact.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully'})
