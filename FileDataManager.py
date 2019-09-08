import logging


class FileDataManager:

    def __init__(self, logger_name, tab_length=4):
        self.logger = logging.getLogger(logger_name)
        self.file = None
        self.tab = ""
        for i in range(tab_length):
            self.tab += " "

    def open(self, file_name):
        self.file = open(file_name, "w+")
        self.logger.info("Opened file " + file_name)

    def write(self, text="", tabs=0):
        for i in range(tabs):
            self.file.write(self.tab)
        self.file.write(text)
        test = text.split("\n", 1)
        if len(text.split("\n", 1)[0]) > 0:
            self.logger.info("Wrote \"" + text.split("\n", 1)[0] + "\" to file.")
        else:
            self.logger.info("Wrote new line(s) to file.")

    def write_line(self, text="", tabs=0, lines=1):
        for i in range(lines):
            text += "\n"
        self.write(text, tabs)

    def close(self):
        self.file.close()
        self.logger.info("Closed file.")

    def __del__(self):
        self.close()
