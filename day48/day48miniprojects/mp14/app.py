import os
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/gallery")
def gallery():
    image_folder = os.path.join(app.static_folder, 'images/gallery')
    images = []

    if os.path.exists(image_folder):
        for file in os.listdir(image_folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                images.append('images/gallery/' + file)

    return render_template("gallery.html", title="Photo Gallery", images=images)

if __name__ == "__main__":
    app.run(debug=True)
