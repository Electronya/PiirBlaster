from flask import Flask, Response, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_jsonpify import jsonify
from flask_cors import CORS

import logging
import json
import os
import signal

from device import Device
from serviceAdvertiser import ServiceAdvertiser

# Setting up app
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
socketio = SocketIO(app, cors_allowed_origins="*")
app.logger.info('App setup done')

# Loading configs
mqttConfig = None
devicesConfig = None

mqttConfigFile = os.path.join('./', 'config', 'service', 'mqtt.json')
with open(mqttConfigFile) as configFile:
    mqttConfig = json.loads(configFile.read())

devicesConfigFile = os.path.join('./', 'config', 'service', 'devices.json')
with open(devicesConfigFile) as configFile:
    devicesConfig = json.loads(configFile.read())

# Waiting for the broker to be available
app.logger.info(f"Checking if broker is reachable")
brokerIsAvailable = False
while not brokerIsAvailable:
    brokerIsAvailable = True if os.system(f"ping -c 1 {mqttConfig['broker']['ip']}") is 0 else False
    if not brokerIsAvailable:
        app.logger.warning(f"Broker not reachable yet")

# Creating devices
devices = []
for deviceConfig in devicesConfig:
    devices.append(Device(app.logger, mqttConfig, deviceConfig))

# Creating the service advertiser
svcAdvertiser = ServiceAdvertiser(app.logger)
signal.signal(signal.SIGINT, svcAdvertiser.stopAdvertising)
signal.signal(signal.SIGTERM, svcAdvertiser.stopAdvertising)
# signal.signal(signal.SIGKILL, svcAdvertiser.stopAdvertising)

#
# Websocket API
#
@socketio.on('connect')
def onConnect():
    app.logger.info(f"websocket.api: New client connected {request.remote_addr}")
    emit('apiStatus', {'result': 'success', 'message': 'connected'})

@socketio.on('disconnect')
def onDisconnet():
    app.logger.info(f"websocket.api: Client {request.remote_addr} disconnected")

@socketio.on('getManufacturersList')
def onGetManufsList(payload):
    app.logger.info(f"websocket.api: Received getManufacturersList message from {request.remote_addr}")
    app.logger.debug(payload)
    emit('manufacturersList', {'result': 'success', 'manufacturers': listManufacturers()})

@socketio.on('getCommandSetsList')
def onGetCmdSetsList(payload):
    app.logger.info(f"websocket.api: Received getCommandSetsList message from {request.remote_addr}")
    app.logger.debug(payload)
    emit('commandSets', {'result': 'success', 'commandSets': listCommandSets(payload['manufacturer'])})

@socketio.on('getDevicesList')
def onGetDevicesList(payload):
    app.logger.info(f"websocket.api: Received getDevicesList message from {request.remote_addr}")
    app.logger.debug(payload)
    emit('devicesList', {'result': 'success', 'devices': devicesConfig})

@socketio.on('addDevice')
def onAddDevice(payload):
    result = {'result': 'fail'}
    app.logger.info(f"websocket.api: Received addDevice message from {request.remote_addr}")
    app.logger.debug(payload['newDevConfig'])
    if filterDevice(payload['newDevConfig']) is None:
        devicesConfig.append(payload['newDevConfig'])
        devices.append(Device(app.logger, mqttConfig, payload['newDevConfig'], isNew=True))
        result['newDevice'] = devicesConfig[-1]
    else:
        result['message'] = f"Device {payload['newDevConfig']['location']}.{payload['newDevConfig']['name']} already exists!!"
    emit('deviceAdded', result)


@socketio.on('updateDevice')
def onUpdateDevice(payload):
    resPayload= {'result': 'success'}
    app.logger.info(f"websocket.api: Received updateDevice message from {request.remote_addr}")
    app.logger.debug(payload)
    devToUpdate = filterDevice(payload['updatedDevConfig'])
    if devToUpdate is not None:
        devToUpdate.setConfig(payload)
        resPayload['newConfig'] = devToUpdate.getConfig()
    else:
        resPayload['result'] = 'fail'
        resPayload['message'] = 'Device not found!!'
    emit('deviceUpdated', resPayload)

@socketio.on('saveDevCongig')
def onSaveDevConfig(payload):
    resPayload = {'result': 'fail'}
    app.logger.info(f"websocket.api: Received saveDeviceConfig message from {request.remote_addr}")
    app.logger.debug(payload)
    devToSave = filterDevice(payload['deviceToSave'])
    if devToSave is not None:
        resPayload = devToSave.saveConfig()
    else:
        resPayload['message'] = 'Device not found!!'
    emit('devConfigSaved', resPayload)

@socketio.on('saveDevCommandSet')
def onSaveDevCommandSet(payload):
    resPayload = {'result': 'fail'}
    app.logger.info(f"websocket.api: Received saveDevCommandSet message from {request.remote_addr}")
    app.logger.debug(payload)
    devToSave = filterDevice(payload['deviceToSave'])
    if devToSave is not None:
        resPayload = devToSave.saveCommandSet()
    else:
        resPayload['message'] = 'Device not found!!'
    emit('devCmdSetSaved', resPayload)

#
# Utilities Function
#
def filterDevice(devInfo):
    app.logger.debug(f"utils.filterDevice: Filtering device {devInfo['location']}.{devInfo['name']}")
    filterItr = filter(lambda device: device.getConfig()['name'] == devInfo['name'] and
        device.getConfig()['location'] == devInfo['location'], devices)
    return next(filterItr, None)

def listManufacturers():
    manufacturers = []
    app.logger.debug(f"utils.listManufacturers: Getting manufacturers list")
    for r, d, f in os.walk('./commandSets'):
        app.logger.debug(f"utils.listManufacturer: Listing manufacturers in {r}")
        for manufacturer in d:
            manufacturers.append(manufacturer)
    return manufacturers

def listCommandSets(manufacturer):
    commandSets = []
    app.logger.debug(f"utils.listCommandSets: Getting commandSets list for {manufacturer}")
    for r, d, f in os.walk(os.path.join('./commandSets', manufacturer)):
        app.logger.debug(f"utils.listCommandSets: Listing command sets in {r}")
        app.logger.debug(f)
        for commandSet in f:
            app.logger.debug(commandSet)
            commandSets.append(commandSet[:-5])
    return commandSets

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000, debug=False, threaded=True)
