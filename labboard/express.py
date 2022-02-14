from crypt import methods
import json
from re import L

from labboard.BaiduExpress import BaiduExpress
from flask import (
    Blueprint, request, jsonify, current_app
)

bp = Blueprint("express", __name__, url_prefix="/express")
baidu_express = BaiduExpress()

@bp.route("/getExpressCompany", methods=["POST"])
def get_express_company():
    if (request.method == "POST"):
        number = request.form["number"]
    return jsonify(baidu_express.get_express_company(number))

@bp.route("/getExpressState", methods=["POST"])
def get_express_state(number=None, company=None):
    if (request.method == "POST"):
        number = request.form["number"]
        company = request.form["company"]
        return jsonify(baidu_express.get_express_state(number, company))
    else:
        return baidu_express.get_express_state(number, company)

@bp.route("/addPackage", methods=["POST"])
def add_package():
    if (request.method == "POST"):
        package_info = {
            "number": request.form["number"],
            "company": request.form["company"],
            "name": request.form["name"]
        }
    
        with open(current_app.config["RECORD_FILE"], "r") as f:
            record = json.load(f)

        if (record.get("packages")):
            for p in record["packages"]:
                if (p == package_info):
                    return jsonify({"status": "duplicated"})

            record["packages"].append(package_info)
        else:
            record["packages"] = [package_info]
        
        with open(current_app.config["RECORD_FILE"], "w") as f:
            json.dump(record, f)
        
        return jsonify({"status": "ok"})

@bp.route("/getPackages", methods=["GET", "POST"])
def get_packages():
    with open(current_app.config["RECORD_FILE"], "r") as f:
        record = json.load(f)
    if (record.get("packages")):
        return jsonify(record["packages"])
    else:
        return jsonify([])

@bp.route("/deletePackage", methods=["POST"])
def delete_package():
    if (request.method == "POST"):
        package_info = {
            "number": request.form["number"],
            "company": request.form["company"],
            "name": request.form["name"]
        }
        with open(current_app.config["RECORD_FILE"], "r") as f:
            record = json.load(f)
        if (record.get("packages")):
            for p in record["packages"]:
                if (p == package_info):
                    record["packages"].remove(p)
                    with open(current_app.config["RECORD_FILE"], "w") as f:
                        json.dump(record, f)
                    return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "no_such_package"})
    