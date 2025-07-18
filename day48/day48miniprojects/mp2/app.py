from flask import Flask, render_template

app = Flask(__name__)

@app.route("/books")
def books():
    # Example list of books; each with name, author, and image filename
    books = [
        {"name": "The Great Gatsby", "author": "F. Scott Fitzgerald", "cover": "book1.jpg"},
        {"name": "1984", "author": "George Orwell", "cover": "book2.jpg"},
        {"name": "To Kill a Mockingbird", "author": "Harper Lee", "cover": "book3.jpg"},
    ]

    # For testing "No books" message, set books = [] below
    # books = []

    return render_template("books.html", title="Online Book Showcase", books=books)

if __name__ == "__main__":
    app.run(debug=True)
