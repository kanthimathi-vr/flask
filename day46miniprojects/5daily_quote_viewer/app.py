from flask import Flask
import datetime

app = Flask(__name__)

# Hardcoded quotes for each day
daily_quotes = {
    'monday':    "Start your week strong!",
    'tuesday':   "Keep going — you’re doing great!",
    'wednesday': "Halfway there. Stay focused!",
    'thursday':  "Push through — the weekend is near!",
    'friday':    "Finish strong and celebrate!",
    'saturday':  "Relax, recharge, and reflect.",
    'sunday':    "Prepare your mind for the week ahead."
}

# Inline CSS styling
QUOTE_STYLE = """
<style>
    body {{ font-family: Arial; background: #f5f5f5; padding: 40px; }}
    .quote-box {{
        background: #fff;
        padding: 20px;
        border-left: 5px solid #007BFF;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        width: 50%;
        margin: auto;
        text-align: center;
    }}
    h2 {{ color: #333; }}
</style>
"""

# Home route – show today's quote
@app.route('/')
def today_quote():
    day = datetime.datetime.now().strftime('%A').lower()
    quote = daily_quotes.get(day, "No quote available.")
    return f"""
    {QUOTE_STYLE}
    <div class="quote-box">
        <h2>Quote for {day.title()}:</h2>
        <p>{quote}</p>
    </div>
    """

# Route for any day's quote
@app.route('/quote/<day>')
def quote_by_day(day):
    day = day.lower()
    quote = daily_quotes.get(day)
    if not quote:
        return f"<p>❌ Invalid day: {day}. Use /quote/monday ... /quote/sunday.</p>"

    return f"""
    {QUOTE_STYLE}
    <div class="quote-box">
        <h2>Quote for {day.title()}:</h2>
        <p>{quote}</p>
    </div>
    """

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
