

# 6. Travel Booking Enquiry
'''
Requirements:
- /booking: Form with name, destination, and travel date
- On submit, redirect to /booking/confirm/<name>
- /deals?destination=paris to filter query results
- Use POST for data submission and dynamic URL for confirmation
'''


from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)


deals = [
    {'destination': 'paris', 'price': '$899', 'nights': 4},
    {'destination': 'london', 'price': '$799', 'nights': 3},
    {'destination': 'rome', 'price': '$699', 'nights': 3},
    {'destination': 'paris', 'price': '$999', 'nights': 5}
]


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form.get('name')
        destination = request.form.get('destination')
        date = request.form.get('travel_date')

        print(f"[Booking Received] Name: {name}, Destination: {destination}, Date: {date}")
        return redirect(url_for('booking_confirm', name=name))
    
    
    return '''
    <h2>Travel Booking Enquiry</h2>
    <form method="POST">
        Name: <input type="text" name="name" required><br><br>
        Destination:
        <select name="destination" required>
            <option value="paris">Paris</option>
            <option value="london">London</option>
            <option value="rome">Rome</option>
        </select><br><br>
        Travel Date: <input type="date" name="travel_date" required><br><br>
        <input type="submit" value="Submit Enquiry">
    </form>
    '''


@app.route('/booking/confirm/<name>')
def booking_confirm(name):
    return f"<h3>Thank you, {name.title()}! Your travel enquiry has been received.</h3>"


@app.route('/deals')
def show_deals():
    dest = request.args.get('destination')
    if not dest:
        return "<p>Please use <code>?destination=paris</code> to filter travel deals.</p>"

    matched_deals = [d for d in deals if d['destination'].lower() == dest.lower()]
    if not matched_deals:
        return f"<p>No deals found for destination: {dest}</p>"

    html = f"<h3>Deals for {dest.title()}:</h3><ul>"
    for d in matched_deals:
        html += f"<li>{d['nights']} nights - {d['price']}</li>"
    html += "</ul>"
    return html


if __name__ == '__main__':
    app.run(debug=True)