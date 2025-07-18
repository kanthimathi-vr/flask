from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
feedback_list = []

@app.route('/')
def feedback_form():
    return render_template('feedback_form.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    comments = request.form['comments']
    feedback_list.append({'name': name, 'comments': comments})
    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/all-feedback')
def all_feedback():
    return render_template('all_feedback.html', feedback=feedback_list)

if __name__ == '__main__':
    app.run(debug=True)
