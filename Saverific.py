import Logger
from DataManager import DataManager

logger_name = "Saverific"
Logger.setup(logger_name)
manager = DataManager(logger_name)
manager.parse_emails()
