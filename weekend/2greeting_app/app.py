from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

def get_time_based_greeting():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return 'morning'
    elif current_hour < 17:
        return 'afternoon'
    else:
        return 'evening'

motivational_quotes = {
    'morning': "Every morning is a chance to start anew. Make it count!",
    'afternoon': "Keep pushing — you're halfway to greatness!",
    'evening': "Reflect. Recharge. Get ready to conquer tomorrow!"
}

greetings_by_language = {
    'en': {'morning': 'Good morning', 'afternoon': 'Good afternoon', 'evening': 'Good evening'},
    'es': {'morning': 'Buenos días', 'afternoon': 'Buenas tardes', 'evening': 'Buenas noches'},
    'fr': {'morning': 'Bonjour', 'afternoon': 'Bon après-midi', 'evening': 'Bonsoir'},
    'de': {'morning': 'Guten Morgen', 'afternoon': 'Guten Tag', 'evening': 'Guten Abend'},
    'hi': {'morning': 'सुप्रभात', 'afternoon': 'नमस्कार', 'evening': 'शुभ संध्या'}
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/greet/<name>')
def greet(name):
    lang = request.args.get('lang', 'en').lower()
    time_of_day = get_time_based_greeting()
    greeting_dict = greetings_by_language.get(lang, greetings_by_language['en'])
    greeting = greeting_dict[time_of_day]
    quote = motivational_quotes[time_of_day]

    return render_template(
        'greet.html',
        name=name,
        greeting=greeting,
        quote=quote,
        time_of_day=time_of_day.capitalize()
    )

if __name__ == '__main__':
    app.run(debug=True)
