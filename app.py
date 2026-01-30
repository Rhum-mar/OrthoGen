import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)
app.debug = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ortho.db")

def get_options():
    options = ["frequence", "nature", "nb_syllabes", "difficulte"]
    return options

def value_options():
        selected_criterion = request.args.get("criterion")
        value_options = db.execute(f"SELECT DISTINCT {selected_criterion} FROM words ORDER BY {selected_criterion} ASC")
        return value_options


@app.route("/", methods=["GET", "POST"])
def index():
    options = get_options()
    return render_template("search.html", options=options)



@app.route("/get_value_options")
def get_value_options():
    selected_criterion = request.args.get("criterion")
    value_options = db.execute(f"SELECT DISTINCT {selected_criterion} FROM words ORDER BY {selected_criterion} ASC")
    return jsonify(value_options)

@app.route("/generate_list", methods=["POST"])
def generate_list():
    words_number = request.form.get("words_number")
    search_rows = request.form.getlist("selected_option")
    values = request.form.getlist("value_options")

    # Initialize the base query
    base_query = "SELECT mot FROM words"

    # Initialize the list of query parameters
    query_params = []

    # Build the base query with the first criterion
    if search_rows and values:
        base_query += f" WHERE {search_rows[0]} = ?"
        query_params.append(values[0])

    # Iterate over additional criteria, if any
    for i in range(1, len(search_rows)):
        base_query += f" AND {search_rows[i]} = ?"
        query_params.append(values[i])

    # Add ORDER BY RANDOM() and LIMIT clauses
    base_query += " ORDER BY RANDOM()"
    if words_number:
        base_query += f" LIMIT {words_number}"

    # Execute the SQL query
    words_list = db.execute(base_query, *query_params)
    words = [row['mot'] for row in words_list]

    options = get_options()

    return render_template("search.html", words=words, options=options)









@app.route("/search_patients", methods=["GET","POST"])
def search_patients():
    query = request.form.get("query")
    # Query the database for patients matching the search query
    patients = db.execute("SELECT * FROM patients WHERE nom LIKE ? OR prenom LIKE ?", query, query)

    return render_template("search_patients.html",patients=patients)

@app.route("/infos_patient")
@login_required
def patient():
    return apology("not coded yet", 200)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM therap WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("you must provide username", 400)

         # Ensure password and verification was submitted
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password and verification", 400)

        # ensure password is same than verification
        if not request.form.get("confirmation") == request.form.get("password"):
            return apology("wrong password double check", 400)

        # check if password already exists
        existing_user = db.execute("SELECT * FROM therap WHERE username = ?",request.form.get("username"))

        if existing_user:
            return apology("username already taken", 400)

        # hash password
        hashed_password = generate_password_hash(request.form.get("password"))

        # insert password in database

        new_row = db.execute("INSERT INTO therap (username, hash, email) VALUES (?, ?, ?)",
                             request.form.get("username"), hashed_password, request.form.get("email"))

        if not new_row:
            return apology("registration failed", 403)

        # stay connected
        elif new_row:
            new_username = request.form.get("username")
            new_row_id = db.execute("SELECT id FROM therap WHERE username = ? ", new_username)
            if len(new_row_id) == 1:
                session["user_id"] = new_row_id[0]['id']

    # return to home page
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
