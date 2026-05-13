from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "sportify_secret_key"

# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sportify.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# USER TABLE
# =========================
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(100), nullable=False)


# =========================
# TOURNAMENT TABLE
# =========================
class Tournament(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    team_name = db.Column(db.String(100), nullable=False)

    captain_name = db.Column(db.String(100), nullable=False)

    sport = db.Column(db.String(50), nullable=False)

    contact = db.Column(db.String(20), nullable=False)

class Match(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    team1 = db.Column(db.String(100), nullable=False)

    team2 = db.Column(db.String(100), nullable=False)

    sport = db.Column(db.String(50), nullable=False)

    match_date = db.Column(db.String(50), nullable=False)

class Venue(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    venue_name = db.Column(db.String(100), nullable=False)

    sport = db.Column(db.String(50), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    available_time = db.Column(db.String(100), nullable=False)

    contact = db.Column(db.String(20), nullable=False)


# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():

    return render_template("index.html")


# =========================
# SIGNUP
# =========================
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


# =========================
# LOGIN PAGE
# =========================
@app.route("/loginpage")
def loginpage():

    return render_template("login.html")


# =========================
# LOGIN
# =========================
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


# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():

    if "user" in session:

        return render_template(
            "dashboard.html",
            user=session["user"]
        )

    return redirect("/loginpage")


# =========================
# TOURNAMENT PAGE
# =========================
@app.route("/tournament")
def tournament():

    if "user" in session:

        return render_template("tournament.html")

    return redirect("/loginpage")


# =========================
# REGISTER TOURNAMENT
# =========================
@app.route("/register_tournament", methods=["POST"])
def register_tournament():

    team_name = request.form["team_name"]

    captain_name = request.form["captain_name"]

    sport = request.form["sport"]

    contact = request.form["contact"]

    new_team = Tournament(
        team_name=team_name,
        captain_name=captain_name,
        sport=sport,
        contact=contact
    )

    db.session.add(new_team)

    db.session.commit()

    return redirect("/teams")


# =========================
# VIEW TEAMS
# =========================
@app.route("/teams")
def teams():

    if "user" in session:

        all_teams = Tournament.query.all()

        return render_template(
            "teams.html",
            teams=all_teams
        )

    return redirect("/loginpage")

@app.route("/schedule")
def schedule():

    teams = Tournament.query.all()

    return render_template(
        "schedule.html",
        teams=teams
    )


@app.route("/create_match", methods=["POST"])
def create_match():

    team1 = request.form["team1"]

    team2 = request.form["team2"]

    sport = request.form["sport"]

    match_date = request.form["match_date"]

    new_match = Match(
        team1=team1,
        team2=team2,
        sport=sport,
        match_date=match_date
    )

    db.session.add(new_match)

    db.session.commit()

    return redirect("/matches")


@app.route("/matches")
def matches():

    all_matches = Match.query.all()

    return render_template(
        "matches.html",
        matches=all_matches
    )

@app.route("/add_venue")
def add_venue():

    return render_template("add_venue.html")


@app.route("/save_venue", methods=["POST"])
def save_venue():

    venue_name = request.form["venue_name"]

    sport = request.form["sport"]

    location = request.form["location"]

    available_time = request.form["available_time"]

    contact = request.form["contact"]

    new_venue = Venue(
        venue_name=venue_name,
        sport=sport,
        location=location,
        available_time=available_time,
        contact=contact
    )

    db.session.add(new_venue)

    db.session.commit()

    return redirect("/venues")


@app.route("/venues")
def venues():

    all_venues = Venue.query.all()

    return render_template(
        "venues.html",
        venues=all_venues
    )
@app.route("/find_courts")
def find_courts():

    return render_template("find_courts.html")


@app.route("/search_courts", methods=["POST"])
def search_courts():

    sport = request.form["sport"]

    location = request.form["location"]

    filtered_venues = Venue.query.filter_by(
        sport=sport,
        location=location
    ).all()

    return render_template(
        "search_results.html",
        venues=filtered_venues,
        sport=sport,
        location=location
    )




# =========================
# DELETE TEAM
# =========================
@app.route("/delete_team/<int:id>")
def delete_team(id):

    team = Tournament.query.get(id)

    if team:

        db.session.delete(team)

        db.session.commit()

    return redirect("/teams")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/loginpage")


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=True)