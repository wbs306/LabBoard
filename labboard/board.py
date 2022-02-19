import json
import os

from flask import (
    Blueprint, render_template, request, jsonify, current_app
)
from labboard.db import query_db

bp = Blueprint('board', __name__, url_prefix="/board")

@bp.route('/')
def load_board():
    sensor_record = query_db("SELECT * FROM SensorCollector WHERE date > DATETIME('NOW', '-1 DAY')")
    fan_record = query_db("SELECT * FROM FanCollector")
    ups_record = query_db("SELECT * FROM UPSCollector")
    sensor_data = {
        "date": [],
        "temperature": [],
        "humidity": []
    }

    last_temp = 0
    temp_diff = 0.35
    for i in sensor_record:
        if (abs(i[1] - last_temp) < temp_diff):
            continue
        sensor_data["date"].append(i[0])
        sensor_data["temperature"].append(round(i[1], 1))
        sensor_data["humidity"].append(round(i[2], 2))
        last_temp = i[1]

    record_exist = os.path.exists(current_app.config["RECORD_FILE"])
    kwargs = {
        "sensor_data": sensor_data,
        "record_exist": record_exist,
    }
    if (record_exist):
        from labboard.weather import get_weather
        from labboard.express import get_express_state
        with open(current_app.config["RECORD_FILE"], "r") as f:
            record = json.load(f)
            kwargs["weather"] = get_weather(record["city_code"])
            packages = []
            if (record.get("packages")):
                packages = record["packages"]
        kwargs["packages_info"] = []
        for i in packages:
            state = get_express_state(i["number"], i["company"])
            state["number"] = i["number"]
            kwargs["packages_info"].append(state)
    return render_template('board.html', **kwargs)
