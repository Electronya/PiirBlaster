from flask import request
from flask_socketio import emit

from .. import socketio
from .. import logger
from .. import appConfig
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
    emit('devicesList', {'result': 'success', 'devices': devManager.getDevsConfigList})

@socketio.on('addDevice')
def onAddDevice(payload):
    logger.info(f"{MODULE_ID}: Received addDevice message from {request.remote_addr}")
    logger.debug(payload['newDevConfig'])
    result = devManager.addDevice(payload['newDevConfig'])
    emit('deviceAdded', result)

@socketio.on('updateDevice')
def onUpdateDevice(payload):
    result = {'result': 'success'}
    logger.info(f"{MODULE_ID}: Received updateDevice message from {request.remote_addr}")
    logger.debug(payload)
    devToUpdate = devManager.getDeviceByIdx(payload['deviceIdx'])
    if devToUpdate is not None:
        devToUpdate.setConfig(payload['updatedDevConfig'])
        result['newConfig'] = devToUpdate.getConfig()
    else:
        result['result'] = 'failed'
        result['message'] = 'Device not found!!'
    emit('deviceUpdated', result)

@socketio.on('saveDevices')
def onSaveDevices(payload):
    logger.info(f"{MODULE_ID}: Received saveDeviceConfig message from {request.remote_addr}")
    logger.debug(payload)
    result = devManager.saveDevices()
    emit('devicesSaved', result)

@socketio.on('saveDevCommandSet')
def onSaveDevCommandSet(payload):
    result = {'result': 'failed'}
    logger.info(f"{MODULE_ID}: Received saveDevCommandSet message from {request.remote_addr}")
    logger.debug(payload)
    devToSave = devManager.getDeviceByName(payload['deviceToSave']['name'],
        payload['deviceToSave']['location'])
    if devToSave is not None:
        result = devToSave.saveCommandSet()
    else:
        result['message'] = 'Device not found!!'
    emit('devCmdSetSaved', result)
