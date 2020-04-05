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
            self.logger.info(f'Creating new Protocol {name}')
            self.descriptor['name'] = name
            self.descriptorFilePath = os.path.join(PROTOCOL_DIR, self.descriptor['name'] + '.json')
        elif descriptorFilePath is not None:
            self.logger.info(f'Loading existing protocol from {descriptorFilePath}')
            self.descriptorFilePath = descriptorFilePath
            with open(self.descriptorFilePath) as descriptorFile:
                self.descriptor = json.loads(descriptorFile.read())
        self.logger.debug(f'Protocol descriptor:\n{self.descriptor}')

    # Set protocol name
    def setName(self, name):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Setting protocol name to {self.descriptor['name']}")
        self.descriptor['name'] = name

    # Get protocol name
    def getName(self):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Getting protocol {self.descriptor['name']} name")
        return self.descriptor['name']

    # Set protocol start bit
    def setStartBit(self, startBit):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Setting start bit-> {startBit}")
        self.descriptor['startBit'] = startBit

    # Get protocol start bit
    def getStartBit(self):
        if 'startBit' in self.descriptor:
            self.logger.debug(f"protocol.{self.descriptor['name']}: Getting start bit-> {self.descriptor['startBit']}")
            return self.descriptor['startBit']
        else:
            self.logger.debug(f'''protocol.{self.descriptor['name']}: No start bit''')
            return None

    # Set protocol zero bit
    def setZeroBit(self, zeroBit):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Setting zero bit-> {zeroBit}")
        self.descriptor['zero'] = zeroBit

    # Get protocol zero bit
    def getZeroBit(self):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Getting zero bit-> {self.descriptor['zero']}")
        return self.descriptor['zero']

    # Set protocol one bit
    def setOneBit(self, oneBit):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Setting one bit-> {oneBit}")
        self.descriptor['one'] = oneBit

    # Get protocol one bit
    def getOneBit(self):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Getting one bit-> {self.descriptor['one']}")
        return self.descriptor['one']

    # Set protocol stop bit
    def setStopBit(self, stopBit):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Setting stop bit-> {stopBit}")
        self.descriptor['stopBit'] = stopBit

    # Get protocol stop bit
    def getStopBit(self):
        if 'startBit' in self.descriptor:
            self.logger.debug(f"protocol.{self.descriptor['name']}: Getting stop bit-> {self.descriptor['stopBit']}")
            return self.descriptor['stopBit']
        else:
            self.logger.debug(f"protocol.{self.descriptor['name']}: No stop bit")
            return None

    # Set protocol gap
    def setGap(self, gap):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Setting gap-> {gap}")
        self.descriptor['gap'] = gap

    # Get protocol gap
    def getGap(self):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Getting gap-> {self.descriptor['gap']}")
        return self.descriptor['gap']

    # Set protocol header size
    def setHeaderSize(self, headerSize):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Setting header size-> {headerSize}")
        self.descriptor['headerSize'] = headerSize

    # Get protocol header size
    def getHeaderSize(self):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Getting header size-> {self.descriptor['headderSize']}")
        return self.descriptor['headerSize']

    # Set protocol data size
    def setDataSize(self, dataSize):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Seeting data size-> {dataSize}")
        self.descriptor['dataSize'] = dataSize

    # Get protocol data size
    def getDataSize(self):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Getting data size-> {self.descriptor['dataSize']}")
        return self.descriptor['dataSize']

    # Set protocol footer size
    def setFooterSize(self, footerSize):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Setting footer size-> {footerSize}")
        self.descriptor['footerSize'] = footerSize

    # Get protocol footer size
    def getFooterSize(self):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Getting footer size-> {self.descriptor['footerSize']}")
        return self.descriptor['footerSize']

    # Set first bit
    def setFirstBit(self, firstBit):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Setting first bit-> {firstBit}")
        self.descriptor['firstBit'] = firstBit

    # Get first bit
    def getFirstBit(self):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Getting first bit-> {self.descriptor['firstBit']}")
        return self.descriptor['firstBit']

    # Set send logical inverse
    def setSendLigicalInverse(self, sendLogicalInverse):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Setting logical inverse-> {sendLogicalInverse}")
        self.descriptor['sendLogicalInverse']

    # Get logical inverse
    def getSendLogicalInverse(self):
        self.logger.debug(f"protocol.{self.descriptor['name']}: Getting logical inverse-> {self.descriptor['sendLogicalInverse']}")
        return self.descriptor['sendLogicalInverse']

    # Save protocol
    def save(self):
        self.logger.info(f"Saving protocol {self.descriptorFilePath}", self.descriptorFilePath)
        with open(self.descriptorFilePath, 'w') as descriptorFile:
            jsonDescriptor = json.dumps(self.descriptor, sort_keys=True, indent=2)
            self.logger.debug(f"Protocol descriptor:\n{jsonDescriptor}", jsonDescriptor)
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
            self.logger.info(f"Creating new remote {model} from {manufacturer}")
            self.descriptor['manufacturer'] = manufacturer
            self.descriptor['model'] = model
            self.descriptor['keyCodes'] = {}
            if protocol is not None:
                self.descriptor['protocol'] = protocol
        else:
            self.logger.info(f"Loading remote {model} from {manufacturer}")
            with open(self.descriptorFilePath) as descriptorFile:
                self.descriptor = json.loads(descriptorFile.read())
            self.protocol = Protocol(self.logger, descriptorFilePath=os.path.join(PROTOCOL_DIR,
                self.descriptor['protocol'] + '.json'))
        self.logger.debug(f"Remote descriptor:\n{self.descriptor}")

    # Convert hex string to bit list
    def _convertToBitList(self, data, dataSize):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Converting {data} to bit list")
        dataInt = int(data, 16)
        return list(f'{dataInt:0>{dataSize}b}')

    # Convert bit list to hex string
    def _convertToHexString(self, bitList, dataSize):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Converting {bitList} to hex sting")
        bitString = ''.join(bitList)
        dataInt = int(bitString, 2)
        return f'0x{dataInt:0>{dataSize/4}x}'

    #Generate bit timing list
    def _generateBitTimingList(self, bitList):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Generating bit timing list from {bitList}")
        bitTimings = []
        for bit in bitList:
            self.logger.debug(f"remotes.{self.descriptor['model']}: Bit value {bit}")
            if bit == '1':
                self.logger.debug(f"remotes.{self.descriptor['model']}: Getting one bit timing")
                bitTimings.append(self.protocol.getOneBit())
            else:
                self.logger.debug(f"remotes.{self.descriptor['model']}: Getting zero bit timing")
                bitTimings.append(self.protocol.getZeroBit())
        self.logger.debug(f"remotes.{self.descriptor['model']}: Bit timing list generated\n{bitTimings}")
        return bitTimings

    # Set model
    def setModel(self, model):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Setting model to {model}")
        self.descriptor['model'] = model

    # Get model
    def getModel(self):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Getting model")
        return self.descriptor['model']

    # Set manufacturer
    def setManufacturer(self, manufacturer):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Setting manufacturer to {manufacturer}")
        self.descriptor['manufacturer'] = manufacturer

    # Get manufacturer
    def getManufacturer(self):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Getting manufacturer")
        return self.descriptor['manufacturer']

    # Set header
    def setHeader(self, header):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Setting header to {header}")
        if self.protocol.getFirstBit() == 'LSB':
            header.reverse()
        self.descriptor['header'] = self._convertToHexString(header, self.protocol.getHeaderSize())

    # Get header
    def getHeader(self):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Getting header")
        if 'header' in self.descriptor:
            headerList = self._convertToBitList(self.descriptor['header'], self.protocol.getHeaderSize())
            if self.protocol.getFirstBit() == 'LSB':
                headerList.reverse()
            return headerList
        else:
            return None

    # Set footer
    def setFooter(self, footer):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Setting footer to {footer}")
        if self.protocol.getFirstBit() == 'LSB':
            footer.reverse()
        self.descriptor['footer'] = self._convertToHexString(footer, self.protocol.getFooterSize())

    # Get footer
    def getFooter(self):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Getting footer")
        if 'footer' in self.descriptor:
            footerList = self._convertToBitList(self.descriptor['footer'], self.protocol.getFooterSize())
            if self.protocol.getFirstBit() == 'LSB':
                footerList.reverse()
            return footerList
        else:
            return None

    # Set key code
    def setKeyCode(self, key, code):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Setting {key} code to {code}")
        if self.protocol.getFirstBit() == 'LSB':
            code.reverse()
        self.descriptor['keyCodes'][key] = self._convertToHexString(code, self.protocol.getDataSize())

    # Get key code
    def getKeyCode(self, key):
        self.logger.debug(f"remote.{self.descriptor['model']}: Getting {key} key")
        if key in self.descriptor['keyCodes']:
            codeList = self._convertToBitList(self.descriptor['keyCodes'][key], self.protocol.getDataSize())
            if self.protocol.getFirstBit() == 'LSB':
                codeList.reverse()
                self.logger.debug(f"remote.{self.descriptor['model']}: codeList {codeList}")
            return codeList
        else:
            self.logger.debug('remote.%s: Key %s not found', self.descriptor['model'], key)
            return None

    # Get command gap
    def getCmdGap(self):
        self.logger.debug(f"remotes.{self.descriptor['model']}: Getting gap")
        return self.protocol.getGap()

    # Generate Command
    def generateCmd(self, key):
        self.logger.info(f"remote.{self.descriptor['model']}: Generating command for {key} key")
        command = []
        startBit = self.protocol.getStartBit()
        if startBit is not None:
            command.append(startBit)
            self.logger.debug(f"remotes.{self.descriptor['model']}: Adding start bit->\n{command}")
        header = self.getHeader()
        if header is not None:
            command += self._generateBitTimingList(header)
            self.logger.debug(f"remotes.{self.descriptor['model']}: Adding header->\n{command}")
        data = self.getKeyCode(key)
        if data is None:
            return None
        command += self._generateBitTimingList(data)
        self.logger.debug(f"remotes.{self.descriptor['model']}: Adding data->\n{command}")
        footer = self.getFooter()
        if footer is not None:
            command += self._generateBitTimingList(footer)
            self.logger.debug(f"remotes.{self.descriptor['model']}: Adding footer->\n{command}")
        return command

    # Save remote
    def save(self):
        self.logger.info(f"Saving remote model {self.descriptor['model']} from {self.descriptor['manufacturer']}")
        with open(self.descriptorFilePath, 'w') as descriptorFile:
            jsonDescriptor = json.dumps(self.descriptor, sort_keys=True, indent=2)
            self.logger.debug(f"Remote descriptor:\n{jsonDescriptor}", jsonDescriptor)
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
        logger.debug(f"Manufacturers list:\n{manufacturers}", manufacturers)
        return manufacturers

    # List remote from manufacturer
    @staticmethod
    def listRemote(manufacturer, logger):
        logger.info(f"Listing all remotes from {manufacturer}", manufacturer)
        remotes = []
        with os.scandir(os.path.join(REMOTE_DIR, manufacturer)) as entries:
            for entry in entries:
                remotes.append(entry.name.replace('.json', ''))
        logger.debug(f"Remotes list from {manufacturer}:\n{remotes}", manufacturer, remotes)
        return remotes
