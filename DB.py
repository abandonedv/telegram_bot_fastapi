import sqlite3 as sq
import datetime


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    async def add_message(self, mes, ans):
        try:
            t = str(datetime.datetime.now())
            self.__cur.execute("INSERT INTO messages VALUES (NULL, ?, ?, ?)", (mes, ans, t))
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка в БД: " + str(e))
            return False

        return True

    async def get_message(self, numb):
        try:
            self.__cur.execute(f"SELECT * FROM messages WHERE number LIKE '{numb}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sq.Error as e:
            print("Ошибка получения из БД " + str(e))

        return True
