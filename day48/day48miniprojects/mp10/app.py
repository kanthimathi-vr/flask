from flask import Flask, render_template

app = Flask(__name__)

@app.route("/products")
def products():
    product_list = [
        {
            "name": "Wireless Headphones",
            "price": 59.99,
            "in_stock": True,
            "image": "images/product1.jpg"
        },
        {
            "name": "Smartwatch",
            "price": 129.99,
            "in_stock": False,
            "image": "images/product2.jpg"
        },
        {
            "name": "Gaming Mouse",
            "price": 39.99,
            "in_stock": True,
            "image": "images/product3.jpg"
        }
    ]
    return render_template("products.html", title="Our Products", products=product_list)

if __name__ == "__main__":
    app.run(debug=True)
