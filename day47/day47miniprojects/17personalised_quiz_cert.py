
# 17. Personalized Quiz Certificate Generator
'''
Requirements:
- /quiz-form: Form to enter name and score
- On POST, redirect to /certificate/<name>/<score>
- Add filter route: /certificates?score=10
- Use url_for() in certificate link generation
'''


from flask import Flask, request, redirect, url_for

app = Flask(__name__)


certificates = []


@app.route('/quiz-form', methods=['GET', 'POST'])
def quiz_form():
    if request.method == 'POST':
        name = request.form.get('name')
        score = request.form.get('score')

        
        certificates.append({'name': name, 'score': score})

        return redirect(url_for('certificate', name=name, score=score))

    return '''
    <h2>Quiz Certificate Generator</h2>
    <form method="POST">
        Name: <input type="text" name="name" required><br><br>
        Score (0–10): <input type="number" name="score" min="0" max="10" required><br><br>
        <input type="submit" value="Generate Certificate">
    </form>
    '''


@app.route('/certificate/<name>/<score>')
def certificate(name, score):
    return f'''
    <div style="border: 2px solid #444; padding: 20px; width: 400px; margin: auto;">
        <h2 style="text-align: center;">Certificate of Achievement</h2>
        <p>This certificate is proudly presented to:</p>
        <h3>{name.title()}</h3>
        <p>For scoring <strong>{score}/10</strong> on the quiz.</p>
        <p style="text-align: center;">🎉 Congratulations! 🎉</p>
    </div>
    '''


@app.route('/certificates')
def filter_certificates():
    score_filter = request.args.get('score')
    filtered = certificates if not score_filter else [c for c in certificates if c['score'] == score_filter]

    if not filtered:
        return "<p>No certificates match the criteria.</p>"

    html = "<h3>Certificates</h3><ul>"
    for c in filtered:
        cert_link = url_for('certificate', name=c['name'], score=c['score'])
        html += f"<li>{c['name']} – Score: {c['score']} – <a href='{cert_link}'>View Certificate</a></li>"
    html += "</ul>"
    return html


if __name__ == '__main__':
    app.run(debug=True)
