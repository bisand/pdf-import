from ast import Str
import sqlite3
from sqlite3 import Error
from typing import Any


class Repository(object):

    __databaseFile: Str

    def __init__(self, databaseFile) -> None:
        self.__databaseFile = databaseFile
        self.__createConnection()

    def __createConnection(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.__databaseFile)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def __enter__(self) -> Repository:
    try:
        return self.gen.next()
    except StopIteration:
        raise RuntimeError("generator didn't yield")

    def __exit__(self, type, value, traceback):
        pass