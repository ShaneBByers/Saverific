from enum import Enum


class Accounts(Enum):

    @classmethod
    def table_name(cls):
        return 'ACCOUNTS'

    @classmethod
    def auto_increments(cls):
        return []

    @classmethod
    def not_nulls(cls):
        return ['ACCOUNT_ID', 'NICKNAME', 'ACCOUNT_NAME', 'ACCOUNT_NUMBER', 'BALANCE', 'IS_CREDIT']

    account_id = 'ACCOUNT_ID'
    bank_id = 'BANK_ID'
    nickname = 'NICKNAME'
    account_name = 'ACCOUNT_NAME'
    account_number = 'ACCOUNT_NUMBER'
    balance = 'BALANCE'
    is_credit = 'IS_CREDIT'
    credit_limit = 'CREDIT_LIMIT'


class Balances(Enum):

    @classmethod
    def table_name(cls):
        return 'BALANCES'

    @classmethod
    def auto_increments(cls):
        return []

    @classmethod
    def not_nulls(cls):
        return ['EMAIL_ID', 'BALANCE']

    email_id = 'EMAIL_ID'
    balance = 'BALANCE'


class Banks(Enum):

    @classmethod
    def table_name(cls):
        return 'BANKS'

    @classmethod
    def auto_increments(cls):
        return []

    @classmethod
    def not_nulls(cls):
        return ['BANK_ID', 'NAME']

    bank_id = 'BANK_ID'
    name = 'NAME'


class Emails(Enum):

    @classmethod
    def table_name(cls):
        return 'EMAILS'

    @classmethod
    def auto_increments(cls):
        return ['EMAIL_ID']

    @classmethod
    def not_nulls(cls):
        return ['ACCOUNT_ID', 'DATE_TIME']

    email_id = 'EMAIL_ID'
    account_id = 'ACCOUNT_ID'
    date_time = 'DATE_TIME'
    email_type_id = 'EMAIL_TYPE_ID'


class EmailTypes(Enum):

    @classmethod
    def table_name(cls):
        return 'EMAIL_TYPES'

    @classmethod
    def auto_increments(cls):
        return []

    @classmethod
    def not_nulls(cls):
        return ['EMAIL_TYPE_ID', 'TABLE', 'IS_EMAIL_HTML']

    email_type_id = 'EMAIL_TYPE_ID'
    table = 'TABLE'
    is_email_html = 'IS_EMAIL_HTML'
    transfer_type_id = 'TRANSFER_TYPE_ID'


class ParseBanks(Enum):

    @classmethod
    def table_name(cls):
        return 'PARSE_BANKS'

    @classmethod
    def auto_increments(cls):
        return []

    @classmethod
    def not_nulls(cls):
        return ['PARSE_ID', 'IDENTIFIER', 'BANK_ID', 'DATE_FORMAT', 'LOCALIZE_DATE_TIME']

    parse_id = 'PARSE_ID'
    identifier = 'IDENTIFIER'
    bank_id = 'BANK_ID'
    date_format = 'DATE_FORMAT'
    localize_date_time = 'LOCALIZE_DATE_TIME'
    email_type_id = 'EMAIL_TYPE_ID'


class ParseComponents(Enum):

    @classmethod
    def table_name(cls):
        return 'PARSE_COMPONENTS'

    @classmethod
    def auto_increments(cls):
        return []

    @classmethod
    def not_nulls(cls):
        return ['PARSE_ID']

    parse_id = 'PARSE_ID'
    name = 'NAME'
    type = 'TYPE'
    prefix = 'PREFIX'
    postfix = 'POSTFIX'


class Transactions(Enum):

    @classmethod
    def table_name(cls):
        return 'TRANSACTIONS'

    @classmethod
    def auto_increments(cls):
        return []

    @classmethod
    def not_nulls(cls):
        return ['EMAIL_ID']

    email_id = 'EMAIL_ID'
    amount = 'AMOUNT'
    merchant_name = 'MERCHANT_NAME'
    merchant_location = 'MERCHANT_LOCATION'


class Transfers(Enum):

    @classmethod
    def table_name(cls):
        return 'TRANSFERS'

    @classmethod
    def auto_increments(cls):
        return []

    @classmethod
    def not_nulls(cls):
        return ['EMAIL_ID', 'TRANSFER_TYPE_ID', 'AMOUNT']

    email_id = 'EMAIL_ID'
    transfer_type_id = 'TRANSFER_TYPE_ID'
    amount = 'AMOUNT'
    location = 'LOCATION'


class TransferTypes(Enum):

    @classmethod
    def table_name(cls):
        return 'TRANSFER_TYPES'

    @classmethod
    def auto_increments(cls):
        return ['TRANSFER_TYPE_ID']

    @classmethod
    def not_nulls(cls):
        return ['TYPE_NAME']

    transfer_type_id = 'TRANSFER_TYPE_ID'
    type_name = 'TYPE_NAME'
