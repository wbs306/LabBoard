from labboard.BaiduExpress import BaiduExpress
from flask import (
    Blueprint, request, jsonify
)

bp = Blueprint("express", __name__, url_prefix="/express")
baidu_express = BaiduExpress()

@bp.route("/getExpressCompany", methods=["POST"])
def get_express_company():
    if (request.method == "POST"):
        number = request.form["number"]
    return jsonify(baidu_express.get_express_company(number))

@bp.route("/getExpressState", methods=["POST"])
def get_express_state():
    if (request.method == "POST"):
        number = request.form["number"]
        company = request.form["company"]
    return jsonify(baidu_express.get_express_state(number, company))
