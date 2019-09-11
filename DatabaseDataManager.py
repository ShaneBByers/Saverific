from DatabaseConnector import DatabaseConnector
import logging


class DatabaseDataManager:

    def __init__(self, logger_name, db_host, db_username, db_password, db_name):
        self.connector = DatabaseConnector(logger_name, db_host, db_username, db_password, db_name)
        self.insert_statement = ""
        self.update_statement = ""
        self.logger = logging.getLogger(logger_name)

    def insert(self, entities, commit=True):
        if isinstance(entities, list):
            for entity in entities:
                self.connector.create_insert(entity)
                last_row_id = self.connector.execute_insert()
        else:
            self.connector.create_insert(entities)
            last_row_id = self.connector.execute_insert()
        if commit:
            last_row_id = self.connector.commit_execute()

        return last_row_id

    def __select(self, entity, single=False):
        self.connector.create_select(entity)
        return self.connector.execute_select(entity.table, single)

    def select_all(self, entity):
        return self.__select(entity)

    def select_single(self, entity):
        return self.__select(entity, True)

    def update(self, entities, commit=True):
        if isinstance(entities, list):
            for entity in entities:
                self.connector.create_update(entity)
                last_row_id = self.connector.execute_update()
        else:
            self.connector.create_update(entities)
            last_row_id = self.connector.execute_update()
        if commit:
            last_row_id = self.connector.commit_execute()

        return last_row_id

    def delete(self, entities, commit=True):
        if isinstance(entities, list):
            for entity in entities:
                self.connector.create_delete(entity)
                last_row_id = self.connector.execute_delete()
        else:
            self.connector.create_delete(entities)
            last_row_id = self.connector.execute_delete()
        if commit:
            last_row_id = self.connector.commit_execute()

        return last_row_id

    def commit(self):
        return self.connector.commit_execute()

    def get_table_information(self):
        return self.connector.get_table_information()
