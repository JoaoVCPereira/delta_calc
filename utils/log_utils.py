import logging

from utils import utils
from config.environment import Logging
from config.environment import DeltaCalc

_LOGGING_LEVEL_FULL = Logging.logging_level_full
_LOGGING_FILE_FULL = Logging.logging_path_full

SERVICES = {
    DeltaCalc.name:DeltaCalc.cron
}

def config_logger():
    utils.create_if_not_exists(_LOGGING_FILE_FULL)
    format = "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s (%(filename)s:%(funcName)s)"
    format_report = "[%(asctime)s] %(message)s"

    datefmt = "%Y-%m-%d %H:%M:%S %z"
    datefmt_report = "%d-%m-%Y %H:%M:%S"

    log_levels_dict = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}
    log_level_full = log_levels_dict[_LOGGING_LEVEL_FULL]
    logging.basicConfig(format=format, datefmt=datefmt, level=log_level_full)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level_full)
    console_handler.setFormatter(logging.Formatter(fmt=format, datefmt=datefmt))

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level_full)
    fileHandler = logging.FileHandler(_LOGGING_FILE_FULL)
    fileHandler.setFormatter(logging.Formatter(fmt=format, datefmt=datefmt))
    root_logger.addHandler(fileHandler)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)