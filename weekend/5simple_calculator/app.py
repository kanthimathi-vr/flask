from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    num1 = request.form.get('num1')
    num2 = request.form.get('num2')
    operation = request.form.get('operation')

    error = None
    result = None

    try:
        n1 = float(num1)
        n2 = float(num2)
    except (ValueError, TypeError):
        error = "Please enter valid numbers."
        return render_template('calculator.html', error=error)

    if operation == 'add':
        result = n1 + n2
    elif operation == 'subtract':
        result = n1 - n2
    elif operation == 'multiply':
        result = n1 * n2
    elif operation == 'divide':
        if n2 == 0:
            error = "Cannot divide by zero."
        else:
            result = n1 / n2
    else:
        error = "Invalid operation selected."

    return render_template('calculator.html', result=result, error=error, num1=num1, num2=num2, operation=operation)


if __name__ == '__main__':
    app.run(debug=True)
