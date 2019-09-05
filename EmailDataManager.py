import html2text
import logging
from EmailConnector import EmailConnector


class EmailDataManager:

    def __init__(self, logger_name, email_host, email_username, email_password):
        self.logger = logging.getLogger(logger_name)
        self.email_connector = EmailConnector(logger_name, email_host, email_username, email_password)

    def get_emails(self, mailbox='"Inbox"'):
        email_dict = {}
        email_messages = self.email_connector.fetch_messages(mailbox)
        for email_message in email_messages:
            email_body = ""
            if email_message.is_multipart():
                for payload in email_message.get_payload():
                    email_body = payload.get_payload()
            else:
                email_body = email_message.get_payload(decode=True)

            if isinstance(email_body, str) and "</" in email_body:
                email_body_text = html2text.html2text(email_body)
            else:
                email_body_text = email_body.decode('utf-8')

            email_dict[email_message] = email_body_text

        return email_dict
