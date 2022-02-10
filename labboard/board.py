import json
import os

from flask import (
    Blueprint, render_template, request, jsonify, current_app
)
from labboard.db import get_db

bp = Blueprint('board', __name__, url_prefix="/board")

def get_weather_state_dict(now_weather, daily_weather):
    return {
        "temp": now_weather["temp"],
        "icon": now_weather["icon"],
        "text": now_weather["text"],
        "feelsLike": now_weather["feelsLike"],
        "tempMax": daily_weather["tempMax"],
        "tempMin": daily_weather["tempMin"]
    }

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
        from labboard.QWeather import daily, now
        with open(current_app.config["RECORD_FILE"], "r") as f:
            city_code = json.load(f)["city_code"]
            daily_weather = daily(city_code)["daily"][0]
            now_weather = now(city_code)["now"] 
            kwargs["weather"] = get_weather_state_dict(now_weather, daily_weather)
    return render_template('board.html', **kwargs)

@bp.route('/getLocation', methods=['POST'])
def get_location():
    from labboard.QWeather import get_city
    if (request.method == "POST"):
        location = request.form["location"]
    
    return jsonify(get_city(location))

@bp.route('/getWeatherState', methods=['POST'])
def get_weather(city_code=None):
    from labboard.QWeather import daily, now
    if (request.method == "POST"):
        city_code = request.form["cityCode"]

    with open(current_app.config["RECORD_FILE"], "w+") as f:
        json.dump({
            "city_code": city_code
        }, f)

    daily_weather = daily(city_code)["daily"][0]
    now_weather = now(city_code)["now"]
    return jsonify(get_weather_state_dict(now_weather, daily_weather))
