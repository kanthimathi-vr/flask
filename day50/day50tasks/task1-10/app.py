from flask import Flask, jsonify
from config import Config
from models import db, Test
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def index():
    try:
        db.create_all()
        return jsonify({'message': 'MySQL connected, tables created'})
    except OperationalError as e:
        return jsonify({'error': 'Database connection failed', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
