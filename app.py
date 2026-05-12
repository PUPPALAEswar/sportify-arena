from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "sportify_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sportify.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DATABASE TABLE
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(100), nullable=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["POST"])
def signup():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    user_exists = User.query.filter_by(email=email).first()

    if user_exists:
        return "User already exists"

    new_user = User(
        name=name,
        email=email,
        password=password
    )

    db.session.add(new_user)
    db.session.commit()

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
    password = request.form["password"]

    user = User.query.filter_by(
        email=email,
        password=password
    ).first()

    if user:

        session["user"] = user.name

        return redirect("/dashboard")

    return "Invalid Email or Password"


@app.route("/dashboard")
def dashboard():

    if "user" in session:

        return f"""
        <h1>Welcome to Sportify Arena</h1>
        <h2>Hello {session['user']}</h2>

        <a href='/logout'>Logout</a>
        """

    return redirect("/loginpage")


@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/loginpage")


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)