import display
import signal
import configparser
import os
import sys
import pathlib
import logging
import logging.handlers

CONFIG = configparser.ConfigParser()


def main():
    display.run(CONFIG)


if __name__ == '__main__':
    # Parse configuration
    CONFIG.read('config.ini')

    # Setup simple logging upon start
    pathlib.Path(CONFIG['logging']['path']).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    for handler in logger.handlers:
        logger.removeHandler(handler)

    log_file = os.path.join(CONFIG['logging']['path'], 'status-display.log')
    log_handler = logging.handlers.WatchedFileHandler(log_file)
    formatter = logging.Formatter(
        '[%(asctime)s|PID %(process)d] <%(levelname)s> %(message)s',
        '%d-%m-%y %H:%M:%S')
    log_handler.setFormatter(formatter)

    logger.addHandler(log_handler)
    logger.setLevel(CONFIG['logging'].getint('level'))
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    signal.signal(signal.SIGINT, display.sendToSleep)
    signal.signal(signal.SIGTERM, display.sendToSleep)
    main()
