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
@bp.route("/team_info/<string:token>", methods=["GET"])
def team_info_page(token):
    collection = database["record"]
    res = collection.find({"user_token": token})
    return jsonify(res), 200

@bp.route("/is_logged", methods=["GET"])
def is_logged_page():
    if session.get("user_token", None):
        message = {"team_name": session["team_name"]}
        return jsonify(message), 200
    else:
        return "token not matched", 400

@bp.route("/login", methods=["POST"])
def login_page():
    data = request.get_json()
    user_token = data.get("user_token", None)
    # query database
    res = collection.find_one({"user_token": user_token})

    if not res:
        return "", 400
    if True:
        session["user_token"] = user_token
        session["team_name"] = res["team_name"]
        return "", 200

@bp.route("/guess/<int:problem>", methods=["POST"])
def guess_page(problem):
    data = request.get_json()
    answer = data.get("answer", None) # get answer
    user_token = session.get("user_token", None) # get user_token

    # query database problem
    collection = database["problem"]
    res = collection.find_one({"number": problem})
    answer_length = len(res["answer"])
    correct_answer = res["answer"]

    if not user_token:
        return "", 401
    if len(answer) != answer_length:
        message = {"message": "系統錯誤"}
        return jsonify(message), 400

    if answer.lower() == correct_answer.lower():
        # upsert to database
        collection = database["record"]
        collection.update_one({"user_token": user_token}, {'$set':{'problem':problem}}, upsert=True)
        message = {"message": "答案正確"}
        return jsonify(message), 200
    else:
        message = {"message": "答案錯誤"}
        return jsonify(message), 403

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
