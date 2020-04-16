from flask import Flask, Response, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_jsonpify import jsonify
from flask_cors import CORS

import logging
import json
import os

from device import Device

# Setting up app
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
socketio = SocketIO(app)
app.logger.info('App setup done')

# Loading configs
mqttConfig = None
devicesConfig = None

mqttConfigFile = os.path.join('./', 'config', 'mqtt.json')
with open(mqttConfigFile) as configFile:
    mqttConfig = json.loads(configFile.read())

devicesConfigFile = os.path.join('./', 'config', 'devices.json')
with open(devicesConfigFile) as configFile:
    devicesConfig = json.loads(configFile.read())

# Creating devices
devices = []
for deviceConfig in devicesConfig:
    devices.append(Device(app.logger, mqttConfig, deviceConfig))

# For Hardware test
# from ircodec.command import CommandSet
# controller = CommandSet('test', emitter_gpio=22, receiver_gpio=11, description='Test')
# controller.add('power')
# controller = CommandSet.load('test.json')
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.emit('power', emit_gap=0.01)
# controller.save_as('test.json')

from irEmitter import IrEmitter
# emitter = IrEmitter({"name": "OUT3", "gpioId": 22}, app.logger)
# emitter.addBit(2400, 590)
# emitter.addBit(1200, 590)
# emitter.addBit(590, 590)
# emitter.addBit(1200, 590)
# emitter.addBit(590, 590)
# emitter.addBit(1200, 590)
# emitter.addBit(590, 590)
# emitter.addBit(590, 590)
# emitter.addBit(590, 590)
# emitter.addBit(590, 590)
# emitter.addBit(590, 590)
# emitter.addBit(590, 590)
# emitter.addBit(1200, 590)
# emitter.addGap(10800)
# emitter.sendCommand(0.5)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000, debug=False, threaded=True)
