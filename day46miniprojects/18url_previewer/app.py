from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return """
        <h1 style= "background-color:purple; color:white; text-align: center;padding:3%;" >Url sample Previewer</h1>
        """


@app.route('/preview/<site>')
def site_preview(site):
    # Convert input to lowercase for consistent handling
    site = site.lower()
    
    # Dictionary of dummy preview texts
    previews = {
        'google': 'Search the world’s information with Google.',
        'youtube': 'Watch and share videos on YouTube.',
        'facebook': 'Connect with friends and the world on Facebook.',
        'twitter': 'See what’s happening right now on Twitter.',
        'linkedin': 'Build your professional network with LinkedIn.'
    }

    # Use default if site not in previews
    preview_text = previews.get(site, f"This is a preview of {site}.com website.")

    return f"""
    <html>
        <head>
            <title>🔍 Preview: {site}.com</title>
            <style>
                body {{
                    font-family: 'Segoe UI', sans-serif;
                    background-color: #f9f9f9;
                    text-align: center;
                    padding: 50px;
                }}
                .preview-box {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    display: inline-block;
                    width: 60%;
                }}
                h1 {{
                    color: #2c3e50;
                    margin-bottom: 10px;
                }}
                p {{
                    font-size: 18px;
                    color: #555;
                }}
                hr {{
                    margin: 20px 0;
                    border: 0;
                    height: 1px;
                    background: #ddd;
                }}
            </style>
        </head>
        <body>
            <div class="preview-box">
                <h1>🔗 {site.capitalize()}.com</h1>
                <hr>
                <p>{preview_text}</p>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    print("🔍 URL Previewer running at http://127.0.0.1:5000")
    app.run(debug=True)
