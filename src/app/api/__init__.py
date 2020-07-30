from flask import request
from flask_socketio import emit

from .. import socketio
from .. import logger
from .. import devManager

MODULE_ID = 'socketio.api'

#
# Websocket API
#
@socketio.on('connect')
def onConnect():
    logger.info(f"{MODULE_ID}: New client connected {request.remote_addr}")
    emit('apiStatus', {'result': 'success', 'message': 'connected'})

@socketio.on('disconnect')
def onDisconnet():
    logger.info(f"{MODULE_ID}: Client {request.remote_addr} disconnected")

@socketio.on('getManufacturersList')
def onGetManufsList(payload):
    logger.info(f"{MODULE_ID}: Received getManufacturersList message from {request.remote_addr}")
    logger.debug(payload)
    emit('manufacturersList', {'result': 'success', 'manufacturers': devManager.listManufacturers()})

@socketio.on('getCommandSetsList')
def onGetCmdSetsList(payload):
    logger.info(f"{MODULE_ID}: Received getCommandSetsList message from {request.remote_addr}")
    logger.debug(payload)
    emit('commandSets', {'result': 'success', 'commandSets': devManager.listCommandSets(payload['manufacturer'])})

@socketio.on('getDevicesList')
def onGetDevicesList(payload):
    logger.info(f"{MODULE_ID}: Received getDevicesList message from {request.remote_addr}")
    logger.debug(payload)
    emit('devicesList', {'result': 'success', 'devices': devicesConfig})

@socketio.on('addDevice')
def onAddDevice(payload):
    result = {'result': 'fail'}
    logger.info(f"{MODULE_ID}: Received addDevice message from {request.remote_addr}")
    logger.debug(payload['newDevConfig'])
    if utils.filterDevice(payload['newDevConfig']) is None:
        devicesConfig.append(payload['newDevConfig'])
        devices.append(Device(logger, mqttConfig, payload['newDevConfig'], isNew=True))
        result['newDevice'] = devicesConfig[-1]
    else:
        result['message'] = f"Device {payload['newDevConfig']['location']}.{payload['newDevConfig']['name']} already exists!!"
    emit('deviceAdded', result)


@socketio.on('updateDevice')
def onUpdateDevice(payload):
    resPayload= {'result': 'success'}
    logger.info(f"{MODULE_ID}: Received updateDevice message from {request.remote_addr}")
    logger.debug(payload)
    devToUpdate = utils.filterDevice(payload['updatedDevConfig'])
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
    logger.info(f"{MODULE_ID}: Received saveDeviceConfig message from {request.remote_addr}")
    logger.debug(payload)
    devToSave = utils.filterDevice(payload['deviceToSave'])
    if devToSave is not None:
        resPayload = devToSave.saveConfig()
    else:
        resPayload['message'] = 'Device not found!!'
    emit('devConfigSaved', resPayload)

@socketio.on('saveDevCommandSet')
def onSaveDevCommandSet(payload):
    resPayload = {'result': 'fail'}
    logger.info(f"{MODULE_ID}: Received saveDevCommandSet message from {request.remote_addr}")
    logger.debug(payload)
    devToSave = utils.filterDevice(payload['deviceToSave'])
    if devToSave is not None:
        resPayload = devToSave.saveCommandSet()
    else:
        resPayload['message'] = 'Device not found!!'
    emit('devCmdSetSaved', resPayload)
