import Constants
import DatabaseManager
import Logger
import os

logger_name = "UpdateDBClasses"
Logger.setup(logger_name)
file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), Constants.DB_CLASS_FILE_PATH)
db_manager = DatabaseManager.connect(logger_name,
                                     Constants.DB_HOST,
                                     Constants.DB_USERNAME,
                                     Constants.DB_PASSWORD,
                                     Constants.DB_NAME,
                                     file_path)
db_manager.update_classes_file()
