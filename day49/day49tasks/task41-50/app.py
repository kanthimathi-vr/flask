from flask import Flask, render_template, request, redirect, flash
from forms import UserForm

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            flash("Form submitted successfully!", "success")
            return redirect('/success')
        else:
            flash("There were errors in your submission.", "error")

            # 🐞 Log errors to terminal
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"[ERROR] {field}: {error}")

    return render_template('form.html', form=form)

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
