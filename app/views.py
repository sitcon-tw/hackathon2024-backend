from flask import Blueprint

bp = Blueprint("main", __name__)

@bp.route("/login", methods=["POST"])
def login_page():
    ...

@bp.route("/guess/<string:problem>", methods=["POST"])
def guess_page(problem):
    ...

@bp.route("/collect", methods=["POST"])
def collect_page():
    ...

@bp.route("/stamp/<int:number>", methods=["GET"])
def stamp_page(number):
    ...
