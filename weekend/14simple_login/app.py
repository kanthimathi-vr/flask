from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        return redirect(url_for('welcome', user=username))
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    username = request.args.get('user', 'Guest')
    return render_template('welcome.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
