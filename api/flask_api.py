from flask import Flask, render_template, send_file, make_response, redirect
from flask_limiter import Limiter, RequestLimit
from flask_limiter.util import get_remote_address
import sqlite3
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()
LIMIT = str(os.getenv("RATE_LIMIT", "2"))
REDIRECT = os.getenv("AUTO_REDIRECT", "http://localhost:5000")
USERNAME = os.getenv("GITHUB_USERNAME", "admin")
LANG = os.getenv("LANGUAGE", "en")

def rate_limited(request_limit: RequestLimit) -> None:
    # Return the rate limit error page or redirect to Github profile
    if REDIRECT:
        return redirect("https://github.com/" + USERNAME, code=302)
    return make_response(
        render_template(os.path.join(LANG, "rate_limit.html"), limit=LIMIT),
        429
    )

flask_api = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=flask_api,
    default_limits=[ LIMIT + " per second" ],
    storage_uri="memory://",
    on_breach=rate_limited
)


# For sending inputs
@flask_api.route("/input/<input>", methods=["GET"])
def input(input):
    # Check if the input is valid
    inputs = ["a", "b", "start", "select", "up", "down", "left", "right"]
    if input not in inputs:
        # Return the not valid error page
        return make_response(
            render_template(os.path.join(LANG, "not_valid.html")),
            400
        )
    
    try:
        # Connect to the database and insert the input
        conn = sqlite3.connect('/shared/db/inputs.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inputs (input) VALUES (?)", (input,))
        conn.commit()
        conn.close()

        # Return the success page or redirect to Github profile
        if REDIRECT:
            return redirect("https://github.com/" + USERNAME, code=302)
        return render_template(os.path.join(LANG, "ok.html"), input=str.capitalize(input))
    except sqlite3.Error as e:
        # Return the SQL error page in case of a database error
        return make_response(
            render_template(os.path.join(LANG, "not_valid.html")),
            500
        )

# To get the latest screenshot
@flask_api.route("/screen/screen.png")
@limiter.exempt
def screen():
    # Check if the screenshot exists
    if not os.path.exists('/shared/screen/screen.png'):
        # Return the offline screenshot if not found
        return send_file(os.path.join("./templates", LANG, "img/offline.png"), mimetype='image/png')
    # Return the current screenshot
    return send_file('/shared/screen/screen.png', mimetype='image/png')
