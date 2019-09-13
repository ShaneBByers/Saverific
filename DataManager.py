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

    @staticmethod
    def get_email_component(text, component):
        types = {'str': (str, '', ''), 'int': (int, ',', ''), 'float': (float, ',', '')}

        val = None

        if component.get(ParseComponents.prefix) in text and \
                component.get(ParseComponents.postfix).replace('\\r', '').replace('\\n', '\n') in text:
            current_type = types[component.get(ParseComponents.type)]
            str_val = (text
                       .split(component.get(ParseComponents.prefix), 1)[1]
                       .strip()
                       .split(component.get(ParseComponents.postfix).replace('\\r', '').replace('\\n', '\n'), 1)[0]
                       .strip()).replace(current_type[1], current_type[2])
            val = current_type[0](str_val)
        return val

    def get_db_parse_info(self):
        parse_banks_select = DBEntity(ParseBanks)
        parse_banks = self.db_manager.select_all(parse_banks_select)

        parse_banks_dict = {}

        for parse_bank in parse_banks:
            parse_components_select = DBEntity(ParseComponents)
            parse_components_select.add_where(ParseComponents.parse_id, parse_bank.get(ParseBanks.parse_id))
            parse_components = self.db_manager.select_all(parse_components_select)
            parse_banks_dict[parse_bank] = parse_components

        return parse_banks_dict

    def get_db_accounts(self):
        accounts_select = DBEntity(Accounts)
        accounts = self.db_manager.select_all(accounts_select)

        return accounts

    def get_unread_emails(self):
        emails = self.email_manager.get_emails()

        return emails

    def parse_emails(self):
        emails = self.get_unread_emails()

        if len(emails) > 0:
            email_types_select = DBEntity(EmailTypes)
            email_types = self.db_manager.select_all(email_types_select)
            db_parse_dict = self.get_db_parse_info()
            db_accounts = self.get_db_accounts()
            for email in emails:
                found_match = False
                for bank, bank_info in db_parse_dict.items():
                    email_text = email.text
                    DetailsTable = None
                    transfer_type_id = None
                    for email_type in email_types:
                        if bank.get(ParseBanks.email_type_id) == email_type.get(EmailTypes.email_type_id):
                            if email_type.get(EmailTypes.is_email_html):
                                email_text = email.html
                                transfer_type_id = email_type.get(EmailTypes.transfer_type_id)
                            if email_type.get(EmailTypes.table) == Transactions.table_name():
                                DetailsTable = Transactions
                            elif email_type.get(EmailTypes.table) == Balances.table_name():
                                DetailsTable = Balances
                            elif email_type.get(EmailTypes.table) == Transfers.table_name():
                                DetailsTable = Transfers
                            break

                    account = None

                    if bank.get(ParseBanks.identifier) in email_text:
                        found_match = True
                        self.logger.info("Found email matching bank with ID " + str(bank.get(ParseBanks.bank_id)) + ".")
                        if DetailsTable is not None:
                            db_email = DBEntity(Emails)
                            for component in bank_info:
                                if component.get(ParseComponents.name) == Accounts.account_number.value:
                                    last_four = self.get_email_component(email_text, component)
                                    for db_account in db_accounts:
                                        if db_account.get(Accounts.account_number) == last_four:
                                            account = db_account
                                            db_email.set(Emails.account_id, db_account.get(Accounts.account_id))
                                            break
                                    break

                            modified_date = email.date.split(' -', 1)[0].split(' +', 1)[0]
                            email_date_time = datetime.datetime.strptime(modified_date, bank.get(ParseBanks.date_format))
                            if bank.get(ParseBanks.localize_date_time):
                                email_date_time = email_date_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
                            db_email.set(Emails.date_time, email_date_time)

                            db_email.set(Emails.email_type_id, bank.get(ParseBanks.email_type_id))

                            db_email_details = DBEntity(DetailsTable)

                            if DetailsTable is Transfers:
                                db_email_details.set(Transfers.transfer_type_id, transfer_type_id)

                            limit = None
                            for component in bank_info:
                                if component.get(ParseComponents.name) == Accounts.credit_limit.value:
                                    limit = self.get_email_component(email_text, component)
                                else:
                                    for col in DetailsTable:
                                        if component.get(ParseComponents.name) == col.value:
                                            val = self.get_email_component(email_text, component)
                                            db_email_details.set(col, val)

                            if limit is not None and account is not None:
                                limit += db_email_details.get(DetailsTable.balance)
                                limit = int(round(float(limit)))
                                account.set(Accounts.credit_limit, limit)
                                account.add_where(Accounts.account_id, account.get(Accounts.account_id))
                                self.db_manager.update(account)

                            parsed = True
                            for col in Emails:
                                if db_email.get(col) is None and col.value in Emails.not_nulls():
                                    parsed = False
                            for col in DetailsTable:
                                if db_email_details.get(col) is None and \
                                        col.value != Emails.email_id.value and \
                                        col.value in DetailsTable.not_nulls():
                                    parsed = False

                            if parsed:
                                db_email_id = self.db_manager.insert(db_email, False)
                                db_email_details.set(DetailsTable.email_id, db_email_id)
                                self.db_manager.insert(db_email_details)
                                self.email_manager.move_email(email)
                            else:
                                self.email_manager.move_email(email, True)
                if not found_match:
                    self.email_manager.move_email(email, True)
            self.db_manager.commit()

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

            auto_increment_list = []
            not_null_list = []
            for column in columns:
                if 'auto_increment' in column['Extra']:
                    auto_increment_list.append(column['Field'])
                elif 'NO' in column['Null']:
                    not_null_list.append(column['Field'])

            self.file_manager.write_line("@classmethod", tabs=1)
            self.file_manager.write_line("def auto_increments(cls):", tabs=1)
            self.file_manager.write("return [", tabs=2)

            if len(auto_increment_list) > 0:
                for column in auto_increment_list[:-1]:
                    self.file_manager.write("'" + column + "', ")
                else:
                    self.file_manager.write("'" + auto_increment_list[-1] + "'")
            self.file_manager.write_line("]", lines=2)

            self.file_manager.write_line("@classmethod", tabs=1)
            self.file_manager.write_line("def not_nulls(cls):", tabs=1)
            self.file_manager.write("return [", tabs=2)

            if len(not_null_list) > 0:
                for column in not_null_list[:-1]:
                    self.file_manager.write("'" + column + "', ")
                else:
                    self.file_manager.write("'" + not_null_list[-1] + "'")
            self.file_manager.write_line("]")

            for column in columns:
                self.file_manager.write_line()
                self.file_manager.write(column['Field'].lower() + " = '" + column['Field'] + "'", tabs=1)
        self.file_manager.write_line()
        self.file_manager.close()
