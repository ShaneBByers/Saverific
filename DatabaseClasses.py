from enum import Enum
import datetime


class Bank(Enum):

    @classmethod
    def table_name(cls):
        return 'BANKS'

    @classmethod
    def auto_increments(cls):
        return []

    bank_id = 'BANK_ID'
    name = 'NAME'


class Card(Enum):

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


class Email(Enum):

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


class ParseBank(Enum):

    @classmethod
    def table_name(cls):
        return 'PARSE_BANKS'

    @classmethod
    def auto_increments(cls):
        return []

    bank_id = 'BANK_ID'
    identifier = 'IDENTIFIER'
    component_id = 'COMPONENT_ID'
    date_format = 'DATE_FORMAT'
    localize_date_format = 'LOCALIZE_DATE_TIME'


class ParseComponent(Enum):

    @classmethod
    def table_name(cls):
        return 'PARSE_COMPONENTS'

    @classmethod
    def auto_increments(cls):
        return ['ID']

    id = 'ID'
    component_id = 'COMPONENT_ID'
    name = 'NAME'
    type = 'TYPE'
    prefix = 'PREFIX'
    postfix = 'POSTFIX'


class DBEntity:

    def __init__(self, table, record=None):
        if record is None:
            self._record = {}
        else:
            self._record = record
        for col in table:
            if col.value not in self._record:
                self._record[col.value] = None
        self.__value_updated = {}
        for col in self._record:
            self.__value_updated[col] = False
        self.table = table
        self.custom_where_clause = None
        self.__select_cols_names = None
        self.__where_clause_list = None

    def get(self, col):
        return self._record[col.value]

    def set(self, col, val):
        self._record[col.value] = val
        self.__value_updated[col.value] = True

    def add_select_col(self, col):
        if self.__select_cols_names is None:
            self.__select_cols_names = []
        self.__select_cols_names.append(col.value)

    def add_where(self, col, val, op="="):
        if self.__where_clause_list is None:
            self.__where_clause_list = []
        self.__where_clause_list.append(WhereStatement(col.value, val, op))

    @property
    def where_clause(self):
        if self.custom_where_clause is not None:
            return self.custom_where_clause
        elif self.__where_clause_list is None or len(self.__where_clause_list) == 0:
            return None
        else:
            return_string = " WHERE ("
            for where in self.__where_clause_list[:-1]:
                return_string += where.to_string()
                return_string += " && "
            else:
                return_string += self.__where_clause_list[-1].to_string()
            return_string += ")"
            return return_string

    @property
    def select_col_clause(self):
        if self.__select_cols_names is None:
            return "*"
        else:
            return_string = ""
            for col in self.__select_cols_names[:-1]:
                return_string += col + ", "
            else:
                return_string += self.__select_cols_names[-1]
            return_string += ""
            return return_string

    @property
    def insert_col_val_clause(self):
        col_list = []
        for col in self._record:
            if col not in self.table.auto_increments():
                col_list.append(col)

        return_string = "("
        for col in col_list[:-1]:
            return_string += col + ", "
        else:
            return_string += col_list[-1]
        return_string += ") VALUES ("
        for col in col_list[:-1]:
            if self._record[col] is None:
                return_string += "NULL, "
            else:
                if isinstance(self._record[col], str):
                    return_string += "\"" + str(self._record[col]) + "\", "
                elif isinstance(self._record[col], datetime.datetime):
                    return_string += "\"" + self._record[col].strftime('%Y-%m-%d %H:%M:%S') + "\""
                else:
                    return_string += str(self._record[col]) + ", "
        else:
            if self._record[col_list[-1]] is None:
                return_string += "NULL"
            else:
                if isinstance(self._record[col_list[-1]], str):
                    return_string += "\"" + str(self._record[col_list[-1]]) + "\""
                elif isinstance(self._record[col_list[-1]], datetime.datetime):
                    return_string += "\"" + self._record[col_list[-1]].strftime('%Y-%m-%d %H:%M:%S') + "\""
                else:
                    return_string += str(self._record[col_list[-1]])
        return_string += ")"
        return return_string

    @property
    def update_clause(self):
        col_list = []
        for col in self._record:
            if self.__value_updated[col] and col not in self.table.auto_increments():
                col_list.append(col)
        return_string = "SET "
        count = 0
        for col in col_list:
            return_string += col + " = "
            val = self._record[col]
            if isinstance(val, str):
                return_string += "\"" + val + "\""
            elif isinstance(val, datetime.datetime):
                return_string += "\"" + val.strftime('%Y-%m-%d %H:%M:%S') + "\""
            else:
                return_string += str(val)
            count += 1
            if count < len(col_list):
                return_string += ", "

        return return_string


class WhereStatement:

    def __init__(self, col, val, op="="):
        self.__col = col
        self.__val = val
        self.__op = op

    @property
    def col(self):
        return self.__col

    @property
    def val(self):
        if self.__val is None:
            return "NULL"
        else:
            return self.__val

    @property
    def op(self):
        return self.__op

    def to_string(self):
        return self.col + " " + self.op + " " + str(self.val)
