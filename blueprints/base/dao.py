import os
import mysql.connector


class BaseDAO:

    def __init__(self):
        self.__db_config = {
            'host' : os.getenv("MYSQL_HOST"),
            'user' : os.getenv("MYSQL_USER"),
            'password' : os.getenv("MYSQL_PASSWORD"),
            'database' : os.getenv("MYSQL_DATABASE"),
            'port' : os.getenv("MYSQL_PORT")
        }

    def _get_connection(self):
        return mysql.connector.connect(**self.__db_config)