from flask import Flask

app = Flask(__name__)

# Home route: shows usage information
@app.route('/')
def usage_info():
    return (
        "Welcome to the BMI Calculator!<br><br>"
        "Usage:<br>"
        "/bmi/&lt;weight_kg&gt;/&lt;height_m&gt;<br><br>"
        "Example: <a href='/bmi/70/1.75'>/bmi/70/1.75</a>"
    )

# BMI calculation route
@app.route('/bmi/<weight>/<height>')
def calculate_bmi(weight, height):
    try:
        weight = float(weight)
        height = float(height)
        bmi = round(weight / (height ** 2), 2)

        # BMI Category
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obesity"

        return (
            f"Weight: {weight} kg<br>"
            f"Height: {height} m<br>"
            f"<b>Your BMI is: {bmi}</b><br>"
            f"Category: <b>{category}</b>"
        )

    except ValueError:
        return "❌ Please enter numeric values for weight and height."

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
