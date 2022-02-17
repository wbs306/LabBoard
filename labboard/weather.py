import json
from threading import stack_size

from flask import (
    Blueprint, current_app, render_template, request, jsonify
)

bp = Blueprint("weather", __name__, url_prefix="/weather")

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
            json.dump({"city_code": city_code}, f)

    daily_weather = daily(city_code)["daily"][0]
    now_weather = now(city_code)["now"]
    state_dict = {
        "temp": now_weather["temp"],
        "icon": now_weather["icon"],
        "text": now_weather["text"],
        "feelsLike": now_weather["feelsLike"],
        "tempMax": daily_weather["tempMax"],
        "tempMin": daily_weather["tempMin"]
    }
    if (request.method == "POST"):
        return render_template("weather.html", **{"weather": state_dict})
    else:
        return state_dict
