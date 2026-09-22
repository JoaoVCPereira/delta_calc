from core.services import DeltaCalcService
from config.environment import DeltaCalc
from utils import log_utils
import logging

def start_service(service_name):
    app = None
    if DeltaCalc.name == service_name:
        app = DeltaCalcService(DeltaCalc)
    if None !=app:
        app.run()
    else:
        logging.error(f'Service [{service_name}] not found.')

if __name__ == "__main__":
    log_utils.config_logger()
    logger = logging.getLogger()
    logger.info('[STARTUP]')

    start_service(DeltaCalc.name)