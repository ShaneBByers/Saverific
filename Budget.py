import logging
from Logger import Logger
from DataManager import DataManager

logger_name = "Saverific_Logger"

logger_obj = Logger(logger_name)
logger = logging.getLogger(logger_name)

data_manager = DataManager(logger_name)
data_manager.parse_emails()

logger.info("DONE")
