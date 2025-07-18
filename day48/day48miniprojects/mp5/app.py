from flask import Flask, render_template

app = Flask(__name__)

@app.route("/jobs")
def jobs():
    jobs_list = [
        {
            "title": "Frontend Developer",
            "company": "TechCorp",
            "location": "New York, NY",
            "remote": True,
            "logo": "images/company1.png"
        },
        {
            "title": "Data Scientist",
            "company": "DataWorks",
            "location": "San Francisco, CA",
            "remote": False,
            "logo": "images/company2.png"
        },
        {
            "title": "Product Manager",
            "company": "Innovate Inc.",
            "location": "Remote",
            "remote": True,
            "logo": "images/company3.png"
        },
    ]
    return render_template("jobs.html", title="Job Listings", jobs=jobs_list)

if __name__ == "__main__":
    app.run(debug=True)
