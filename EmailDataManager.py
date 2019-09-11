import html2text
import logging
from EmailConnector import EmailConnector


class EmailDataManager:

    def __init__(self, logger_name, host, username, password, source_mailbox, dest_mailbox, error_mailbox):
        self.logger = logging.getLogger(logger_name)
        self.email_connector = EmailConnector(logger_name, host, username, password, source_mailbox, dest_mailbox, error_mailbox)

    def get_emails(self):
        return self.email_connector.get_messages()

    def move_email(self, message, error=False):
        self.email_connector.move_message(message, error)
