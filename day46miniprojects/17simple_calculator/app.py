from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
        <h1 style= "background-color:purple; color:white; text-align: center;padding:3%;" >Simple calculator</h1>
        """


@app.route('/calc/<op>/<float:num1>/<float:num2>')
def calc(op, num1, num2):
    # Perform operation based on op
    if op == 'add':
        result = num1 + num2
        symbol = '+'
    elif op == 'sub':
        result = num1 - num2
        symbol = '-'
    elif op == 'mul':
        result = num1 * num2
        symbol = '×'
    elif op == 'div':
        if num2 == 0:
            return "<h2 style='color:red;'>🚫 Error: Division by zero is not allowed.</h2>"
        result = num1 / num2
        symbol = '÷'
    else:
        return """
        <h2 style="color:red;">❌ Invalid Operation</h2>
        <p>Please use <a href='/ops'>/ops</a> to see valid operations.</p>
        """

    return f"""
    <html>
        <head>
            <title>Simple Calculator</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f0f8ff;
                    text-align: center;
                    padding: 50px;
                }}
                .card {{
                    background-color: #ffffff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    display: inline-block;
                }}
                h2 {{
                    color: #2c3e50;
                }}
                .result {{
                    font-size: 24px;
                    color: #1abc9c;
                }}
                a {{
                    text-decoration: none;
                    color: #2980b9;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🧮 Simple Calculator</h2>
                <p class="result">{num1} {symbol} {num2} = <strong>{result}</strong></p>
                <hr>
                <p><a href="/ops">View Valid Operations</a></p>
            </div>
        </body>
    </html>
    """

@app.route('/ops')
def show_ops():
    return """
    <html>
        <head>
            <title>Calculator Operations</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    background-color: #fcf8e8;
                    padding: 40px;
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    margin: 10px 0;
                    font-size: 18px;
                }
            </style>
        </head>
        <body>
            <h2>✅ Valid Operations</h2>
            <ul>
                <li><b>add</b>: /calc/add/10/5 → 15</li>
                <li><b>sub</b>: /calc/sub/10/5 → 5</li>
                <li><b>mul</b>: /calc/mul/10/5 → 50</li>
                <li><b>div</b>: /calc/div/10/5 → 2</li>
            </ul>
            <p>Numbers can be integers or decimals.</p>
            <p>Example: <a href="/calc/add/12.5/7.3">/calc/add/12.5/7.3</a></p>
        </body>
    </html>
    """

if __name__ == '__main__':
    print("🧮 Calculator app running at http://127.0.0.1:5000")
    app.run(debug=True)
