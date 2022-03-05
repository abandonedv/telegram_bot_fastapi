import sqlite3 as sq
import datetime


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    async def add_messages(self, mes):
        try:
            t = str(datetime.datetime.now())
            self.__cur.execute("INSERT INTO messages VALUES (NULL, ?, ?)", (mes, t))
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка в БД: " + str(e))
            return False

        return True
