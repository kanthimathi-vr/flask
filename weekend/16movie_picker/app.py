from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample movie database
movies_by_genre = {
    "action": ["Mad Max: Fury Road", "John Wick", "Die Hard"],
    "comedy": ["The Hangover", "Superbad", "Step Brothers"],
    "drama": ["The Shawshank Redemption", "Forrest Gump", "The Godfather"],
    "sci-fi": ["Interstellar", "Inception", "The Matrix"],
    "horror": ["The Conjuring", "Get Out", "A Quiet Place"]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    genres = list(movies_by_genre.keys())
    if request.method == 'POST':
        selected_genre = request.form.get('genre')
        return redirect(url_for('movies', genre=selected_genre))
    return render_template('index.html', genres=genres)

@app.route('/movies/<genre>')
def movies(genre):
    genre = genre.lower()
    movie_list = movies_by_genre.get(genre, [])
    return render_template('movies.html', genre=genre.title(), movies=movie_list)

if __name__ == '__main__':
    app.run(debug=True)
