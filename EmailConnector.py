import logging
from imap_tools import MailBox


class EmailConnector:

    def __init__(self, logger_name, host, user, password, source_mailbox, dest_mailbox, error_mailbox):
        self.logger = logging.getLogger(logger_name)
        self.mailbox = MailBox(host)
        self.mailbox.login(user, password, initial_folder=source_mailbox)
        self.logger.info("Connected to " + host + " with user " + user + ".")
        self.source_mailbox = source_mailbox
        self.dest_mailbox = dest_mailbox
        self.error_mailbox = error_mailbox

    def get_messages(self):
        return list(self.mailbox.fetch())

    def move_message(self, message, error):
        if error:
            self.mailbox.move(message.uid, self.error_mailbox)
            self.logger.info("Moved email with UID " + str(message.uid) + " to " + self.error_mailbox + ".")
        else:
            self.mailbox.move(message.uid, self.dest_mailbox)
            self.logger.info("Moved email with UID " + str(message.uid) + " to " + self.dest_mailbox + ".")
