from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():

    name = request.form["name"]
    email = request.form["email"]

    return render_template(
        "success.html",
        name=name,
        email=email
    )

if __name__ == "__main__":
    app.run(debug=True)