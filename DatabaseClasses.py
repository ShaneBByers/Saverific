from enum import Enum


class Banks(Enum):

    @classmethod
    def table_name(cls):
        return 'BANKS'

    @classmethod
    def auto_increments(cls):
        return []

    bank_id = 'BANK_ID'
    name = 'NAME'


class Cards(Enum):

    @classmethod
    def table_name(cls):
        return 'CARDS'

    @classmethod
    def auto_increments(cls):
        return []

    card_id = 'CARD_ID'
    bank_id = 'BANK_ID'
    nickname = 'NICKNAME'
    name = 'NAME'
    last_four = 'LAST_FOUR'


class Emails(Enum):

    @classmethod
    def table_name(cls):
        return 'EMAILS'

    @classmethod
    def auto_increments(cls):
        return ['EMAIL_ID']

    email_id = 'EMAIL_ID'
    card_id = 'CARD_ID'
    amount = 'AMOUNT'
    merchant_name = 'MERCHANT_NAME'
    merchant_location = 'MERCHANT_LOCATION'
    date_time = 'DATE_TIME'


class ParseBanks(Enum):

    @classmethod
    def table_name(cls):
        return 'PARSE_BANKS'

    @classmethod
    def auto_increments(cls):
        return []

    parse_id = 'PARSE_ID'
    identifier = 'IDENTIFIER'
    bank_id = 'BANK_ID'
    date_format = 'DATE_FORMAT'
    localize_date_time = 'LOCALIZE_DATE_TIME'


class ParseComponents(Enum):

    @classmethod
    def table_name(cls):
        return 'PARSE_COMPONENTS'

    @classmethod
    def auto_increments(cls):
        return []

    parse_id = 'PARSE_ID'
    name = 'NAME'
    type = 'TYPE'
    prefix = 'PREFIX'
    postfix = 'POSTFIX'
