from flask import request, jsonify
from models import db, Student
import validators

def register_routes(app):

    @app.route('/students', methods=['POST'])
    def register_student():
        data = request.get_json()
        email = data.get('email')
        
        if not validators.email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        student = Student(
            name=data['name'],
            roll_no=data['roll_no'],
            email=email,
            age=data['age']
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'Student registered successfully', 'id': student.id}), 201

    @app.route('/students', methods=['GET'])
    def get_students():
        students = Student.query.all()
        return jsonify([{
            'id': s.id,
            'name': s.name,
            'roll_no': s.roll_no,
            'email': s.email,
            'age': s.age
        } for s in students])

    @app.route('/students/<int:student_id>', methods=['GET'])
    def get_student(student_id):
        student = Student.query.get_or_404(student_id)
        return jsonify({
            'id': student.id,
            'name': student.name,
            'roll_no': student.roll_no,
            'email': student.email,
            'age': student.age
        })

    @app.route('/students/<int:student_id>', methods=['PUT'])
    def update_student(student_id):
        student = Student.query.get_or_404(student_id)
        data = request.get_json()

        email = data.get('email', student.email)
        if email and not validators.email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        student.name = data.get('name', student.name)
        student.roll_no = data.get('roll_no', student.roll_no)
        student.email = email
        student.age = data.get('age', student.age)

        db.session.commit()
        return jsonify({'message': 'Student profile updated'})

    @app.route('/students/<int:student_id>', methods=['DELETE'])
    def delete_student(student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted'})
