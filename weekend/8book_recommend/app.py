from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample book recommendations by genre
book_data = {
    "fiction": ["The Great Gatsby", "To Kill a Mockingbird", "The Catcher in the Rye"],
    "mystery": ["Gone Girl", "The Girl with the Dragon Tattoo", "In the Woods"],
    "fantasy": ["Harry Potter", "The Hobbit", "Mistborn"],
    "sci-fi": ["Dune", "Neuromancer", "Ender's Game"],
    "romance": ["Pride and Prejudice", "Me Before You", "The Notebook"]
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        genre = request.form.get('genre')
        return redirect(url_for('books', genre=genre.lower()))
    return render_template('index.html')

@app.route('/books/<genre>')
def books(genre):
    recommendations = book_data.get(genre.lower(), [])
    return render_template('books.html', genre=genre.capitalize(), books=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
