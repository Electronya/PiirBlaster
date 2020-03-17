import time

import pigpio

FREQUENCY = 38

class IrEmitter:
    # Constructor
    def __init__(self, config, logger):
        self.logger = logger
        self.logger.info('Creating IR emitter on gpio %d', config['gpioId'])
        self.config = config
        self.pi = pigpio.pi()
        self.cmdWaveform = []

        self.pi.set_mode(self.config['gpioId'], pigpio.OUTPUT)

    # Generate carrier of micro second length
    def _generateCarrier(self, microsec):
        self.logger.debug('Generating carrier for %d us', microsec)
        waveform = []
        cycle = 1000/FREQUENCY
        cycles = int(round(microsec/cycle))
        on = int(round(cycle/3))
        sofar = 0
        for c in range(cycles):
            target = int(round((c+1)*cycle))
            sofar += on
            off = target - sofar
            sofar += off
            waveform.append(pigpio.pulse(1<<self.config['gpioId'], 0, on))
            waveform.append(pigpio.pulse(0, 1<<self.config['gpioId'], off))
        return waveform

    # Get name
    def getName(self):
        return self.config['name']

    # Add bit to waveform
    def addBit(self, onTime, offTime):
        self.logger.debug('Adding bit with on time: %d us and off time %d us to waveform', onTime, offTime)
        self.cmdWaveform += self._generateCarrier(onTime)
        self.cmdWaveform.append(pigpio.pulse(0, 1<<self.config['gpioId'], offTime))

    # Add gap
    def addGap(self, gapTime):
        self.logger.debug('Adding gap of %d us', gapTime)
        self.cmdWaveform.append(pigpio.pulse(0, 1<<self.config['gpioId'], gapTime))

    # Send command
    def sendCommand(self, pressingLength):
        self.logger.info('Sending command for %1.2f sec', pressingLength)
        self.pi.wave_add_generic(self.cmdWaveform)
        waveId = self.pi.wave_create()
        self.pi.wave_send_repeat(waveId)
        time.sleep(pressingLength)
        self.pi.wave_tx_stop()
        self.pi.wave_delete(waveId)
