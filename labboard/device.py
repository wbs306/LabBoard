from flask import (
    Blueprint, render_template
)
from labboard.db import query_db

bp = Blueprint("device", __name__, url_prefix="/device")

def get_ups_data():
    ups_record = query_db("SELECT * FROM UPSCollector")
    return ups_record

def get_fan_data():
    fan_record = query_db("SELECT * FROM FanCollector")
    return fan_record

def get_sensor_data():
    sensor_record = query_db("SELECT * FROM SensorCollector WHERE date > DATETIME('NOW', '-1 DAY')")
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
    return sensor_data

@bp.route("/getSensorCard", methods=["GET", "POST"])
def get_sensor_card():
    return render_template("sensor_card.html", **{"sensor_data": get_sensor_data()})