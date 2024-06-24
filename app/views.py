from flask import Blueprint, send_from_directory, session, request


bp = Blueprint("main", __name__)

@bp.route("/login", methods=["POST"])
def login_page():
    data = request.get_json()
    user_token = data.get("user_token", None)
    # query database
    valid_account = True
    
    if not valid_account:
        return "", 400
    if True:
        session["user_token"] = user_token
        return "", 200
    # placeholder
    session["username"] = "test"

@bp.route("/guess/<string:problem>", methods=["POST"])
def guess_page(problem):
    data = request.get_json()
    answer = data.get("answer", None)
    if len(answer) != 4:
        message = {"message": "系統錯誤"}
        return jsonify(message), 400
    
    # query database
    correct_answer = True

    if not correct_answer:
        message = {"message": "答案錯誤"}
        return jsonify(message), 403
    if True:
        message = {"message": "答案正確"}
        return jsonify(message), 200

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
