import Logger
from DataManager import DataManager
import os

logger_name = "UpdateDBClasses"
Logger.setup(logger_name)
file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Generated/DatabaseClasses.py")
manager = DataManager(logger_name)
manager.update_classes_file(file_path)
