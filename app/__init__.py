from flask import Flask, request, redirect, render_template, session
from datetime import datetime
import db

app = Flask(__name__)
app.secret_key = "foo"


@app.route("/")
def index():
    """
    Displays the default page of the website
    """
    if logged_in():
        return redirect("/home")
    return render_template("index.html")


def logged_in():
    return 'user' in session


@app.route("/signup", methods=['POST'])
def signup():
    """
    Retrieves user inputs from signup page.
    Checks it against the database to make sure the information is unique.
    Adds information to the "users" database table.
    """
    user = request.form["newusername"]
    pwd = request.form["newpassword"]
    if user.strip() == "" or pwd.strip == "":
        return render_template("index.html", explain="Username or Password cannot be blank")
    # Add user information if passwords match
    if (request.form["newpassword"] != request.form["newpassword1"]):
        return render_template("index.html", explain="The passwords do not match")

    register_success = db.register_user(user, pwd) #returns whether or not user was registered
    if not register_success:
        return render_template("index.html", explain="Username already exists")
    else:
        user_id = db.fetch_user_id(user, pwd)
        session["user"] = db.fetch_username(user_id)
        session["user_id"] = user_id
        return redirect("/home")


@app.route("/login", methods=['POST'])
def login():
    """
    Retrieves user login inputs and checks it against the "users" database table.
    Brings user to home page after successful login.
    """
    user = request.form["username"]
    pwd = request.form["password"]

    if user.strip() == "" or pwd.strip() == "":
        return render_template("index.html", explain1 = "Username or Password cannot be blank")

    user_id = db.fetch_user_id(user, pwd) # None when no user_id exists for that user and pwd
    if user_id is None:
        return render_template("index.html", explain1 = "Username or Password is incorrect")
    # Adds user and user id to session if all is well
    session["user"] = db.fetch_username(user_id)
    session["user_id"] = user_id
    return redirect("/home")


@app.route("/logout")
def logout():
    if logged_in():
        session.pop("user")
        session.pop("user_id")
    return redirect("/")


@app.route("/home")
def home():
    if logged_in():
        return render_template("home.html", user = session['user'], entries = db.fetch_journal(session["user_id"]))
    return redirect("/")


@app.route("/entry", methods=["POST"])
def entry():
    """
    Retrieves the user's new entry and adds it to their lists of entries.
    """
    entry = request.form["entry"]
    date = request.form["date"] # 2022-10-15
    # print(entry, date) # works with new lines!!
    '''
    >>> from datetime import datetime
    >>> now = datetime.now()
    >>> print(now)
    2022-10-15 21:39:37.232720
    >>> now.strftime("%B %d %Y")
    'October 15 2022'
    '''
    format_data = "%Y-%m-%d"
    date = datetime.strptime(date, format_data) #format the time stamp which is in string format to date-time object.
    date = date.strftime("%B %d, %Y") # October 10, 2022
    print("DEBUG: " + date)

    added = db.add_to_journal(session["user_id"], entry, date)
    if added:
        return render_template("home.html", user = session['user'], entries = db.fetch_journal(session["user_id"]))
    else:
        return render_template("home.html", user = session['user'], entries = db.fetch_journal(session["user_id"]), explain = "An entry for this day was already written")


if __name__ == "__main__":
	app.debug = True
	app.run()