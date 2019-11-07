import mysql.connector

from src.model import EventEntity


class DbManager:
    db_config = {
        'host': 'db',
        'port': '3306',
        'user': 'event_manager_usr',
        'password': 'event_manager_pass',
        'database': 'event_manager_db'
    }

    def __init__(self):
        self.__connection = mysql.connector.connect(**self.db_config)

        if not self.__connection.is_connected():
            raise Exception('Connection problem')

    def _select(self, query: str):
        cursor = self.__connection.cursor()
        cursor.execute(query)

        return cursor.fetchall()

    def _run(self, query):
        cursor = self.__connection.cursor()
        cursor.execute(query)
        self.__connection.commit()


class DbEventManager(DbManager):
    __table = 'events'

    def fetch(self, event_id):
        records = self._select("SELECT * FROM {} WHERE id='{}'".format(
            self.__table,
            event_id
        ))

        if len(records):
            event = EventEntity()

            event.id = records[0][0]
            event.device_type = records[0][1]
            event.category = records[0][2]
            event.client = records[0][3]
            event.client_group = records[0][4]
            event.valid = bool(records[0][5])
            event.value = float(records[0][6])
            event.timestamp = records[0][7]

            return event

        return None

    def delete(self, event_id):
        self._run("DELETE FROM {} WHERE id='{}'".format(
            self.__table,
            event_id
        ))
