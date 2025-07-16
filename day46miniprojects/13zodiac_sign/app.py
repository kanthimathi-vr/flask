from flask import Flask

app = Flask(__name__)

# Dummy zodiac logic based on month only (not real astrology)
def get_zodiac_sign(month):
    signs = {
        1: "Capricorn ♑",
        2: "Aquarius ♒",
        3: "Pisces ♓",
        4: "Aries ♈",
        5: "Taurus ♉",
        6: "Gemini ♊",
        7: "Cancer ♋",
        8: "Leo ♌",
        9: "Virgo ♍",
        10: "Libra ♎",
        11: "Scorpio ♏",
        12: "Sagittarius ♐"
    }
    return signs.get(month, "Unknown")

@app.route('/')
def home():
    return "<h1>zodiac sign</h1>"
# Route: /zodiac/<date>
@app.route('/zodiac/<date>')
def zodiac(date):
    try:
        year, month, day = date.split('-')
        month = int(month)
        day = int(day)
        sign = get_zodiac_sign(month)
        return f"""
        <html>
            <body style="font-family: Arial; text-align: center; margin-top: 50px;">
                <h2>Your Zodiac Sign</h2>
                <hr>
                <p><strong>Date Entered:</strong> {date}</p>
                <p><strong>Zodiac Sign:</strong> <i>{sign}</i></p>
                <hr>
                <p><a href="/zodiac/help">Need Help?</a></p>
            </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
            <body style="font-family: Arial; text-align: center; margin-top: 50px;">
                <h3>⚠️ Error processing date</h3>
                <p>Make sure you enter it in <strong>YYYY-MM-DD</strong> format.</p>
                <p><a href="/zodiac/help">Go to Help</a></p>
            </body>
        </html>
        """

# Route: /zodiac/help
@app.route('/zodiac/help')
def zodiac_help():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>📅 Zodiac Sign Help</h2>
            <hr>
            <p>To get your zodiac sign, visit:</p>
            <p><strong>/zodiac/YYYY-MM-DD</strong></p>
            <p><i>Example: /zodiac/2000-12-25</i></p>
            <hr>
        </body>
    </html>
    """

# Run the app
if __name__ == '__main__':
    print("🔮 Zodiac Sign Generator running on http://127.0.0.1:5000")
    app.run(debug=True)
