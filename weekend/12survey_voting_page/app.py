from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        vote = request.form.get('vote')
        return redirect(url_for('thank_you', choice=vote))
    return render_template('survey.html')

@app.route('/thank-you')
def thank_you():
    choice = request.args.get('choice', 'None')
    return render_template('thank_you.html', choice=choice)

if __name__ == '__main__':
    app.run(debug=True)
