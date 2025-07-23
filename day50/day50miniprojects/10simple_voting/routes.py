from flask import request, jsonify
from models import db, Candidate, Vote

def register_routes(app):

    # Add a new candidate
    @app.route('/candidates', methods=['POST'])
    def add_candidate():
        data = request.get_json()
        candidate = Candidate(name=data['name'], party=data['party'])
        db.session.add(candidate)
        db.session.commit()
        return jsonify({'message': 'Candidate added', 'id': candidate.id}), 201

    # View all candidates
    @app.route('/candidates', methods=['GET'])
    def get_candidates():
        candidates = Candidate.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'party': c.party
        } for c in candidates])

    # Cast a vote
    @app.route('/vote', methods=['POST'])
    def cast_vote():
        data = request.get_json()
        voter_name = data.get('voter_name')
        candidate_id = data.get('candidate_id')

        # Check for duplicate voting
        if Vote.query.filter_by(voter_name=voter_name).first():
            return jsonify({'error': 'Voter has already voted'}), 400

        # Check if candidate exists
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Invalid candidate'}), 404

        vote = Vote(voter_name=voter_name, candidate_id=candidate_id)
        db.session.add(vote)
        db.session.commit()
        return jsonify({'message': 'Vote cast successfully'}), 201

    # View vote count per candidate
    @app.route('/results', methods=['GET'])
    def view_results():
        candidates = Candidate.query.all()
        results = []
        for c in candidates:
            count = Vote.query.filter_by(candidate_id=c.id).count()
            results.append({
                'candidate_id': c.id,
                'name': c.name,
                'party': c.party,
                'votes': count
            })
        return jsonify(results)
