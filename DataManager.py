import logging
import datetime
from Constants import Constants
from EmailDataManager import EmailDataManager
from DatabaseDataManager import DatabaseDataManager
from FileDataManager import FileDataManager
from DatabaseEntity import DBEntity
from DatabaseClasses import *


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

        self.file_manager = FileDataManager(logger_name)

    def get_db_parse_info(self):
        parse_banks_select = DBEntity(ParseBanks)
        parse_banks = self.db_manager.select_all(parse_banks_select)

        parse_banks_dict = {}

        for parse_bank in parse_banks:
            parse_components_select = DBEntity(ParseComponents)
            parse_components_select.add_where(ParseComponents.component_id, parse_bank.get(ParseBanks.component_id))
            parse_components = self.db_manager.select_all(parse_components_select)
            parse_banks_dict[parse_bank] = parse_components

        return parse_banks_dict

    def get_db_cards(self):
        cards_select = DBEntity(Cards)
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
                if bank.get(ParseBanks.identifier) in email.text:
                    self.logger.info("Found email matching bank with ID " + str(bank.get(ParseBanks.bank_id)) + ".")
                    db_email = DBEntity(Emails)
                    modified_date = email.date.split(' -', 1)[0].split(' +', 1)[0]
                    email_date_time = datetime.datetime.strptime(modified_date, bank.get(ParseBanks.date_format))
                    if bank.get(ParseBanks.localize_date_format):
                        email_date_time = email_date_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
                    db_email.set(Emails.date_time, email_date_time)
                    parsed = True
                    for component in bank_info:
                        for col in Emails:
                            if component.get(ParseComponents.name) == col.value or \
                                    (component.get(ParseComponents.name) == 'LAST_FOUR' and col.value == 'CARD_ID'):
                                if component.get(ParseComponents.prefix) in email.text and \
                                        component.get(ParseComponents.postfix).replace('\\n', '\n') in email.text:
                                    val = types[component.get(ParseComponents.type)](email.text
                                                                                    .split(component.get(ParseComponents.prefix), 1)[1]
                                                                                    .strip()
                                                                                    .split(component.get(ParseComponents.postfix).replace('\\n', '\n'), 1)[0]
                                                                                    .strip())
                                    if component.get(ParseComponents.name) == 'LAST_FOUR':
                                        for card in db_cards:
                                            if card.get(Cards.last_four) == val:
                                                db_email.set(Cards.card_id, card.get(Cards.card_id))
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

    def update_classes_file(self):
        table_info = self.db_manager.get_table_information()
        self.file_manager.open(Constants.db_class_filename.value)
        self.file_manager.write("from enum import Enum")
        for table_name, columns in table_info.items():
            self.file_manager.write_line(lines=3)
            name_words = table_name.split('_')
            name = ''
            for name_word in name_words:
                name += name_word.capitalize()
            self.file_manager.write_line("class " + name + "(Enum):", lines=2)

            self.file_manager.write_line("@classmethod", tabs=1)
            self.file_manager.write_line("def table_name(cls):", tabs=1)
            self.file_manager.write_line("return '" + table_name + "'", tabs=2, lines=2)

            self.file_manager.write_line("@classmethod", tabs=1)
            self.file_manager.write_line("def auto_increment(cls):", tabs=1)
            self.file_manager.write("return [", tabs=2)
            auto_increment_list = []
            for column in columns:
                if 'auto_increment' in column['Extra']:
                    auto_increment_list.append(column['Field'])
            if len(auto_increment_list) > 0:
                for column in auto_increment_list[:-1]:
                    self.file_manager.write("'" + column + "', ")
                else:
                    self.file_manager.write("'" + auto_increment_list[-1] + "'")
            self.file_manager.write_line("]")

            for column in columns:
                self.file_manager.write_line()
                self.file_manager.write(column['Field'].lower() + " = '" + column['Field'] + "'", tabs=1)
        self.file_manager.write_line()
        self.file_manager.close()
