import time
import pigpio

class IrReader:
    # Constructor
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.pi = pigpio.pi()
        self.onPulses = []
        self.offPulses = []

        self.t1 = None
        self.t2 = None

        self.logger.info('Creating IR Reader on gpio %d', self.config['gpioId'])

        self.pi.set_mode(self.config['gpioId'], pigpio.INPUT)

    # Interrupt callback
    def _intCallback(self, gpio, level, tick):
        self.logger.debug('Interrupt generated on %d, at level %d, on %d tick', gpio, level, tick)

        self.t1 = self.t2
        self.t2 = tick

        if self.t1 is not None:
            if level == 1:
                self.onPulses.append(pigpio.tickDiff(self.t1, self.t2))
            else:
                self.offPulses.append(pigpio.tickDiff(self.t1, self.t2))

    # Start reading
    def _startReading(self):
        self.logger.debug('Starting to read IR codes')
        self.readingCallback = self.pi.callback(self.config['gpioId'], pigpio.EITHER_EDGE, self._intCallback)

    # Stop reading
    def _stopReading(self):
        self.logger.debug('Stopping to readin IR codes')
        self.readingCallback.cancel()
        self.t1 = None
        self.t2 = None

    # Forming bits
    def _formingBits(self):
        pulseNumber = len(self.onPulses) if len(self.onPulses) < len(self.offPulses) else len(self.offPulses)
        self.logger.debug('Pulses Number: %d', pulseNumber)
        return [{'onTime': self.onPulses[i], 'offTime': self.offPulses[i]} for i in range(0, pulseNumber)]

    # Finding protocol
    def _findProtocol(self):
        self.logger.debug('Trying to find protocol')

    # Averaging bit times
    def _averageBitTimes(self, bit, codeLength):
        self.logger.debug('Averaging bit times')

    # Get name
    def getName(self):
        return self.config['name']

    # Start discovering protocol
    def discoverProtocol(self):
        self.logger.info('Starting protocol discovery')
        self._startReading()
        time.sleep(10)
        self._stopReading()
        bits = self._formingBits()
        self.logger.debug('Bits')
        self.logger.debug(bits)

    # Start recording a key code
    def recordKeyCode(self, key, codeLength):
        self.logger.info('Starting to record code for %s key', key)
        self._startReading()
        time.sleep(5)
        self._stopReading()
        bits = self._formingBits()
        self.logger.debug('Bits')
        self.logger.debug(bits)
