#  digital_card
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
        <html>
        <body>
        <h1>Kanthimathi</h1>
        <p>Email: mathi@gmail.com</p>
        <p>Phone: 9876543821</p>
        </body>
        </html>

    """
# About page
@app.route('/about')
def about():
    return """
    <html>
        <body>
            <h2>About Me</h2>
            <p>I am a software engineer with a passion for backend development, Flask, and API design.</p>
        </body>
    </html>
    """
# Skills route with dynamic name
@app.route('/skills/<name>')
def skills(name):
    skills_data = {
        'mathi': ['Python', 'Flask', 'Docker'],
        'john': ['JavaScript', 'React', 'Node.js'],
        'alice': ['HTML', 'CSS', 'UX Design']
    }

    skills_list = skills_data.get(name.lower())
    
    if not skills_list:
        return f"<h3>No skills found for {name.title()}.</h3>"

    html_skills = "<ul>" + "".join(f"<li>{skill}</li>" for skill in skills_list) + "</ul>"
    return f"<h3>Skills for {name.title()}:</h3>{html_skills}"

if __name__ == '__main__':
    app.run(debug=True)











