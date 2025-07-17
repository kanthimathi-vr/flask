

# 18. Newsletter Subscription
'''
Requirements:
- /subscribe: GET form with name, email
- On POST, redirect to /thanks/<name>
- /subscribers?month=July shows filtered data
- Display confirmation using dynamic routing and url_for()
'''


from flask import Flask, request, redirect, url_for

app = Flask(__name__)


subscribers = []


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        month = request.form.get('month')

        
        subscribers.append({'name': name, 'email': email, 'month': month})
        
      
        return redirect(url_for('thanks', name=name))
    
    return '''
    <h2>Newsletter Subscription</h2>
    <form method="POST">
        Name: <input type="text" name="name" required><br><br>
        Email: <input type="email" name="email" required><br><br>
        Subscription Month:
        <select name="month" required>
            <option value="July">July</option>
            <option value="August">August</option>
            <option value="September">September</option>
        </select><br><br>
        <input type="submit" value="Subscribe">
    </form>
    '''

@app.route('/thanks/<name>')
def thanks(name):
    return f'''
    <h3>Thank you, {name.title()}!</h3>
    <p>You have successfully subscribed to our newsletter. 🎉</p>
    <p><a href="{url_for('view_subscribers')}">View all subscribers</a></p>
    '''


@app.route('/subscribers')
def view_subscribers():
    month_filter = request.args.get('month')
    if month_filter:
        filtered = [s for s in subscribers if s['month'].lower() == month_filter.lower()]
    else:
        filtered = subscribers

    if not filtered:
        return "<p>No subscribers found.</p>"

    html = f"<h3>Subscribers{' for ' + month_filter if month_filter else ''}</h3><ul>"
    for s in filtered:
        html += f"<li>{s['name']} – {s['email']} (Month: {s['month']})</li>"
    html += "</ul>"
    return html


if __name__ == '__main__':
    app.run(debug=True)

