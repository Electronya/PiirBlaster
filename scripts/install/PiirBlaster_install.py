#!/usr/bin/env python3
import os
import subprocess

# Text styling class
class Text:
    HEADER = '\033[1;34m'
    SUCCESS = '\033[1;32m'
    FAIL = '\033[1;21m'
    ENDC = '\033[0m'

# Commands class
class Command:
    INSTALL_PY_DEPS = 'sudo apt-get install -y python3 python3-distutils python3-pip python3-setuptools python3-venv'
    CLONE_PIIRBLASTER = 'git clone https://github.com/Electronya/PiirBlaster.git'
    CREATE_PIIRBLASTER_SVC = 'sudo cp ./PiirBlaster/scripts/services/piirblaster.service /etc/systemd/system'
    ENABLE_PIIRBLASTER_SVC = 'sudo systemctl enable piirblaster.service'
    START_PIIRBLASTER_SVC = 'sudo systemctl start piirblaster.service'
    CREATE_VRITUAL_ENV = 'python3 -m venv venv'
    INSTALL_DEPENDENCIES = 'venv/bin/pip install -r requirements.txt'
    DWNLD_PIGPIO = 'wget https://github.com/joan2937/pigpio/archive/master.zip'
    UNZIP_PIGPIO = 'unzip master.zip'
    BUILD_PIGPIO = 'make'
    INSTALL_PIGPIO = 'sudo make install'
    CREATE_PIGPIO_SVC = 'sudo cp ./PiirBlaster/scripts/services/pigpiod.service /etc/systemd/system'
    ENABLE_PIGPIO_SVC = 'sudo systemctl enable pigpiod.service'
    START_PIGPIO_SVC = 'sudo systemctl start pigpiod.service'

# Execute shell command
def execCommand(command):
    process = subprocess.run(command.split(' '))
    return process.returncode

# Download PIGPIO
def downloadPIGPIO():
    print(f"{Text.HEADER}*** DOWNLOADING PIGPIO ***{Text.ENDC}")
    cmdResult = execCommand(Command.DWNLD_PIGPIO)
    if cmdResult != 0:
        print(f"{Text.FAIL}PIGPIO DOWNLOAD FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}PIGPIO DOWNLOAD DONE{Text.ENDC}")
    return True

# Unzip PIGPIO
def unzipPIGPIO():
    print(f"{Text.HEADER}*** UNZIPPNG PIGPIO ***{Text.ENDC}")
    cmdResult = execCommand(Command.UNZIP_PIGPIO)
    if cmdResult != 0:
        print(f"{Text.FAIL}PIGPIO UNZIP FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}PIGPIO UNZIP DONE{Text.ENDC}")
    return True

# Building PIGPIO
def buildPIGPIO():
    print(f"{Text.HEADER}*** BUILDING PIGPIO ***{Text.ENDC}")
    os.chdir('pigpio-master')
    cmdResult = execCommand(Command.BUILD_PIGPIO)
    if cmdResult != 0:
        print(f"{Text.FAIL}PIGPIO BUILD FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}PIGPIO BUILD DONE{Text.ENDC}")
    return True

# Install PIGPIO
def installPIGPIO():
    print(f"{Text.HEADER}*** INSTALLING PIGPIO ***{Text.ENDC}")
    cmdResult = execCommand(Command.INSTALL_PIGPIO)
    if cmdResult !=0:
        print(f"{Text.FAIL}PIGPIO INSTALL FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}PIGPIO INSTALL DONE{Text.ENDC}")
    return True

# Creating PIGPIO service
def createPigpioSvc():
    print(f"{Text.HEADER}*** CREATING PIGPIO SERVICE ***{Text.ENDC}")
    os.chdir('..')
    cmdResult = execCommand(Command.CREATE_PIGPIO_SVC)
    if cmdResult != 0:
        print(f"{Text.FAIL}CREATING PIGPIO SERVICE FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}CREATING PIGPIO SERVICE DONE{Text.ENDC}")
    return True

# Enabling PIGPIO service
def enablePigpioSvc():
    print(f"{Text.HEADER}*** ENABLING PIGPIO SERVICE ***{Text.ENDC}")
    cmdResult = execCommand(Command.ENABLE_PIGPIO_SVC)
    if cmdResult != 0:
        print(f"{Text.FAIL}ENABLING PIGPIO SERVICE FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}ENABLING PIGPIO SERVICE DONE{Text.ENDC}")
    return True

# Starting PIGPIO service
def startPigpioSvc():
    print(f"{Text.HEADER}*** STARTING PIGPIO SERVICE ***{Text.ENDC}")
    cmdResult = execCommand(Command.START_PIGPIO_SVC)
    if cmdResult != 0:
        print(f"{Text.FAIL}STARTING PIGPIO SERVICE FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}STARTING PIGPIO SERVICE DONE{Text.ENDC}")
    return True

# Setup PIGPIO service
def setupPigpioSvc():
    # TODO: Check if sevice is already installed & Split in multiple functions
    print(f"{Text.HEADER}*** SETTING UP PIGPIO SERVICE ***{Text.ENDC}")
    if downloadPIGPIO():
        if unzipPIGPIO():
            if buildPIGPIO():
                if installPIGPIO():
                    if createPigpioSvc():
                        if enablePigpioSvc():
                            if startPigpioSvc():
                                print(f"{Text.SUCCESS}SETTING UP PIGPIO SERVICE DONE{Text.ENDC}")
                                return True
    print(f"{Text.FAIL}SETTING UP PIGPIO SERVICE FAILED!!!{Text.ENDC}")
    return False

# Install Python dependencies
def installPythonDeps():
    print(f"{Text.HEADER}*** INSTALLING PYTHON DEPENDENCIES ***{Text.ENDC}")
    cmdResult = execCommand(Command.INSTALL_PY_DEPS)
    if cmdResult != 0:
        print(f"{Text.FAIL}INSTALLING PYTHON DEPS FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}INTALLING PYTHON DEPS DONE{Text.ENDC}")
    return True

# Clone PiirBlaster repo
def clonePiirBlaster():
    # TODO: Copuing the deployment key
    print(f"{Text.HEADER}*** CLONING PiirBlaster REPO ***{Text.ENDC}")
    cmdResult = execCommand(Command.CLONE_PIIRBLASTER)
    if cmdResult != 0:
        print(f"{Text.FAIL}CLONING PiirBlaster FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}CLONING PiirBlaster DONE{Text.ENDC}")
    return True

# Creating virtual environment
def createVirtualEnv():
    print(f"{Text.HEADER}*** CREATING VIRTUAL ENVIRONMENT ***{Text.ENDC}")
    os.chdir('PiirBlaster')
    cmdResult = execCommand(Command.CREATE_VRITUAL_ENV)
    if cmdResult != 0:
        print(f"{Text.FAIL}CREATING VIRTUAL ENVIRONEMENT FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}CREATING VIRTUAL ENVIRONMENT DONE{Text.ENDC}")
    return True

# TODO: Install python3-venv (sudo apt install python3-venv)

# Install dependencies
def installDependencies():
    print(f"{Text.HEADER}*** INSTALLING PiirBlaster DEPENDENCIES ***{Text.ENDC}")
    cmdResult = execCommand(Command.INSTALL_DEPENDENCIES)
    if cmdResult != 0:
        print(f"{Text.FAIL}INSTALLING PiirBlaster DEPENDENCIES FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}INSTALLING PiirBlaster DEPENDENCIES DONE{Text.ENDC}")
    os.chdir('..')
    return True

# Create PiirBlaster service
def createPiirBlasterSvc():
    print(f"{Text.HEADER}*** CREATING PiirBlaster SERVICE ***{Text.ENDC}")
    cmdResult = execCommand(Command.CREATE_PIIRBLASTER_SVC)
    if cmdResult != 0:
        print(f"{Text.FAIL}CREATING PiirBlaster SERVICE FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}CREATING PiirBlaster SERVICE DONE{Text.ENDC}")
    return True

# Enabling PiirBlaster Service
def enablePiirBlasterSvc():
    print(f"{Text.HEADER}*** ENABLING PiirBlaster SERVICE ***{Text.ENDC}")
    cmdResult = execCommand(Command.ENABLE_PIIRBLASTER_SVC)
    if cmdResult != 0:
        print(f"{Text.FAIL}ENALBING PiirBlaster SERVICE FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}ENABLING PiirBlaster SERVICE DONE{Text.ENDC}")
    return True

# Start PiirBlaster Service
def startPiirBlasterSvc():
    print(f"{Text.HEADER}*** STARTING PiirBlaster SERVICE ***{Text.ENDC}")
    cmdResult = execCommand(Command.START_PIIRBLASTER_SVC)
    if cmdResult != 0:
        print(f"{Text.FAIL}STARTING PiirBlaster SERVICE FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}STARTING PiirBlaster SERVICE DONE{Text.ENDC}")
    return True

# Setup PiirBlaster service
def setupPiirBlasterSvc():
    # TODO: Check if sevice is already installed
    print(f"{Text.HEADER}*** SETTING UP PiirBlaster SERVICE ***{Text.ENDC}")
    if createVirtualEnv():
        if installDependencies():
            if createPiirBlasterSvc():
                if enablePiirBlasterSvc():
                    if startPiirBlasterSvc():
                        print(f"{Text.SUCCESS}SETTING UP PiirBlaster SERVICE DONE{Text.ENDC}")
                        return True
    print(f"{Text.FAIL}SETTING UP PiirBlaster SERVICE FAILED!!!{Text.ENDC}")
    return False

# print(f"{Text.HEADER}*** SERVICE CONFIGURATION ***{Text.ENDC}")
# Ask for the hostname the service will use for advertising
# hostname = input(f"Please enter the hostname that the service will use for advertising:")

if installPythonDeps():
    if clonePiirBlaster():
        if setupPigpioSvc():
            if setupPiirBlasterSvc():
                print(f"{Text.SUCCESS}INSATALLING PiirBlaster SERVICE DONE{Text.ENDC}")
                exit()
print(f"{Text.FAIL}INTALLING PiirBlaster SERVICE FAILED!!!{Text.ENDC}")
