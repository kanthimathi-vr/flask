
# 4. Simple Online Poll
'''
Requirements:
- /poll: Show a form to vote for options A, B, or C (POST)
- /vote: Read and store using request.form, redirect to /result
- /result?option=A – filter vote count by query param
- /voter/<name> – show user’s selected vote
'''

from flask import Flask, request, redirect, url_for

app = Flask(__name__)


votes = []  

@app.route('/poll', methods=['GET'])
def poll_form():
    return '''
    <h2>Vote in Our Poll</h2>
    <form method="POST" action="/vote">
        Name: <input type="text" name="name" required><br><br>
        Choose an option:<br>
        <input type="radio" name="option" value="A" required> Option A<br>
        <input type="radio" name="option" value="B"> Option B<br>
        <input type="radio" name="option" value="C"> Option C<br><br>
        <input type="submit" value="Vote">
    </form>
    '''


@app.route('/vote', methods=['POST'])
def vote():
    name = request.form.get('name', '').strip()
    option = request.form.get('option', '').strip()

    
    votes.append({'name': name, 'option': option})

    return redirect(url_for('result'))


@app.route('/result')
def result():
    option = request.args.get('option')
    if not option:
        return "<p>Please provide an option (?option=A, B, or C).</p>"

    count = sum(1 for v in votes if v['option'].upper() == option.upper())
    return f"<h3>Total votes for Option {option.upper()}: {count}</h3>"


@app.route('/voter/<name>')
def voter_result(name):
    user_votes = [v for v in votes if v['name'].lower() == name.lower()]
    if not user_votes:
        return f"<h3>No vote found for {name.title()}</h3>"
    
    last_vote = user_votes[-1]
    return f"<h3>{name.title()} voted for Option {last_vote['option'].upper()}</h3>"


if __name__ == '__main__':
    app.run(debug=True)
