from flask import Blueprint, send_from_directory, session, request


bp = Blueprint("main", __name__)

@bp.route("/login", methods=["POST"])
def login_page():
    # placeholder
    session["username"] = "test"
    return ""

@bp.route("/guess/<string:problem>", methods=["POST"])
def guess_page(problem):
    ...

@bp.route("/collect", methods=["POST"])
def collect_page():
    data = request.get_json()
    token = data.get("token", None)
    if not token:
        return "", 400
    if True:
        return ""
    else:
        return "", 201

@bp.route("/stamp/<int:number>", methods=["GET"])
def stamp_page(number):
    filename = "black.png"
    if session.get("username", None):
        filename = f"image-{number}.png"
    return send_from_directory("../images", filename)
