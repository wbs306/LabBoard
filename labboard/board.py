import json
import os
from concurrent.futures import as_completed

from flask import (
    Blueprint, render_template, request, jsonify, current_app
)
from flask_executor import Executor
from labboard.db import query_db
from labboard.device import get_sensor_data

bp = Blueprint('board', __name__, url_prefix="/board")

@bp.route('/')
def load_board():
    sensor_data = get_sensor_data()

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
            packages = []
            if (record.get("packages")):
                packages = record["packages"]
            
            package_workers = []
            executor = Executor(current_app)
            for i in packages:
                package_workers.append(executor.submit(get_express_state, i["number"], i["company"]))

            weather_worker = executor.submit(get_weather, record["city_code"])
            kwargs["packages_info"] = [i.result() for i in as_completed(package_workers)]
            kwargs["weather"] = next(as_completed([weather_worker])).result()
    return render_template('board.html', **kwargs)
