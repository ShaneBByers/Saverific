import html2text
import logging
from EmailConnector import EmailConnector


class EmailDataManager:

    def __init__(self, logger_name, host, username, password, source_mailbox, dest_mailbox):
        self.logger = logging.getLogger(logger_name)
        self.email_connector = EmailConnector(logger_name, host, username, password, source_mailbox, dest_mailbox)

    def get_emails(self):
        return self.email_connector.get_messages()

    def move_emails(self, messages, mailbox=None):
        for message in messages:
            self.email_connector.move_message(message, mailbox)
