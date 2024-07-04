import os
from enum import Enum
from flask import Blueprint, send_from_directory, session, request, jsonify, current_app
from pymongo import MongoClient

secret = os.getenv("SECRET")
assert secret
username = os.getenv("MONGO_USERNAME", "admin")
password = os.getenv("MONGO_PASSWORD", "admin")
client = MongoClient(f"mongodb://{username}:{password}@hackathon2024-mongodb:27017/")
collection = client["sitcon-hackathon"]["users"]

TOKEN_PROBLEM_MAP = {
    '8dd5c5e969ec5d24c825a409d77cb7e42794c9708c1b80c350c70b90a38f5f36': 2,
    '929d586819380e59e49c59c09f7f2b8ff0dc8ee46012076330fffff04e876ec9': 6,
    '96cab5718e3171b7b788e78ec7329e815ba60ada2a51838878f51e79c7a878cd': 7,
    '5be6ce0530ed9d608b51c2adc49ce826e732253a74095d031e98a560597bb4b7': 10,
    'a279dfa7053d3c965934183deb4aaef86f62f37a75f7dc071a019e7a61d644c5': 11,
    'be527397b173da8d5c9fafc503d096c591af9393674dc5c1cd5b305c72fe2bf5': 12,
    '9616971f7b97ed5ca0d40bb4a63d951679ba3d21f8aed55f1a273e7059578df3': 13,
    '7e8e4ce30f80b85ef3b3f6f2a1bee4c267f0abd9aa5fa323c2bd2ed3ad7a8fb9': 14,
    '0e2e9a23a50750ee09dbe5ce982b497d6f9a85b0d10bb40f72ab78519d2c5b31': 19,
    '18ec5bf28eb443b84ccaf1792caaf9aba6a066f46b3ef3a1e824761f790d8902': 21, # Above are for stalls
    '97973dd45474f26cea8adcc47bcf1c1c68655dbfba5df6914c213f2666c7e5f8': 4,
    '0a8becc6c4349d4d014c9144420a9133a8d59c4a1d19d5e12d891bf6f1554091': 5, # Above are for check in wall
    '31fb2b0ad61ffcc8b96ecd64fbb12a135e68e2484dc0afb2372e7f65d7e944df': 15,
    '294b3e339f48879542052d9c3d119598090711c423520ea2e063c9e1ee3b2e2d': 17,
    '38a2283f668a08414a0495de56b8180195c169465b339ce9be7091320294b410': 23 # Above are for guess where am i
}
GAME_ANS = {
    0: {
        'answer': ['COMPUTER', 'DOOR', 'STAGE', 'TABLE', 'WALL'],
        'stamp': [[1, 3], [22]],
        'message': [
            '有答案是錯的歐',
            '請再仔細看題目呦',
            '恭喜你成功!但接下來的挑戰可沒這麼簡單歐，哈哈'
        ],
        'total_stamp': 3
    },
    1: {
        'answer': ['Please', 'check', 'under', 'your', 'desk'],
        'stamp': [[], [0]],
        'message': [
            '再仔細檢查我們精美的圖吧',
            '再仔細檢查我們精美的圖吧',
            '歡迎進到第二階段!'
        ],
        'total_stamp': 1
    },
    2: {
        'answer': ['Please', 'computer'],
        'stamp': [[24], [18]],
        'message': [
            '猜錯了歐，請再一次',
            '請再確認一下答案',
            '相當厲害，相信你也準備好進到最終試煉了，那就敬請期待吧~!'
        ],
        'total_stamp': 2
    },
    3: {
        'answer': ['I', 'LOVE', 'SITCON', 'HACKATHON', '2024'],
        'stamp': [[], [16, 8, 20, 9]],
        'message': [
            '請認真玩遊戲，不然你朋友將死於戰爭…',
            '請認真玩遊戲，不然你朋友將死於戰爭…',
            '恭喜你全數破關! 但，這只是集章活動的一部分，若要獲得最終獎品，還是得破完拼圖，並正確猜到最終答案歐😉'
        ],
        'total_stamp': 4
    }
}

def add_stamp_to_user(user_token, stamp):
    res = collection.find_one({"user_token": user_token})
    if not res:
        current_app.logger.error(f'{user_token} not in the users collection')
        return False
    elif stamp in res.get("collected", []):
        return False
    else:
        collection.update_one({"user_token": user_token}, {"$addToSet": {"collected": stamp}})
        return True

class Result(Enum):
    WRONG = 0
    PARTIAL = 1
    CORRECT = 2

def compare_game_ans(guess, ans):
    guess = [x.lower().strip() for x in guess]
    ans = [x.lower().strip() for x in ans]
    if ans == guess:
        return Result.CORRECT
    guess = sorted(guess)
    ans = sorted(ans)
    if ans == guess:
        return Result.PARTIAL
    return Result.WRONG
    

bp = Blueprint("main", __name__)

@bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return "", 200

@bp.route("/team_info", methods=["GET"])
def team_info_page():
    user_token = session.get("user_token", None)
    if user_token:
        res = collection.find_one({"user_token": user_token})
        return jsonify({"problem": res['problem']}), 200
    else:
        return "token not matched", 201

@bp.route("/is_logged", methods=["GET"])
def is_logged_page():
    if session.get("user_token", None):
        message = {"team_name": session["team_name"]}
        return jsonify(message), 200
    else:
        return "token not matched", 201

@bp.route("/register", methods=["POST"])
def register():
    secret_token = request.json['secret_token'].strip()
    user_token = request.json['user_token'].strip()
    team_name = request.json['team_name'].strip()
    if secret_token != secret:
        return "", 400
    if not user_token or not team_name:
        return "", 400
    res = collection.insert_one({"user_token": user_token, "team_name": team_name, "collected": [], "problem": 0})
    return "", 200

@bp.route("/login", methods=["POST"])
def login_page():
    user_token = request.json['user_token'].strip()
    # query database
    res = collection.find_one({"user_token": user_token})

    if not res:
        return "", 201
    else:
        session["user_token"] = user_token
        session["team_name"] = res["team_name"]
        return res["team_name"], 200

# problem is 0-indexed
@bp.route("/guess/<int:problem>", methods=["POST"])
def guess_page(problem):
    user_token = session.get("user_token", None) # get user_token
    if not user_token:
        return "", 401
    answer = request.json['answer']

    if problem not in GAME_ANS:
        return "", 400
    ans = GAME_ANS[problem]['answer']
    res = compare_game_ans(answer, ans)

    stamps = []
    for i in range(res.value):
        stamps += GAME_ANS[problem]['stamp'][i]
    for stamp in stamps:
        add_stamp_to_user(user_token, stamp)
    
    message = {"message": GAME_ANS[problem]['message'][res.value], "result": res.value, "count": len(stamps), "total_stamp": GAME_ANS[problem]['total_stamp']}
    if res == Result.CORRECT:
        collection.update_one({"user_token": user_token}, {'$max':{'problem': problem + 1}})
    return jsonify(message), 200

@bp.route("/collect", methods=["POST"])
def collect_page():
    user_token = session.get("user_token", None)
    if not user_token:
        return "", 401
    data = request.get_json()
    token = data.get("token", None).strip()
    stamp = TOKEN_PROBLEM_MAP.get(token, None)
    if not stamp:
        return "", 202
    if add_stamp_to_user(user_token, stamp):
        return "", 200
    else:
        return "", 201

@bp.route("/stamp/<int:number>", methods=["GET"])
def stamp_page(number):
    filename = "black.png"
    if session.get("user_token", None):
        res = collection.find_one({"user_token": session["user_token"]})
        if res and number in res.get("collected", []):
            filename = f"image-{number}.png"
    return send_from_directory("../images", filename)
