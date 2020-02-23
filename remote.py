import os
import json

PROTOCOL_DIR = './remotes/protocols/'
REMOTE_DIR = './remotes/'

class Protocol:
    # Constructor
    def __init__(self, logger, name=None, descriptorFilePath=None):
        self.logger = logger
        self.descriptor = {}
        if name is not None:
            self.logger.info('Creating new Protocol %s', name)
            self.descriptor['name'] = name
            self.descriptorFilePath = os.path.join(PROTOCOL_DIR, self.descriptor['name'] + '.json')
        elif descriptorFilePath is not None:
            self.logger.info('Loading existing protocol from %s', descriptorFilePath)
            self.descriptorFilePath = descriptorFilePath
            with open(self.descriptorFilePath) as descriptorFile:
                self.descriptor = json.loads(descriptorFile.read())
        self.logger.debug('Protocol descriptor:\n%s', self.descriptor)

    # Set protocol name
    def setName(self, name):
        self.descriptor['name'] = name

    # Get protocol name
    def getName(self):
        return self.descriptor['name']

    # Set protocol start bit
    def setStartBit(self, startBit):
        self.descriptor['startBit'] = startBit

    # Get protocol start bit
    def getStartBit(self):
        if 'startBit' in self.descriptor:
            return self.descriptor['startBit']
        else:
            return None

    # Set protocol zero bit
    def setZeroBit(self, zeroBit):
        self.descriptor['zero'] = zeroBit

    # Get protocol zero bit
    def getZeroBit(self):
        return self.descriptor['zero']

    # Set protocol one bit
    def setOneBit(self, oneBit):
        self.descriptor['one'] = oneBit

    # Get protocol one bit
    def getOneBit(self):
        return self.descriptor['one']

    # Set protocol stop bit
    def setStopBit(self, stopBit):
        self.descriptor['stopBit'] = stopBit

    # Get protocol stop bit
    def getStopBit(self):
        if 'startBit' in self.descriptor:
            return self.descriptor['stopBit']
        else:
            return None

    # Set protocol gap
    def setGap(self, gap):
        self.descriptor['gap'] = gap

    # Get protocol gap
    def getGap(self):
        return self.descriptor['gap']

    # Set protocol header size
    def setHeaderSize(self, headerSize):
        self.descriptor['headerSize'] = headerSize

    # Get protocol header size
    def getHeaderSize(self):
        return self.descriptor['headerSize']

    # Set protocol data size
    def setDataSize(self, dataSize):
        self.descriptor['dataSize'] = dataSize

    # Get protocol data size
    def getDataSize(self):
        return self.descriptor['dataSize']

    # Set protocol footer size
    def setFooterSize(self, footerSize):
        self.descriptor['footerSize'] = footerSize

    # Get protocol footer size
    def getFooterSize(self):
        return self.descriptor['footerSize']

    # Save protocol
    def save(self):
        self.logger.info('Saving protocol %s', self.descriptorFilePath)
        with open(self.descriptorFilePath, 'w') as descriptorFile:
            jsonDescriptor = json.dumps(self.descriptor, sort_keys=True, indent=2)
            self.logger.debug('Protocol descriptor:\n%s', jsonDescriptor)
            descriptorFile.write(jsonDescriptor)

    # List available protocol descriptor files
    @staticmethod
    def listDescriptorFiles(logger):
        logger.info('Listing supported protocols')
        descriptorFiles =[]
        with os.scandir(PROTOCOL_DIR) as entries:
            for entry in entries:
                logger.debug('Protocol: %s found', entry.path)
                descriptorFiles.append(entry.path)
        return descriptorFiles

class Remote:
    # Constructor
    def __init__(self, logger, manufacturer, model, protocol=None, isNew=False):
        self.logger = logger
        self.descriptor = {}
        self.descriptorFilePath = os.path.join(REMOTE_DIR, manufacturer, model + '.json')
        if isNew:
            self.logger.info('Creating new remote %s from %s', model, manufacturer)
            self.descriptor['manufacturer'] = manufacturer
            self.descriptor['model'] = model
            self.descriptor['keyCodes'] = {}
            if protocol is not None:
                self.descriptor['protocol'] = protocol
        else:
            self.logger.info('Loading remote %s from %s', model, manufacturer)
            with open(self.descriptorFilePath) as descriptorFile:
                self.descriptor = json.loads(descriptorFile.read())
            self.protocol = Protocol(self.logger, os.path.join(PROTOCOL_DIR, self.descriptor['protocol'] + '.json'))
        self.logger.debug('Remote descriptor:\n%s', self.descriptor)

    # Set model
    def setModel(self, model):
        self.descriptor['model'] = model

    # Get model
    def getModel(self):
        return self.descriptor['model']

    # Set manufacturer
    def setManufacturer(self, manufacturer):
        self.descriptor['manufacturer'] = manufacturer

    # Get manufacturer
    def getManufacturer(self):
        return self.descriptor['manufacturer']

    # Set header
    def setHeader(self, header):
        self.descriptor['header'] = f'0x{header:0>4X}'

    # Get header
    def getHeader(self):
        if 'header' in self.descriptor:
            return int(self.descriptor['header'], 16)
        else:
            return None

    # Set footer
    def setFooter(self, footer):
        self.descriptor['footer'] = f'0x{footer:0>4X}'

    # Get footer
    def getFooter(self):
        if 'footer' in self.descriptor:
            return int(self.descriptor['footer'], 16)
        else:
            return None

    # Set key code
    def setKeyCode(self, key, code):
        self.descriptor['keyCodes'][key] = f'{code:0>4X}'

    # Get key code
    def getKeyCode(self, key):
        if key in self.descriptor['keyCodes']:
            return int(self.descriptor['keyCodes'][key], 16)
        else:
            return None

    # Save remote
    def save(self):
        self.logger.info('Saving remote model %s from %s', self.descriptor['model'], self.descriptor['manufacturer'])
        with open(self.descriptorFilePath, 'w') as descriptorFile:
            jsonDescriptor = json.dumps(self.descriptor, sort_keys=True, indent=2)
            self.logger.debug('Remote descriptor:\n%s', jsonDescriptor)
            descriptorFile.write(jsonDescriptor)

    # List manufacturer
    @staticmethod
    def listManufacturer(logger):
        logger.info('Listing all manufacturers')
        manufacturers = []
        with os.scandir(REMOTE_DIR) as entries:
            for entry in entries:
                if entry.name != 'protocols':
                    manufacturers.append(entry.name)
        logger.debug('Manufacturers list:\n%s', manufacturers)
        return manufacturers

    # List remote from manufacturer
    @staticmethod
    def listRemote(manufacturer, logger):
        logger.info('Listing all remotes from %s', manufacturer)
        remotes = []
        with os.scandir(os.path.join(REMOTE_DIR, manufacturer)) as entries:
            for entry in entries:
                remotes.append(entry.name.replace('.json', ''))
        logger.debug('Remotes list from %s:\n%s', manufacturer, remotes)
        return remotes
