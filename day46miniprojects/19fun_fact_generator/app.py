from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return """
        <h1 style= "background-color:purple; color:white; text-align: center;padding:3%;" >Fun fact Generator</h1>
        """


# Dictionary of animal fun facts
animal_facts = {
    "dog": "Dogs can learn over 1000 words and gestures.",
    "cat": "Cats can jump up to six times their length!",
    "elephant": "Elephants can recognize themselves in mirrors.",
    "owl": "Owls can rotate their heads up to 270 degrees.",
    "dolphin": "Dolphins sleep with one eye open!"
}

# Route: /fact/<animal>
@app.route('/fact/<animal>')
def fact(animal):
    animal = animal.lower()
    fact = animal_facts.get(animal)
    
    if fact:
        return f"""
        <html>
            <head><title>Fun Fact: {animal.title()}</title></head>
            <body style="font-family: Arial; background-color: #fff3cd; text-align: center; padding: 50px;">
                <div style="background-color: #ffeeba; padding: 30px; border-radius: 10px;">
                    <h2>🐾 Fun Fact About {animal.title()}</h2>
                    <p style="font-size: 20px;">{fact}</p>
                    <hr>
                    <p><a href="/fact/list">See all available animals</a></p>
                </div>
            </body>
        </html>
        """
    else:
        return f"""
        <html>
            <body style="font-family: Arial; text-align: center; background-color: #f8d7da; padding: 40px;">
                <h2 style="color: #721c24;">❌ No fact found for '{animal}'</h2>
                <p><a href="/fact/list">Click here to see available animals</a></p>
            </body>
        </html>
        """

# Route: /fact/list
@app.route('/fact/list')
def fact_list():
    items = "".join([f"<li>{animal.title()}</li>" for animal in animal_facts.keys()])
    
    return f"""
    <html>
        <head><title>Available Animals</title></head>
        <body style="font-family: Arial; background-color: #e2f0d9; text-align: center; padding: 50px;">
            <div style="background-color: #d4edda; padding: 30px; border-radius: 10px;">
                <h2>📜 Animals You Can Ask About</h2>
                <ul style="list-style-type: none; font-size: 18px; padding: 0;">
                    {items}
                </ul>
                <hr>
                <p>Try: <code>/fact/dog</code>, <code>/fact/owl</code>, etc.</p>
            </div>
        </body>
    </html>
    """

# Run app
if __name__ == '__main__':
    print("🦁 Fun Fact Generator running on http://127.0.0.1:5000")
    app.run(debug=True)
