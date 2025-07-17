

# 19. Weather Report Generator
'''
Requirements:
- /weather: GET form with city name
- Submit to /weather-result (POST)
- Redirect to /weather/<city> (dynamic)
- Support query string: /weather?unit=metric
'''

from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# Dummy weather data (simulate real API)
weather_data = {
    'london': {'temp_c': 15, 'temp_f': 59, 'desc': 'Cloudy'},
    'paris': {'temp_c': 20, 'temp_f': 68, 'desc': 'Sunny'},
    'new york': {'temp_c': 25, 'temp_f': 77, 'desc': 'Rainy'},
}

@app.route('/weather', methods=['GET'])
def weather_form():
    unit = request.args.get('unit', 'metric')  # default to metric
    return f'''
    <h2>Weather Report Generator</h2>
    <form action="/weather-result" method="POST">
        City: <input type="text" name="city" required><br><br>
        <label>Unit:</label>
        <select name="unit">
            <option value="metric" {"selected" if unit == "metric" else ""}>Metric (°C)</option>
            <option value="imperial" {"selected" if unit == "imperial" else ""}>Imperial (°F)</option>
        </select><br><br>
        <input type="submit" value="Get Weather">
    </form>
    '''

@app.route('/weather-result', methods=['POST'])
def weather_result():
    city = request.form.get('city').lower()
    unit = request.form.get('unit', 'metric')
    return redirect(url_for('weather_city', city=city, unit=unit))

@app.route('/weather/<city>')
def weather_city(city):
    unit = request.args.get('unit', 'metric')
    city_lower = city.lower()
    data = weather_data.get(city_lower)

    if not data:
        return f"<h3>Sorry, weather data for '{city.title()}' is not available.</h3>"

    if unit == 'imperial':
        temp = data['temp_f']
        unit_symbol = '°F'
    else:
        temp = data['temp_c']
        unit_symbol = '°C'

    return f'''
    <h2>Weather in {city.title()}</h2>
    <p>Temperature: {temp} {unit_symbol}</p>
    <p>Condition: {data['desc']}</p>
    <p><a href="{url_for('weather_form', unit=unit)}">Check another city</a></p>
    '''

if __name__ == '__main__':
    app.run(debug=True)

