import os
from flask import Blueprint, send_from_directory, session, request
from pymongo import MongoClient

username = os.getenv("MONGO_USERNAME", "admin")
password = os.getenv("MONGO_PASSWORD", "admin")
client = MongoClient(f"mongodb://{username}:{password}@mongodb:27017/")
database = client["sitcon-hackathon"]
collection = database["users"]

TOKEN_PROBLEM_MAP = {
    "TOKEN0": 0,
}

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

@bp.route("/guess/<int:problem>", methods=["POST"])
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
    user_token = session.get("user_token", None)
    if not user_token:
        return "", 401
    data = request.get_json()
    token = data.get("token", None)
    problem = TOKEN_PROBLEM_MAP.get(token, None)
    if not problem:
        return "", 400
    res = collection.find_one({"user_token": user_token})
    if not res:
        collection.insert_one({"user_token": user_token, "collected": [problem]})
        return ""
    elif problem in res.get("collected", []):
        return "", 201
    else:
        collection.update_one({"user_token": user_token}, {"$addToSet": {"collected": problem}})
        return ""

@bp.route("/stamp/<int:number>", methods=["GET"])
def stamp_page(number):
    filename = "black.png"
    if session.get("user_token", None):
        res = collection.find_one({"user_token": session["user_token"]})
        if res and number in res.get("collected", []):
            filename = f"image-{number}.png"
    return send_from_directory("../images", filename)
