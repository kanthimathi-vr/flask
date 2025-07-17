

# 20. Movie Rating System
'''
Requirements:
- /rate: Form with name, movie title, and rating
- POST to /submit-rating, redirect to /thank-you/<name>
- /ratings?movie=Inception filters query
- /movie/<title> displays dynamic movie info
'''


from flask import Flask, request, redirect, url_for

app = Flask(__name__)


ratings = []


@app.route('/rate', methods=['GET', 'POST'])
def rate():
    if request.method == 'POST':
        name = request.form.get('name')
        movie = request.form.get('movie').title()
        rating = request.form.get('rating')

        
        ratings.append({'name': name, 'movie': movie, 'rating': rating})

        
        return redirect(url_for('thank_you', name=name))
    
    return '''
    <h2>Movie Rating</h2>
    <form method="POST">
        Name: <input type="text" name="name" required><br><br>
        Movie Title: <input type="text" name="movie" required><br><br>
        Rating (1-5): <input type="number" name="rating" min="1" max="5" required><br><br>
        <input type="submit" value="Submit Rating">
    </form>
    '''


@app.route('/thank-you/<name>')
def thank_you(name):
    return f'''
    <h3>Thanks for your rating, {name.title()}!</h3>
    <p><a href="{url_for('rate')}">Rate another movie</a></p>
    <p><a href="{url_for('view_ratings')}">View all ratings</a></p>
    '''


@app.route('/ratings')
def view_ratings():
    movie_filter = request.args.get('movie')
    if movie_filter:
        filtered = [r for r in ratings if r['movie'].lower() == movie_filter.lower()]
    else:
        filtered = ratings
    
    if not filtered:
        return "<p>No ratings found.</p>"

    html = "<h3>Movie Ratings</h3><ul>"
    for r in filtered:
        movie_link = url_for('movie_info', title=r['movie'])
        html += f"<li>{r['name']} rated <a href='{movie_link}'>{r['movie']}</a>: {r['rating']}/5</li>"
    html += "</ul>"
    return html


@app.route('/movie/<title>')
def movie_info(title):
    
    movies = {
        'Inception': {'year': 2010, 'genre': 'Sci-Fi', 'director': 'Christopher Nolan'},
        'Titanic': {'year': 1997, 'genre': 'Romance', 'director': 'James Cameron'},
        'Matrix': {'year': 1999, 'genre': 'Action', 'director': 'The Wachowskis'},
    }

    info = movies.get(title.title())
    if not info:
        return f"<h3>No info available for '{title.title()}'.</h3>"

    return f'''
    <h2>{title.title()}</h2>
    <ul>
        <li>Year: {info['year']}</li>
        <li>Genre: {info['genre']}</li>
        <li>Director: {info['director']}</li>
    </ul>
    <p><a href="{url_for('view_ratings', movie=title)}">See all ratings for this movie</a></p>
    '''

if __name__ == '__main__':
    app.run(debug=True)
