from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/poll', methods=['GET', 'POST'])
def poll():
    question = "Do you like Python?"
    options = ["Yes", "No", "Maybe"]

    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice not in options:
            choice = "Invalid choice"
        return redirect(url_for('result', choice=choice))
    return render_template('poll.html', question=question, options=options)

@app.route('/result')
def result():
    choice = request.args.get('choice', 'No response')
    return render_template('result.html', choice=choice)

if __name__ == '__main__':
    app.run(debug=True)
