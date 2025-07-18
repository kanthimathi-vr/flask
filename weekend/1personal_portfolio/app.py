from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
profiles = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    skills = request.form['skills']
    bio = request.form['bio']
    
    profiles[name] = {
        'name': name,
        'skills': [s.strip() for s in skills.split(',')],
        'bio': bio
    }
    return redirect(url_for('profile', name=name))

@app.route('/profile/<name>')
def profile(name):
    user = profiles.get(name)
    if user:
        return render_template('profile.html', user=user)
    return "Profile not found", 404

if __name__ == '__main__':
    app.run(debug=True)
