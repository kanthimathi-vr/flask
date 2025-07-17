from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# In-memory donation records
donations = []

# HTML donation form
donation_form = """
<h2>Make a Donation</h2>
<form action="/donate-confirm" method="post">
  Name: <input type="text" name="name" required><br><br>
  Amount (USD): <input type="number" name="amount" min="1" required><br><br>
  Purpose:
  <select name="purpose" required>
    <option value="education">Education</option>
    <option value="healthcare">Healthcare</option>
    <option value="environment">Environment</option>
  </select><br><br>
  <input type="submit" value="Donate">
</form>
"""

@app.route('/donate')
def donate():
    return render_template_string(donation_form)

@app.route('/donate-confirm', methods=['POST'])
def donate_confirm():
    name = request.form['name']
    amount = request.form['amount']
    purpose = request.form['purpose']

    # Save the donation
    donations.append({
        'name': name,
        'amount': float(amount),
        'purpose': purpose
    })

    # Redirect to thank-you page
    return redirect(url_for('thank_donor', name=name))

@app.route('/thank-donor/<name>')
def thank_donor(name):
    return f"<h3>Thank you, {name}, for your generous donation!</h3><a href='/donate'>Make another donation</a>"

@app.route('/donations')
def list_donations():
    purpose_filter = request.args.get('purpose')
    if purpose_filter:
        filtered = [d for d in donations if d['purpose'] == purpose_filter]
    else:
        filtered = donations

    html = f"<h2>Donations {'for ' + purpose_filter.title() if purpose_filter else ''}</h2><ul>"
    for d in filtered:
        html += f"<li>{d['name']} donated ${d['amount']} for {d['purpose']}</li>"
    html += "</ul><a href='/donate'>Donate again</a>"
    return html

if __name__ == '__main__':
    app.run(debug=True)
