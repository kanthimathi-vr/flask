from flask import Flask, render_template

app = Flask(__name__)

@app.route("/menu")
def menu():
    menu_data = {
        "Starters": [
            {"name": "Bruschetta", "price": 6.5, "available": True, "image": "images/starter1.jpg"},
            {"name": "Garlic Bread", "price": 4.0, "available": False, "image": "images/starter2.jpg"},
        ],
        "Mains": [
            {"name": "Margherita Pizza", "price": 12.0, "available": True, "image": "images/main1.jpg"},
            {"name": "Spaghetti Carbonara", "price": 14.0, "available": True, "image": "images/main2.jpg"},
        ],
        "Desserts": [
            {"name": "Tiramisu", "price": 7.0, "available": False, "image": "images/dessert1.jpg"},
            {"name": "Gelato", "price": 5.5, "available": True, "image": "images/dessert2.jpg"},
        ],
    }
    return render_template("menu.html", title="Our Menu", menu=menu_data)

if __name__ == "__main__":
    app.run(debug=True)
