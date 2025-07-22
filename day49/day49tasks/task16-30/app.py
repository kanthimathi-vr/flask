from flask import Flask, render_template, request
from forms import UserForm

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        return render_template('result.html', form=form)
    error_count = len(form.errors)
    return render_template('form.html', form=form, error_count=error_count)

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ =='__main__':
    app.run(debug=True)