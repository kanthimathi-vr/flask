# 13. Book Recommendation System
# Requirements:
# - /recommend: GET form with genre (sci-fi, romance)
# - POST to /show-recommendation
# - Redirect to /thanks/<user>
# - /books?genre=sci-fi to filter results
# - Use request.form and dynamic /book/<title> route


from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# Sample book database (normally from a real database)
books = [
    {'title': 'Dune', 'genre': 'sci-fi'},
    {'title': 'Neuromancer', 'genre': 'sci-fi'},
    {'title': 'Pride and Prejudice', 'genre': 'romance'},
    {'title': 'The Notebook', 'genre': 'romance'},
    {'title': 'Foundation', 'genre': 'sci-fi'},
    {'title': 'Me Before You', 'genre': 'romance'}
]

# Form HTML
recommend_form = """
<h2>Get a Book Recommendation</h2>
<form action="/show-recommendation" method="post">
  Your Name: <input type="text" name="user" required><br><br>
  Select Genre:
  <select name="genre" required>
    <option value="sci-fi">Science Fiction</option>
    <option value="romance">Romance</option>
  </select><br><br>
  <input type="submit" value="Recommend">
</form>
"""

@app.route('/recommend')
def recommend():
    return render_template_string(recommend_form)

@app.route('/show-recommendation', methods=['POST'])
def show_recommendation():
    user = request.form.get('user')
    genre = request.form.get('genre')

    # Optionally store or process this info here

    return redirect(url_for('thanks', user=user))

@app.route('/thanks/<user>')
def thanks(user):
    return f"<h3>Thank you, {user}! Check out our <a href='/books'>book list</a>.</h3>"

@app.route('/books')
def list_books():
    genre_filter = request.args.get('genre')
    if genre_filter:
        filtered = [book for book in books if book['genre'] == genre_filter]
    else:
        filtered = books

    html = "<h2>Recommended Books</h2><ul>"
    for book in filtered:
        html += f"<li><a href='/book/{book['title'].replace(' ', '%20')}'>{book['title']} ({book['genre']})</a></li>"
    html += "</ul><a href='/recommend'>Back to Recommend</a>"
    return html

@app.route('/book/<title>')
def book_detail(title):
    # Convert back from URL-safe title
    title = title.replace('%20', ' ')
    book = next((b for b in books if b['title'].lower() == title.lower()), None)
    if not book:
        return f"<h3>No book found with title '{title}'</h3>", 404
    return f"<h2>{book['title']}</h2><p>Genre: {book['genre'].title()}</p>"

if __name__ == '__main__':
    app.run(debug=True)
