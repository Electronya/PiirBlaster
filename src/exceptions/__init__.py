class DeviceExists(Exception):
    """
    Exception raised when trying to add a device with the same location and
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
