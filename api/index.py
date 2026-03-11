from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    notebooks = [
        {"name": "Notebook 1"},
        {"name": "Notebook 2"}
    ]
    return render_template("index.html", notebooks=notebooks)

def handler(request):
    return app(request.environ, lambda status, headers: None)