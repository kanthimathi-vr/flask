from flask import request, jsonify
from models import db, Employee

def register_routes(app):

    # Create employee
    @app.route('/employees', methods=['POST'])
    def add_employee():
        data = request.get_json()
        employee = Employee(
            name=data['name'],
            position=data['position'],
            department=data['department'],
            salary=data['salary']
        )
        db.session.add(employee)
        db.session.commit()
        return jsonify({'message': 'Employee added', 'id': employee.id}), 201

    # Read all employees or filter by department
    @app.route('/employees', methods=['GET'])
    def get_employees():
        department = request.args.get('department')
        if department:
            employees = Employee.query.filter_by(department=department).all()
        else:
            employees = Employee.query.all()
        return jsonify([{
            'id': e.id,
            'name': e.name,
            'position': e.position,
            'department': e.department,
            'salary': e.salary
        } for e in employees])

    # Read single employee
    @app.route('/employees/<int:emp_id>', methods=['GET'])
    def get_employee(emp_id):
        employee = Employee.query.get_or_404(emp_id)
        return jsonify({
            'id': employee.id,
            'name': employee.name,
            'position': employee.position,
            'department': employee.department,
            'salary': employee.salary
        })

    # Update employee
    @app.route('/employees/<int:emp_id>', methods=['PUT'])
    def update_employee(emp_id):
        employee = Employee.query.get_or_404(emp_id)
        data = request.get_json()

        employee.name = data.get('name', employee.name)
        employee.position = data.get('position', employee.position)
        employee.department = data.get('department', employee.department)
        employee.salary = data.get('salary', employee.salary)

        db.session.commit()
        return jsonify({'message': 'Employee updated'})

    # Delete employee
    @app.route('/employees/<int:emp_id>', methods=['DELETE'])
    def delete_employee(emp_id):
        employee = Employee.query.get_or_404(emp_id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted'})
