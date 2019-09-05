import logging
import imaplib
import email


class EmailConnector:

    def __init__(self, logger_name, email_host, email_user, email_password):
        self.logger = logging.getLogger(logger_name)
        self.mail = imaplib.IMAP4_SSL(email_host, 993)
        self.mail.login(email_user, email_password)
        self.logger.info("Connected to " + email_host + " with user " + email_user + ".")

    def fetch_messages(self, mailbox):
        status, msgs = self.mail.select(mailbox)
        self.logger.info("Selected mailbox: " + mailbox)
        if status != 'OK':
            self.logger.info(msgs)
        _, id_list = self.mail.search(None, 'ALL')
        id_list = id_list[0].split()
        self.logger.info("Found " + str(len(id_list)) + " messages.")
        email_messages = []
        for email_id in id_list:
            _, data = self.mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_messages.append(email.message_from_string(raw_email_string))
        return email_messages
