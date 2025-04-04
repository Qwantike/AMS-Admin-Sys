from flask import Flask, render_template
import os

app = Flask(__name__)

GRAPHICS_DIR = "static/graphics"  # Correction du chemin

@app.route("/")
def index():
    # Récupérer toutes les images dans le dossier graphics
    images = [f for f in os.listdir(GRAPHICS_DIR) if f.endswith(".png")]
    images.sort()  # Tri pour afficher toujours dans le même ordre
    
    return render_template("index.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)


