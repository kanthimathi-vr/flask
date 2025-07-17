# 9. Product Warranty Checker
# Requirements:
# - /check-warranty: Form with product serial (POST)
# - /result?serial=ABC123 shows query-based response
# - /warranty/<product> returns warranty for specific product using dynamic routing
# - Redirect to confirmation page after checking


from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# Simulated warranty database
warranty_data = {
    "ABC123": "Valid until 2026-01-01",
    "XYZ789": "Expired on 2023-12-31",
    "LMN456": "Valid until 2025-11-15"
}

# Form template
check_warranty_form = """
<h2>Check Product Warranty</h2>
<form action="/check-warranty" method="post">
    Product Serial Number: <input type="text" name="serial" required>
    <input type="submit" value="Check">
</form>
"""

@app.route('/check-warranty', methods=['GET', 'POST'])
def check_warranty():
    if request.method == 'POST':
        serial = request.form.get('serial')
        return redirect(url_for('result', serial=serial))
    return render_template_string(check_warranty_form)

@app.route('/result')
def result():
    serial = request.args.get('serial')
    warranty = warranty_data.get(serial, "No warranty information found for this serial.")
    return f"""
    <h3>Warranty Status for {serial}:</h3>
    <p>{warranty}</p>
    <a href="/check-warranty">Check another</a>
    """

@app.route('/warranty/<product>')
def warranty_by_product(product):
    warranty = warranty_data.get(product, "No warranty information available for this product.")
    return f"""
    <h3>Warranty Details for {product}</h3>
    <p>{warranty}</p>
    """

if __name__ == '__main__':
    app.run(debug=True)
