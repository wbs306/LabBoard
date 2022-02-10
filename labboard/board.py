from flask import (
    Blueprint, render_template, request, jsonify
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

    kwargs = {
        "sensor_data": sensor_data
    }
    return render_template('board.html', **kwargs)

@bp.route('/getLocation', methods=['POST'])
def get_location():
    from labboard.QWeather import get_city
    if (request.method == "POST"):
        location = request.form["location"]
    
    return jsonify(get_city(location))