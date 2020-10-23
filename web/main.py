from flask import Flask, send_from_directory, make_response, redirect, url_for
from ics import dav2ics
import keys

app = Flask(__name__)


def __get_ICS(key):
    if key == keys.DANIEL:
        return dav2ics.getStrCalendars([("default", True), ("personnal", False)])
    elif key == keys.THIBAUT:
        return dav2ics.getStrCalendars([("default", True), ("personnal", False)])
    elif key == keys.LAURENT:
        return dav2ics.getStrCalendars([("default", True), ("personnal", False)])
    elif key == keys.AURELIEN:
        return dav2ics.getStrCalendars([("default", True), ("personnal", False)])
    elif key == keys.OTHER:
        return dav2ics.getStrCalendars([("default", False), ("personnal", False)])

    return None

@app.route("/ics/", strict_slashes=False)
@app.route("/ics/<key>", strict_slashes=False)
def show_ICS(key=""):
    ics = __get_ICS(key)
    if ics is not None:
        response = make_response(ics, 200)
        response.mimetype = "text/plain"
        return response

    return "Please put a correct key"

@app.route("/ics/<key>/view", strict_slashes=False)
def view_ICS_redir(key):
    return redirect(url_for("view_ICS", key=key))

@app.route("/view/<key>", strict_slashes=False)
def view_ICS(key):
    ics = __get_ICS(key)
    if ics is not None:
        path = "index.html"
    else:
        path = key

    return send_from_directory('./static/online-ics-feed-viewer/', path)

@app.route("/view/lib/<path>", strict_slashes=False)
def serve_lib(path):
    return send_from_directory('./static/online-ics-feed-viewer/lib', path)
