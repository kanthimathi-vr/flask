from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Word Counter</h1>"
# Route: Count words in a given string
@app.route('/wordcount/<text>')
def word_count(text):
    words = text.split()
    count = len(words)
    
    return f"""
    <html>
        <head>
            <title>Word Counter</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    padding: 40px;
                    text-align: center;
                }}
                .result {{
                    background: #e0f7fa;
                    border: 1px solid #00acc1;
                    border-radius: 10px;
                    padding: 20px;
                    display: inline-block;
                }}
            </style>
        </head>
        <body>
            <div class="result">
                <h2>🔤 Word Counter</h2>
                <p><strong>Input:</strong> {text}</p>
                <p><strong>Word Count:</strong> {count}</p>
            </div>
            <p><a href="/wordcount/help">Need Help?</a></p>
        </body>
    </html>
    """

# Route: Help Page
@app.route('/wordcount/help')
def word_count_help():
    return """
    <html>
        <head>
            <title>Word Count Help</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #fffbe6;
                    padding: 40px;
                    text-align: center;
                }
                .help-box {
                    border: 1px solid #fdd835;
                    background-color: #fff9c4;
                    padding: 20px;
                    border-radius: 8px;
                    display: inline-block;
                }
            </style>
        </head>
        <body>
            <div class="help-box">
                <h2>📘 How to Use Word Counter</h2>
                <p>Use the URL format: <strong>/wordcount/your+text+goes+here</strong></p>
                <p>Words are counted by spaces in the input.</p>
                <p><i>Example:</i> /wordcount/this+is+a+test</p>
            </div>
        </body>
    </html>
    """

# Run app with debug mode
if __name__ == '__main__':
    print("🧮 Word Counter App running at http://127.0.0.1:5000")
    app.run(debug=True)
