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

@app.route("/loginpage")
def loginpage():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]

    return f"Welcome Back {email}"

if __name__ == "__main__":
    app.run(debug=True)