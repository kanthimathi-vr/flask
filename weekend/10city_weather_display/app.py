from flask import Flask, render_template, request

app = Flask(__name__)

# Static simulated weather data
weather_data = {
    "paris": {"condition": "sunny", "temp_c": 25},
    "london": {"condition": "rainy", "temp_c": 17},
    "newyork": {"condition": "cloudy", "temp_c": 22},
    "moscow": {"condition": "snow", "temp_c": -3}
}

@app.route('/weather/<city>')
def weather(city):
    city_lower = city.lower()
    unit = request.args.get('unit', 'celsius')
    data = weather_data.get(city_lower)

    if not data:
        return f"<h2>Weather for '{city}' not found.</h2>"

    temp = data['temp_c']
    if unit == 'fahrenheit':
        temp = round((temp * 9/5) + 32)
        unit_symbol = "°F"
    else:
        unit_symbol = "°C"

    return render_template("weather.html", city=city.title(), temp=temp, unit=unit_symbol, condition=data["condition"])

if __name__ == '__main__':
    app.run(debug=True)
