from flask import Flask

app = Flask(__name__)

# 🔸 Hardcoded Product Data (dictionary with string keys for IDs)
products = {
    "101": {"name": "Wireless Mouse", "price": "$25", "stock": "In Stock"},
    "102": {"name": "Mechanical Keyboard", "price": "$75", "stock": "Out of Stock"},
    "103": {"name": "HD Monitor", "price": "$150", "stock": "In Stock"}
}

@app.route('/')
def home():
    return "<h1>Product Info</h1>"

# 🔹 Individual Product Page
@app.route('/product/<id>')
def product_info(id):
    print(f"[LOG] Accessed /product/{id}")
    
    product = products.get(id)
    if not product:
        return f"""
        <html>
            <body style="font-family:Arial;text-align:center;margin-top:50px;">
                <h2>❌ Product Not Found</h2>
                <p>No product found with ID: {id}</p>
            </body>
        </html>
        """

    return f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial;
                    text-align: center;
                    background-color: #f5faff;
                    margin-top: 50px;
                }}
                .card {{
                    border: 2px solid #2196f3;
                    display: inline-block;
                    padding: 20px;
                    border-radius: 10px;
                    background: #e3f2fd;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Product ID: {id}</h2>
                <p><strong>Name:</strong> {product['name']}</p>
                <p><strong>Price:</strong> {product['price']}</p>
                <p><strong>Stock:</strong> {product['stock']}</p>
            </div>
        </body>
    </html>
    """

# 🔹 Route: List All Products
@app.route('/products')
def product_list():
    print("[LOG] Accessed /products")

    table_rows = ""
    for pid, details in products.items():
        table_rows += f"<tr><td>{pid}</td><td>{details['name']}</td></tr>"

    return f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial;
                    text-align: center;
                    background-color: #fcfcfc;
                    margin-top: 40px;
                }}
                table {{
                    margin: auto;
                    border-collapse: collapse;
                    width: 60%;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 10px;
                    text-align: center;
                }}
                th {{
                    background-color: #f0f0f0;
                }}
            </style>
        </head>
        <body>
            <h2>📦 Product Catalog</h2>
            <table>
                <tr>
                    <th>Product ID</th>
                    <th>Name</th>
                </tr>
                {table_rows}
            </table>
        </body>
    </html>
    """

# 🔹 Run the Flask App
if __name__ == '__main__':
    print("🛒 Product Info App running at http://127.0.0.1:5000")
    app.run(debug=True)
