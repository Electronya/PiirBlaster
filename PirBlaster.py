from flask import Flask, Response, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_jsonpify import jsonify
from flask_cors import CORS

import paho.mqtt.client as mqtt

import logging

from irReader import IrReader
from remote import Protocol, Remote

# Setting up app
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
socketio = SocketIO(app)
app.logger.info('App setup done')

manufacturers = Remote.listManufacturer(app.logger)
for manufacturer in manufacturers:
    remotes = Remote.listRemote(manufacturer, app.logger)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000, debug=False, threaded=True)
