from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

import logging

from .config import Config
from .device import DeviceManager

socketio = SocketIO(cors_allowed_origins="*")

logger = None
devManager = None

def createApp(debug=False):
    # Setting up app
    app = Flask(__name__)
    app.debug = debug
    logger = app.logger

    # Load configuration
    appConfig = Config(logger)

    # Load devices
    devManager = DeviceManager(logger, appConfig)

    # Setup configuration API
    from . import api

    socketio.init_app(app)
    logger.info('App setup done')

    return app
