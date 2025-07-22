from flask import Flask, render_template, request, redirect, url_for
from forms import UserForm

app = Flask(__name__)
app.secret_key = 'supersecretkey' 
# csrf protection 

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    
    # Pre-fill default values
    if request.method == 'GET':
        form.name.data = 'John Doe'
        form.country.data = 'us'
        form.number.data = 42
        form.gender.data = 'male'
        form.message.data = "Enter your message here..."

    if form.validate_on_submit():
        # task2: Print to console
        print("Name:", form.name.data)
        print("Email:", form.email.data)
        print("Message:", form.message.data)

        print("Gender:", form.gender.data)
        print("Country:", form.country.data)
        print("Terms Accepted:", form.terms.data)
        print("Password:", form.password.data)
        print("Confirm Password:", form.confirm_password.data)
        print("Date:", form.date.data)
        print("Number:", form.number.data)

        # Redirect to success page
        return render_template('result.html', form=form)

    return render_template('form.html', form=form)

@app.route('/success')
def success():
    return render_template("success.html")


if __name__ =='__main__':
    app.run(debug=True)