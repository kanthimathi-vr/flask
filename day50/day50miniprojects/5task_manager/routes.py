from flask import request, jsonify
from models import db, Task
from datetime import datetime

def register_routes(app):

    @app.route('/tasks', methods=['POST'])
    def add_task():
        data = request.get_json()
        try:
            due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

        task = Task(
            title=data['title'],
            due_date=due_date
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully', 'id': task.id}), 201

    @app.route('/tasks', methods=['GET'])
    def view_tasks():
        tasks = Task.query.order_by(Task.due_date.asc()).all()
        return jsonify([
            {
                'id': t.id,
                'title': t.title,
                'is_done': t.is_done,
                'due_date': t.due_date.strftime('%Y-%m-%d')
            } for t in tasks
        ])

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task_status(task_id):
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        task.is_done = data.get('is_done', task.is_done)
        db.session.commit()
        return jsonify({'message': 'Task status updated'})

    @app.route('/tasks/completed', methods=['DELETE'])
    def delete_completed_tasks():
        completed_tasks = Task.query.filter_by(is_done=True).all()
        for task in completed_tasks:
            db.session.delete(task)
        db.session.commit()
        return jsonify({'message': f'{len(completed_tasks)} completed task(s) deleted'})
