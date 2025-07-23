from flask import request, jsonify
from models import db, Student, Course, Enrollment

def register_routes(app):

    # Add a student
    @app.route('/students', methods=['POST'])
    def add_student():
        data = request.get_json()
        student = Student(name=data['name'])
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'Student added', 'id': student.id}), 201

    # Add a course
    @app.route('/courses', methods=['POST'])
    def add_course():
        data = request.get_json()
        course = Course(name=data['name'], fee=data['fee'])
        db.session.add(course)
        db.session.commit()
        return jsonify({'message': 'Course added', 'id': course.id}), 201

    # Enroll a student in a course
    @app.route('/enroll', methods=['POST'])
    def enroll_student():
        data = request.get_json()
        enrollment = Enrollment(student_id=data['student_id'], course_id=data['course_id'])
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({'message': 'Student enrolled successfully', 'id': enrollment.id}), 201

    # View all enrollments (student-course pairings)
    @app.route('/enrollments', methods=['GET'])
    def view_enrollments():
        enrollments = Enrollment.query.all()
        result = []
        for e in enrollments:
            result.append({
                'enrollment_id': e.id,
                'student_id': e.student.id,
                'student_name': e.student.name,
                'course_id': e.course.id,
                'course_name': e.course.name,
                'course_fee': e.course.fee
            })
        return jsonify(result)

    # Update an enrollment
    @app.route('/enrollments/<int:enroll_id>', methods=['PUT'])
    def update_enrollment(enroll_id):
        data = request.get_json()
        enrollment = Enrollment.query.get_or_404(enroll_id)
        enrollment.student_id = data.get('student_id', enrollment.student_id)
        enrollment.course_id = data.get('course_id', enrollment.course_id)
        db.session.commit()
        return jsonify({'message': 'Enrollment updated'})

    # Delete an enrollment
    @app.route('/enrollments/<int:enroll_id>', methods=['DELETE'])
    def delete_enrollment(enroll_id):
        enrollment = Enrollment.query.get_or_404(enroll_id)
        db.session.delete(enrollment)
        db.session.commit()
        return jsonify({'message': 'Enrollment deleted'})
