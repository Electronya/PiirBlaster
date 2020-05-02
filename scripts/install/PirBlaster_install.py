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
    CLONE_PIRBLASTER = 'git clone git@github.com:Electronya/PirBlaster.git'
    CREATE_PIRBLASTER_SVC = 'sudo cp ./scripts/services/pirblaster.service /etc/systemd/system'
    ENABLE_PIRBLASTER_SVC = 'sudo systemctl enable pirblaster.service'
    START_PIRBLASTER_SVC = 'sudo systemctl start pirblaster.service'
    CREATE_VRITUAL_ENV = 'python3 -m venv venv'
    ACTIVATE_VIRTUAL_ENV = 'source venv/bin/activate'
    DEACTIVATE_VIRTUAL_ENV = 'deactivate'
    INSTALL_DEPENDENCIES = 'pip install -r requirements.txt'
    DWNLD_PIGPIO = 'wget https://github.com/joan2937/pigpio/archive/master.zip'
    UNZIP_PIGPIO = 'unzip master.zip'
    BUILD_PIGPIO = 'make'
    INSTALL_PIGPIO = 'sudo make install'
    CREATE_PIGPIO_SVC = 'sudo cp ./scripts/services/pigpiod.service /etc/systemd/system'
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

# Clone PirBlaster repo
def clonePirBlaster():
    # TODO: Copuing the deployment key
    print(f"{Text.HEADER}*** CLONING PIRBLASTER REPO ***{Text.ENDC}")
    cmdResult = execCommand(Command.CLONE_PIRBLASTER)
    if cmdResult != 0:
        print(f"{Text.FAIL}CLONING PIRBLASTER FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}CLONING PIRBLASTER DONE{Text.ENDC}")
    return True

# Creating virtual environment
def createVirtualEnv():
    print(f"{Text.HEADER}*** CREATING VIRTUAL ENVIRONMENT ***{Text.ENDC}")
    os.chdir('./PirBlaster')
    cmdResult = execCommand(Command.CREATE_VRITUAL_ENV)
    if cmdResult != 0:
        print(f"{Text.FAIL}CREATING VIRTUAL ENVIRONEMENT FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}CREATING VIRTUAL ENVIRONMENT DONE{Text.ENDC}")
    return True

# Activate virtual environment
def activateVirutalEnv():
    print(f"{Text.HEADER}*** AVITVATING VIRTUAL ENVIRONMENT ***{Text.ENDC}")
    cmdResult = execCommand(Command.ACTIVATE_VIRTUAL_ENV)
    if cmdResult != 0:
        print(f"{Text.FAIL}ACTIVATING VIRTUAL ENVIRONMENT FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}ACTIVATING VIRTUAL ENVIRONMENT DONE{Text.ENDC}")
    return True

# Deactivate virtual environment
def deactivateVirtualEnv():
    print(f"{Text.HEADER}*** DEACTIVATING VIRTUAL ENVIRONMENT ***{Text.ENDC}")
    cmdResult = execCommand(Command.DEACTIVATE_VIRTUAL_ENV)
    if cmdResult != 0:
        print(f"{Text.FAIL}DEACTIVATING VIRTUAL ENVIRONMENT FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}DEACTIVATING VIRTUAL ENVIRONMENT DONE{Text.ENDC}")
    os.chdir('..')
    return True

# Install dependencies
def installDependencies():
    print(f"{Text.HEADER}*** INSTALLING PIRBLASTER DEPENDENCIES ***{Text.ENDC}")
    cmdResult = execCommand(Command.INSTALL_DEPENDENCIES)
    if cmdResult != 0:
        print(f"{Text.FAIL}INSTALLING PIRBLASTER DEPENDENCIES FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}INSTALLING PIRBLASTER DEPENDENCIES DONE{Text.ENDC}")
    return True

# Create PirBlaster service
def createPirBlasterSvc():
    print(f"{Text.HEADER}*** CREATING PIRBLASTER SERVICE ***{Text.ENDC}")
    cmdResult = execCommand(Command.CREATE_PIRBLASTER_SVC)
    if cmdResult != 0:
        print(f"{Text.FAIL}CREATING PIRBLASTER SERVICE FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}CREATING PIRBLASTER SERVICE DONE{Text.ENDC}")
    return True

# Enabling PirBlaster Service
def enablePirBlasterSvc():
    print(f"{Text.HEADER}*** ENABLING PIRBLASTER SERVICE ***{Text.ENDC}")
    cmdResult = execCommand(Command.ENABLE_PIRBLASTER_SVC)
    if cmdResult != 0:
        print(f"{Text.FAIL}ENALBING PIRBLASTER SERVICE FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}ENABLING PIRBLASTER SERVICE DONE{Text.ENDC}")
    return True

# Start PirBlaster Service
def startPirBlasterSvc():
    print(f"{Text.HEADER}*** STARTING PIRBLASTER SERVICE ***{Text.ENDC}")
    cmdResult = execCommand(Command.START_PIRBLASTER_SVC)
    if cmdResult != 0:
        print(f"{Text.FAIL}STARTING PIRBLASTER SERVICE FAILED!!!{Text.ENDC}")
        return False
    print(f"{Text.SUCCESS}STARTING PIRBLASTER SERVICE DONE{Text.ENDC}")
    return True

# Setup PirBlaster service
def setupPirBlasterSvc():
    # TODO: Check if sevice is already installed
    print(f"{Text.HEADER}*** SETTING UP PIRBLASTER SERVICE ***{Text.ENDC}")
    if createVirtualEnv():
        if activateVirutalEnv():
            if installDependencies():
                if deactivateVirtualEnv():
                    if createPirBlasterSvc():
                        if enablePirBlasterSvc():
                            if startPirBlasterSvc():
                                print(f"{Text.SUCCESS}SETTING UP PIRBLASTER SERVICE DONE{Text.ENDC}")
                                return True
    print(f"{Text.FAIL}SETTING UP PIRBLASTER SERVICE FAILED!!!{Text.ENDC}")
    return False

# print(f"{Text.HEADER}*** SERVICE CONFIGURATION ***{Text.ENDC}")
# Ask for the hostname the service will use for advertising
# hostname = input(f"Please enter the hostname that the service will use for advertising:")

if clonePirBlaster():
    if setupPigpioSvc():
        if setupPirBlasterSvc():
            print(f"{Text.SUCCESS}INSATALLING PIRBLASTER SERVICE DONE{Text.ENDC}")
            exit()
print(f"{Text.FAIL}INTALLING PIRBLASTER SERVICE FAILED!!!{Text.ENDC}")
