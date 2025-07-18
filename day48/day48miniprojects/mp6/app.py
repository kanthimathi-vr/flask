from flask import Flask, render_template

app = Flask(__name__)

@app.route("/movies")
def movies():
    movies_list = [
        {
            "title": "Inception",
            "poster": "images/movie1.jpg",
            "new_release": False,
            "rating": 4
        },
        {
            "title": "Dune",
            "poster": "images/movie2.jpg",
            "new_release": True,
            "rating": 5
        },
        {
            "title": "The Matrix Resurrections",
            "poster": "images/movie3.jpg",
            "new_release": True,
            "rating": 3
        },
    ]
    return render_template("movies.html", title="Recommended Movies", movies=movies_list)

if __name__ == "__main__":
    app.run(debug=True)
