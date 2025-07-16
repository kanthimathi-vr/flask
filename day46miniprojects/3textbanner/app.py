from flask import Flask

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return """
    <html>
        <body>
            <h2>Enter your banner text</h2>
            <p>Try this: <a href="/banner/Hello">/banner/Hello</a></p>
        </body>
    </html>
    """
# Banner route with default <h1>
@app.route('/banner/<text>')
def banner(text):
    return f"""
    <html>
        <body>
            <h1>{text}</h1>
        </body>
    </html>
    """
# Banner route with variable heading size
@app.route('/banner/<text>/<size>')
def banner_with_size(text, size):
    size = size.lower()
    if size not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        return f"<p>Invalid heading size: {size}. Use h1 to h6 only.</p>"

    return f"""
    <html>
        <body>
            <{size}>{text}</{size}>
        </body>
    </html>
    """

# Run the app
if __name__ == '__main__':
    app.run(debug=True)




