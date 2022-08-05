import flask

from flask import Flask, render_template_string, request
app = Flask(__name__)

@app.route("/")
def index():
    name = request.args.get("name")
    if name:
        return "Hello, " + render_template_string(name)
    else:
        return "Please GET me your name.\n"

if __name__ == "__main__":
    with open("/root/status", "w") as f:
        f.write("1")
    app.run(host="0.0.0.0")