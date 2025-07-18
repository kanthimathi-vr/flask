from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    default_color = '#ff69b4'  # Hot Pink default
    color = default_color
    submitted = False

    if request.method == 'POST':
        color_input = request.form.get('color_input')
        if color_input:
            color = color_input.strip()
            submitted = True

    return render_template('index.html', color=color, submitted=submitted)

if __name__ == '__main__':
    app.run(debug=True)
