from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Text_mirror</h1>"

@app.route('/mirror/<text>')
def mirror_text(text):
    reversed_text = text[::-1]
    text_length = len(text)

    return f"""
    <html>
        <head>
            <title>🔁 Text Mirror Tool</title>
            <style>
                body {{
                    font-family: Courier New, monospace;
                    text-align: center;
                    padding: 40px;
                    background-color: #f0f8ff;
                }}
                table {{
                    margin: auto;
                    border-collapse: collapse;
                    width: 60%;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 12px;
                    font-size: 16px;
                }}
                th {{
                    background-color: #e0f7fa;
                    color: #006064;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
            </style>
        </head>
        <body>
            <h2>🔁 Text Mirror Tool</h2>
            <pre>
Original : {text}
Reversed : {reversed_text}
Length   : {text_length}
            </pre>
            <br><hr><br>
            <table>
                <tr>
                    <th>Original Text</th>
                    <th>Reversed Text</th>
                    <th>Length</th>
                </tr>
                <tr>
                    <td>{text}</td>
                    <td>{reversed_text}</td>
                    <td>{text_length}</td>
                </tr>
            </table>
        </body>
    </html>
    """

# Run the Flask app
if __name__ == '__main__':
    print("🔁 Text Mirror Tool running at http://127.0.0.1:5000")
    app.run(debug=True)
