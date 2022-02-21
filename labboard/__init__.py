import os
from datetime import datetime

from flask import Flask
from . import QWeather

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'test.db'),
        RECORD_FILE=os.path.join(app.instance_path, 'record.json'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.template_global("format_date")
    def format_date(date):
        return datetime.fromtimestamp(int(date))

    from . import board
    app.register_blueprint(board.bp)

    from . import express
    app.register_blueprint(express.bp)

    from . import weather
    app.register_blueprint(weather.bp)
    with open(os.path.join(app.instance_path, 'qweather_key.key')) as f:
        weather.init_app(QWeather.QWeather(f.read()))

    from . import device
    app.register_blueprint(device.bp)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app