import sqlite3 as sql
from _sqlite3 import DatabaseError, Error

class Database:

    def __init__(self):
        try:
            self.db = sql.connect("blackmail.db")
            sql_query = ''' CREATE TABLE IF NOT EXISTS blackmail(id TEXT primary key, owner TEXT, message TEXT,
                            said_by_user TEXT)'''
            self.db.cursor().execute(sql_query)
            self.db.commit()
            print("Database has been initialized")
        except Error as e:
            print(e)

    def add(self, blackmail):
        sql_query = ''' INSERT INTO blackmail(id, owner, message, said_by_user)
                        VALUES(?, ?, ?, ?) '''
        cur = self.db.cursor()
        cur.execute(sql_query, blackmail)
        self.db.commit()
        return True

    def get_one(self, ID):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM blackmail WHERE id=?", ID)
        return cur.fetchone()

    def get_all_from_owner(self, owner):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM blackmail WHERE owner=?", owner)
        return cur.fetchall()

    def get_all_from_target(self, target):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM blackmail where said_by_user=?", target)
        return cur.fetchall()
