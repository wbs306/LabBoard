import json
import os

from flask import (
    Blueprint, render_template, request, jsonify, current_app
)
from labboard.db import get_db

bp = Blueprint('board', __name__, url_prefix="/board")

@bp.route('/')
def load_board():
    db = get_db()
    sensor_record = db.execute("SELECT * FROM SensorCollector").fetchall()
    fan_record = db.execute("SELECT * FROM FanCollector").fetchall()
    ups_record = db.execute("SELECT * FROM UPSCollector").fetchall()
    sensor_data = {
        "date": [],
        "temperature": [],
        "humidity": []
    }
    for i in sensor_record:
        sensor_data["date"].append(i[0])
        sensor_data["temperature"].append(round(i[1], 1))
        sensor_data["humidity"].append(round(i[2], 2))

    record_exist = os.path.exists(current_app.config["RECORD_FILE"])
    kwargs = {
        "sensor_data": sensor_data,
        "record_exist": record_exist,
    }
    if (record_exist):
        from labboard.weather import get_weather
        with open(current_app.config["RECORD_FILE"], "r") as f:
            city_code = json.load(f)["city_code"]
            kwargs["weather"] = get_weather(city_code)
    return render_template('board.html', **kwargs)
