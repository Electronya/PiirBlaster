import logging
from unittest import TestCase
from unittest.mock import Mock, patch

from ircodec.command import CommandSet
import paho.mqtt.client as mqtt

import os
import sys
sys.path.append(os.path.abspath('./src'))

from config import Config                                   # noqa: E402
from device.Device import Device                            # noqa: E402
from exceptions import CommandNotFound                      # noqa: E402


class TestDevice(TestCase):
    """
    Device class test cases.
    """
    def setUp(self):
        """
        Test case setup.
        """
        self.deviceConfig = {
            'name': 'testDev',
            'location': 'testLocation',
            'linkedEmitter': 'OUT0',
            'commandSet': {
                'model': 'testModel',
                'manufacturer': 'testManufacturer',
                'description': 'My test device ',
                'emitterGpio': 3,
                'receiverGpio': 6,
                'packetGap': 0.01
            },
            'topicPrefix': 'testPrefix',
            'lastWill': {
                'qos': 2,
                'retain': True
            }
        }

        self.baseTopic = f"{self.deviceConfig['topicPrefix']}/{self.deviceConfig['location']}/{self.deviceConfig['name']}/"     # noqa: E501

        self.mockedAppConfig = Mock(spec_set=Config)
        self.mockedAppConfig.getUserName.return_value = 'username'
        self.mockedAppConfig.getUserPassword.return_value = 'password'
        self.mockedAppConfig.getBrokerHostname.return_value = 'host'
        self.mockedAppConfig.getBrokerPort.return_value = 2000

        self.mockedClient = Mock(spec_set=mqtt.Client)

        self.mockedCmdSet = Mock(spec_set=CommandSet)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_constructorNewDevice(self, mockedClient, mockedCmdSet):
        """
        The constructor must create a new command set based on the device
        configuration when the isNew flag is True.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        name = self.deviceConfig['commandSet']['model']
        emitter = self.deviceConfig['commandSet']['emitterGpio']
        receiver = self.deviceConfig['commandSet']['receiverGpio']
        description = self.deviceConfig['commandSet']['description']
        device = Device(logging, self.mockedAppConfig,      # noqa: F841
                        self.deviceConfig, isNew=True)
        mockedCmdSet.assert_called_once_with(name, emitter_gpio=emitter,
                                             receiver_gpio=receiver,
                                             description=description)

    @patch('device.Device.CommandSet.load')
    @patch('device.Device.mqtt.Client')
    def test_constructorLoadDevice(self, mockedClient, mockedCmdSetLoad):
        """
        The constructor must load an existing command set when the
        isNew flag is Flase.
        """
        mockedClient.side_effect = [self.mockedClient]
        manufacturer = self.deviceConfig['commandSet']['manufacturer']
        model = self.deviceConfig['commandSet']['model']
        device = Device(logging, self.mockedAppConfig,      # noqa: F841
                        self.deviceConfig)
        mockedCmdSetLoad.assert_called_once_with(f"./commandSets/"
                                                 f"{manufacturer}"
                                                 f"/{model}.json")

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    @patch('device.Device.Device._initMqttClient')
    def test_constructorInitMqttClient(self, mockedClientInit,
                                       mockedClient, mockedCmdSet):
        """
        The constructor must initialize the MQTT client with the appropriate
        broker/user information.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        username = self.mockedAppConfig.getUserName()
        password = self.mockedAppConfig.getUserPassword()
        hostname = self.mockedAppConfig.getBrokerHostname()
        port = self.mockedAppConfig.getBrokerPort()
        device = Device(logging, self.mockedAppConfig,      # noqa: F841
                        self.deviceConfig, isNew=True)
        mockedClientInit.assert_called_once_with(username, password,
                                                 hostname, port)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__initMqttClientClientId(self, mockedClient, mockedCmdset):
        """
        The _initMqttClient (called by the constructor) method must initialize
        the MQTT client with the correct client ID.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdset.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,      # noqa: F841
                        self.deviceConfig, isNew=True)
        mockedClient.assert_called_once_with(client_id=f"{self.deviceConfig['location']}."      # noqa: E501
                                             f"{self.deviceConfig['name']}")

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__initMqttClientEventCallbacks(self, mockedClient, mockedCmdSet):
        """
        The _initMqttClient (called by the constructor) method must initialize
        the client event callbacks.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        self.assertEqual(device.client.on_connect, device._on_connect,
                         'Device _initClient method failed to initialize '
                         'the client event callbacks.')
        self.assertEqual(device.client.on_disconnect, device._on_disconnect,
                         'Device _initClient method failed to initialize '
                         'the client event callbacks.')
        self.assertEqual(device.client.on_message, device._on_message,
                         'Device _initClient method failed to initialize '
                         'the client event callbacks.')
        self.assertEqual(device.client.on_publish, device._on_publish,
                         'Device _initClient method failed to initialize '
                         'the client event callbacks.')
        self.assertEqual(device.client.on_subscribe, device._on_subscribe,
                         'Device _initClient method failed to initialize '
                         'the client event callbacks.')
        self.assertEqual(device.client.on_log, device._on_log,
                         'Device _initClient method failed to initialize'
                         'the client event callbacks.')

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__initMqttClientLastWill(self, mockedClient, mockedCmdSet):
        """
        The _initMqttClient (called by the constructor) method must initialize
        the client last will.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        willTopic = f"{self.baseTopic}{device.STATUS_TOPIC}"
        qos = self.deviceConfig['lastWill']['qos']
        retain = self.deviceConfig['lastWill']['retain']
        self.mockedClient.will_set.assert_called_once_with(willTopic,
                                                           device.OFFLINE_MSG,
                                                           qos, retain)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__initMqttClientUserPassword(self, mockedClient, mockedCmdSet):
        """
        The _initMqttClient (called by the constructor) method must initialize
        the client username and password.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,      # noqa: F841
                        self.deviceConfig, isNew=True)
        username = self.mockedAppConfig.getUserName()
        password = self.mockedAppConfig.getUserPassword()
        self.mockedClient.username_pw_set.assert_called_once_with(username,
                                                                  password)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__initMqttClientConnect(self, mockedClient, mockedCmdSet):
        """
        The _initMqttClient (called by the constructor) method must connect
        the client to the appropriate broker.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,      # noqa: F841
                        self.deviceConfig, isNew=True)
        hostname = self.mockedAppConfig.getBrokerHostname()
        port = self.mockedAppConfig.getBrokerPort()
        self.mockedClient.connect.assert_called_once_with(hostname, port=port)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__publishCmdResultSuccess(self, mockedClient, mockedCmdSet):
        """
        The _publishCmdResult method must publish the success message
        when the success flag is true.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device._publishCmdResult(True)
        topic = f"{self.baseTopic}{device.RESULT_TOPIC}"
        self.mockedClient.publish.assert_called_once_with(topic, payload=device.SUCCESS_MSG)    # noqa: E501

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__publishCmdResultError(self, mockedClient, mockedCmdSet):
        """
        The _publishCmdResult method must publish the error message
        when the success flag is false.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device._publishCmdResult(False)
        topic = f"{self.baseTopic}{device.RESULT_TOPIC}"
        self.mockedClient.publish.assert_called_once_with(topic, payload=device.ERROR_MSG)    # noqa: E501

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__on_connectPublishStatus(self, mockedClient, mockedCmdSet):
        """
        The _on_connect method must pubish the online status of the device.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device._on_connect(None, None, None, None)
        topic = f"{self.baseTopic}{device.STATUS_TOPIC}"
        self.mockedClient.publish.assert_called_once_with(topic, payload=device.ONLINE_MSG,     # noqa: E501
                                                          qos=1, retain=True)                   # noqa: E501

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__on_connectSubscribeCmd(self, mockedClient, mockedCmdSet):
        """
        The _on_connect method must subscribe to the command topic.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device._on_connect(None, None, None, None)
        topic = f"{self.baseTopic}{device.CMD_TOPIC}"
        self.mockedClient.subscribe.assert_called_once_with(topic)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__on_disconnect(self, mockedClient, mockedCmdSet):
        """
        The _on_disconnect method does not do much.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device._on_disconnect(None, None, None)
        self.assertTrue(True)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    @patch('device.Device.Device._publishCmdResult')
    def test__on_messageCmdNotSupported(self, mockedPubCmdResult,
                                        mockedClient, mockedCmdSet):
        """
        The _on_message method must publish the error message on
        the result topic.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        self.mockedCmdSet.emit.side_effect = [KeyError()]
        msg = Mock()
        msg.payload.decode.return_value = 'not supported command'
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device._on_message(None, None, msg)
        mockedPubCmdResult.assert_called_once_with(False)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    @patch('device.Device.Device._publishCmdResult')
    def test__on_messageEmitCommand(self, mockedPubCmdResult,
                                    mockedClient, mockedCmdSet):
        """
        The _on_message method must emit 4 times the desired command.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        msg = Mock()
        msg.payload.decode.return_value = 'supported command'
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device._on_message(None, None, msg)
        self.assertEqual(self.mockedCmdSet.emit.call_count, 4,
                         'Device _on_message failed to emit 4 times '
                         'the command')
        self.mockedCmdSet.emit.assert_called_with('supported command',
                                                  emit_gap=self.deviceConfig['commandSet']['packetGap'])     # noqa: E501

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    @patch('device.Device.Device._publishCmdResult')
    def test__on_messagePubSuccess(self, mockedPubCmdResult,
                                   mockedClient, mockedCmdSet):
        """
        The _on_message method must publish the success message when
        the command emit operation succeed.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        msg = Mock()
        msg.payload.decode.return_value = 'supported command'
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device._on_message(None, None, msg)
        mockedPubCmdResult.assert_called_once_with(True)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__on_publish(self, mockedClient, mockedCmdSet):
        """
        The _on_publish method does not do much.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device._on_publish(None, None, None)
        self.assertTrue(True)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__on_subscribe(self, mockedClient, mockedCmdSet):
        """
        The _on_subscribe method does not do much.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device._on_subscribe(None, None, None, None)
        self.assertTrue(True)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test__on_log(self, mockedClient, mockedCmdSet):
        """
        The _on_log method does not do much.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device._on_log(None, None, mqtt.MQTT_LOG_INFO, None)
        self.assertTrue(True)

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_startLoop(self, mockedClient, mockedCmdSet):
        """
        The startLoop method must start the client network loop.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device.startLoop()
        self.mockedClient.loop_start.assert_called_once()

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_stopLoop(self, mockedClient, mockedCmdSet):
        """
        The stopLoop method must stop the client network loop
        and disconnect the client.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device.stopLoop()
        self.mockedClient.loop_stop.assert_called_once()
        self.mockedClient.disconnect.assert_called_once()

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_getName(self, mockedClient, mockedCmdSet):
        """
        The getName method must return the name of the device.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        name = device.getName()
        self.assertEqual(name, self.deviceConfig['name'],
                         'Device getName failed to return the'
                         'device name.')

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_getLocation(self, mockedClient, mockedCmdSet):
        """
        The getLocation method must return the location of the device.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        location = device.getLocation()
        self.assertEqual(location, self.deviceConfig['location'],
                         'Device getLocation failed to return the'
                         'device location.')

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_getConfig(self, mockedClient, mockedCmdSet):
        """
        The getConfig method must return the configuration of the device.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        configuration = device.getConfig()
        self.assertEqual(configuration, self.deviceConfig,
                         'Device getConfig failed to return the'
                         'device configuration.')

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_setConfig(self, mockedClient, mockedCmdSet):
        """
        The setConfig method must update the configuration of the device.
        """
        newConfig = {
            'name': 'newDev',
            'location': 'newLocation',
            'linkedEmitter': 'OUT0',
            'commandSet': {
                'model': 'newModel',
                'manufacturer': 'newManufacturer',
                'description': 'My new device ',
                'emitterGpio': 3,
                'receiverGpio': 6,
                'packetGap': 0.01
            },
            'topicPrefix': 'newPrefix',
            'lastWill': {
                'qos': 2,
                'retain': True
            }
        }
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device.setConfig(newConfig)
        configuration = device.getConfig()
        self.assertEqual(configuration, newConfig,
                         'Device setConfig failed to return the'
                         'device configuration.')

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_getCommandList(self, mockedClient, mockedCmdSet):
        """
        The getCommandList method must return the list of command
        supported by the device.
        """
        cmdSetJson = {
            "type": "CommandSet",
            "name": "rm-s103",
            "emitter_gpio": 22,
            "receiver_gpio": 11,
            "commands": {
                "power": {},
                "volumeUp": {},
                "volumeDown": {},
                "channelUp": {},
                "channelDown": {}
            }
        }
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        self.mockedCmdSet.to_json.return_value = cmdSetJson
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        commandList = device.getCommandList()
        self.assertEqual(commandList, cmdSetJson['commands'].keys(),
                         'Device getCommandList failed to return the device'
                         'supported command list.')

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_addCommandCmdSetAdd(self, mockedClient, mockedCmdSet):
        """
        The addCommand method must call the add method of the command set
        with the new command name and derscription.
        """
        newCmdName = 'new command'
        newCmdDescription = 'description of new command'
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device.addCommand(newCmdName, newCmdDescription)
        self.mockedCmdSet.add.assert_called_once_with(newCmdName,
                                                      description=newCmdDescription)    # noqa: E501

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_deleteCommandCmdNotFound(self, mockedClient, mockedCmdSet):
        """
        The deleteCommand must raise a CommandNotFound error if the command to
        be deleted is not supported.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        commandName = 'not supported command'
        self.mockedCmdSet.remove.side_effect = KeyError()
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        with self.assertRaises(CommandNotFound) as context:
            device.deleteCommand(commandName)
            self.assertTrue(f"command {commandName} not supported."
                            in str(context.exception),
                            'Device deleteCommand failed to raise a '
                            'CommandNotFound error when the command '
                            'to be deleted is not supported.')

    @patch('device.Device.CommandSet')
    @patch('device.Device.mqtt.Client')
    def test_deleteCommandRemove(self, mockedClient, mockedCmdSet):
        """
        The deleteCommand must call the command set remove method.
        """
        mockedClient.side_effect = [self.mockedClient]
        mockedCmdSet.side_effect = [self.mockedCmdSet]
        commandName = 'supported command'
        device = Device(logging, self.mockedAppConfig,
                        self.deviceConfig, isNew=True)
        device.deleteCommand(commandName)
        self.mockedCmdSet.remove.assert_called_once_with(commandName)
