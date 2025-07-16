from flask import Flask

app = Flask(__name__)

# Sample data (can be extended)
portfolio_data = {
    "mathi": {
        "skills": ["Python", "Flask", "HTML", "CSS"],
        "projects": [
            {"title": "Blog Website", "desc": "A personal blog using Flask"},
            {"title": "ToDo App", "desc": "Task tracker with SQLite"},
        ]
    },
    "rani": {
        "skills": ["JavaScript", "React", "Node.js"],
        "projects": [
            {"title": "Weather App", "desc": "Fetches weather using APIs"},
            {"title": "Chat App", "desc": "Real-time chat using Socket.IO"},
        ]
    }
}
@app.route('/')
def home():
    return "<h1><b>Static Portfolio</b></h1>"

# 🔹 Route 1: Profile Page
@app.route('/portfolio/<name>')
def profile(name):
    name = name.lower()
    if name not in portfolio_data:
        return f"<h3>No profile found for {name.title()}.</h3>"
    
    return f"""
    <html>
        <body>
            <h1>{name.title()}'s Portfolio</h1>
            <p>Welcome to the static profile page of {name.title()}.</p>
            <p>Visit <a href="/portfolio/{name}/skills">Skills</a> | 
            <a href="/portfolio/{name}/projects">Projects</a></p>
        </body>
    </html>
    """

# 🔹 Route 2: Skills Page (List)
@app.route('/portfolio/<name>/skills')
def skills(name):
    name = name.lower()
    if name not in portfolio_data:
        return f"<h3>No profile found for {name.title()}.</h3>"
    
    skills_list = portfolio_data[name]["skills"]
    skill_items = "".join(f"<li>{skill}</li>" for skill in skills_list)
    
    return f"""
    <html>
        <body>
            <h2>{name.title()}'s Skills</h2>
            <ul>{skill_items}</ul>
            <a href="/portfolio/{name}">← Back to Profile</a>
        </body>
    </html>
    """

# 🔹 Route 3: Projects Page (Table)
@app.route('/portfolio/<name>/projects')
def projects(name):
    name = name.lower()
    if name not in portfolio_data:
        return f"<h3>No profile found for {name.title()}.</h3>"

    project_rows = "".join(
        f"<tr><td>{proj['title']}</td><td>{proj['desc']}</td></tr>"
        for proj in portfolio_data[name]["projects"]
    )

    return f"""
    <html>
        <body>
            <h2>{name.title()}'s Projects</h2>
            <table border="1" cellpadding="8">
                <tr><th>Title</th><th>Description</th></tr>
                {project_rows}
            </table>
            <br>
            <a href="/portfolio/{name}">← Back to Profile</a>
        </body>
    </html>
    """

# Run with debug mode
if __name__ == '__main__':
    app.run(debug=True)
