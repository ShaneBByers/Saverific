import logging
import datetime
from Constants import Constants
from EmailDataManager import EmailDataManager
from DatabaseDataManager import DatabaseDataManager
from DatabaseClasses import Bank, Card, Email, ParseBank, ParseComponent, DBEntity


class DataManager:

    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.db_manager = DatabaseDataManager(logger_name,
                                              Constants.db_host.value,
                                              Constants.db_username.value,
                                              Constants.db_password.value,
                                              Constants.db_name.value)
        self.email_manager = EmailDataManager(logger_name,
                                              Constants.email_host.value,
                                              Constants.email_username.value,
                                              Constants.email_password.value,
                                              Constants.email_source_mailbox.value,
                                              Constants.email_dest_mailbox.value,
                                              Constants.email_error_mailbox.value)

    def get_db_parse_info(self):
        parse_banks_select = DBEntity(ParseBank)
        parse_banks = self.db_manager.select_all(parse_banks_select)

        parse_banks_dict = {}

        for parse_bank in parse_banks:
            parse_components_select = DBEntity(ParseComponent)
            parse_components_select.add_where(ParseComponent.component_id, parse_bank.get(ParseBank.component_id))
            parse_components = self.db_manager.select_all(parse_components_select)
            parse_banks_dict[parse_bank] = parse_components

        return parse_banks_dict

    def get_db_cards(self):
        cards_select = DBEntity(Card)
        cards = self.db_manager.select_all(cards_select)

        return cards

    def get_unread_emails(self):
        emails = self.email_manager.get_emails()

        return emails

    def parse_emails(self):
        db_parse_dict = self.get_db_parse_info()
        db_cards = self.get_db_cards()
        emails = self.get_unread_emails()

        types = {'str': str, 'int': int, 'float': float}

        insert_emails = []
        parsed_emails = []
        not_parsed_emails = []

        for email in emails:
            for bank, bank_info in db_parse_dict.items():
                if bank.get(ParseBank.identifier) in email.text:
                    self.logger.info("Found email matching bank with ID " + str(bank.get(ParseBank.bank_id)) + ".")
                    db_email = DBEntity(Email)
                    modified_date = email.date.split(' -', 1)[0].split(' +', 1)[0]
                    email_date_time = datetime.datetime.strptime(modified_date, bank.get(ParseBank.date_format))
                    if bank.get(ParseBank.localize_date_format):
                        email_date_time = email_date_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
                    db_email.set(Email.date_time, email_date_time)
                    parsed = True
                    for component in bank_info:
                        for col in Email:
                            if component.get(ParseComponent.name) == col.value or \
                                    (component.get(ParseComponent.name) == 'LAST_FOUR' and col.value == 'CARD_ID'):
                                if component.get(ParseComponent.prefix) in email.text and \
                                        component.get(ParseComponent.postfix).replace('\\n', '\n') in email.text:
                                    val = types[component.get(ParseComponent.type)](email.text
                                                                                    .split(component.get(ParseComponent.prefix), 1)[1]
                                                                                    .strip()
                                                                                    .split(component.get(ParseComponent.postfix).replace('\\n', '\n'), 1)[0]
                                                                                    .strip())
                                    if component.get(ParseComponent.name) == 'LAST_FOUR':
                                        for card in db_cards:
                                            if card.get(Card.last_four) == val:
                                                db_email.set(Card.card_id, card.get(Card.card_id))
                                    else:
                                        db_email.set(col, val)
                                else:
                                    parsed = False
                    if parsed:
                        insert_emails.append(db_email)
                        parsed_emails.append(email)
                    else:
                        not_parsed_emails.append(email)

        for insert_email in insert_emails:
            self.db_manager.insert(insert_email, False)
        self.db_manager.commit()

        self.email_manager.move_emails(parsed_emails)
        self.email_manager.move_emails(not_parsed_emails, True)
