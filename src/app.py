import sys

from .config import Config
from .device import DeviceManager
from .logger import initLogger


class App:
    """
    The application class.
    """
    def __init__(self):
        """
        Contructor.
        """
        logger = initLogger()
        self.logger = logger.getLogger('APP')
        self.logger.info('Initializing the app.')

        self.config = Config()
        self.deviceMngr = DeviceManager(logger, self.config)

        self.logger.info('App initialized.')

    def run(self):
        """
        Run the application.
        """
        self.logger.info('Running the app.')

    def stop(self):
        """
        Stop the application.
        """
        self.logger.info('Stopping the app.')


if __name__ == '__main__':
    app = App()
    try:
        app.run()
    except Exception:
        app.stop()
        sys.exit(0)
