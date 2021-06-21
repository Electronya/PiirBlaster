class DeviceFileAccess(Exception):
    """
    Exception raised when access to the device file generate errors.
    """
    pass


class DeviceNotFound(Exception):
    """
    Exception raised when no device corresponding to the search
    critera was found.
    """
    def __init__(self, name, location):
        """
        Constructor.

        Params:
            name:       The device name that already exists.
            location:   The device location that already exists.
        """
        super().__init__(f"device {location}.{name} not found")


class DeviceExists(Exception):
    """
    Exception raisedd when trying to add a device with the same location and
    name than one that is already active.
    """
    def __init__(self, name, location):
        """
        Constructor.

        Params:
            name:       The device name that already exists.
            location:   The device location that already exists.
        """
        super().__init__(f"device {location}.{name} already exists.")


class CommandNotFound(Exception):
    """
    Exception raised when no command corresponding to the seach
    was found.
    """
    def __init__(self, command):
        """
        Constructor.

        Params:
            command:    The name of the command that was not found.
        """
        super().__init__(f"command {command} not supported.")


class CommandFileAccess(Exception):
    """
    Exception raised when access to the command set fail.
    """
    pass
