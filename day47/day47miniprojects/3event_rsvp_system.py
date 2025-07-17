

# 3. Event RSVP System
'''
Requirements:
- /rsvp: GET form for name, email, and attending (yes/no)
- POST to /rsvp-confirm
- Redirect to /thank-you/<name> using url_for
- Add a route /guests?attending=yes to list all attendees
- Use dynamic parameter route to thank each guest personally
'''


from flask import Flask, request, redirect, url_for

app = Flask(__name__)


guest_list = []


@app.route('/rsvp', methods=['GET'])
def rsvp_form():
    return '''
    <h2>RSVP for the Event</h2>
    <form method="POST" action="/rsvp-confirm">
        Name: <input type="text" name="name" required><br><br>
        Email: <input type="email" name="email" required><br><br>
        Will you attend?
        <select name="attending">
            <option value="yes">Yes</option>
            <option value="no">No</option>
        </select><br><br>
        <input type="submit" value="Submit RSVP">
    </form>
    '''


@app.route('/rsvp-confirm', methods=['POST'])
def rsvp_confirm():
    name = request.form.get('name', 'Guest').strip()
    email = request.form.get('email', '').strip()
    attending = request.form.get('attending', 'no')

  
    guest_list.append({
        'name': name,
        'email': email,
        'attending': attending
    })

    
    return redirect(url_for('thank_you', name=name))


@app.route('/thank-you/<name>')
def thank_you(name):
    return f"<h3>Thank you, {name.title()}, for your RSVP!</h3>"


@app.route('/guests')
def show_guests():
    filter_attending = request.args.get('attending')
    if not filter_attending:
        return "<p>Please use <code>?attending=yes</code> or <code>?attending=no</code> to filter guests.</p>"

    filtered = [g for g in guest_list if g['attending'] == filter_attending.lower()]
    
    if not filtered:
        return f"<p>No guests found with attending = {filter_attending}</p>"

    html = f"<h3>Guest List - Attending: {filter_attending.capitalize()}</h3><ul>"
    for g in filtered:
        html += f"<li>{g['name']} ({g['email']})</li>"
    html += "</ul>"
    return html


if __name__ == '__main__':
    app.run(debug=True)
