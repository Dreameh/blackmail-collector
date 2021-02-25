import sqlite3 as sql
from _sqlite3 import DatabaseError, Error


class Database:
    testsql_query = ''' CREATE TABLE IF NOT EXISTS blackmail(id TEXT primary key, owner TEXT,
    message TEXT, said_by_user TEXT)'''
    def __init__(self):
        try:
            self.db = sql.connect("blackmail.db")
            self.cursor = db.cursor()
        except Error as e:
            print(e)

    def init_table(self):
        try:
            self.cursor.execute(testsql_query)
        except Error as e:
            print(e)

    def check_connection(self):
        if self.db is not None:
            return True
        else:
            return False

    def add(self, blackmail):
        if check_connection():
            sql_query = ''' INSERT INTO blackmail(id, owner, message, said_by_user)
            VALUES(?, ?, ?, ?) '''
            self.cursor.execute(sql_query, blackmail)
            self.db.commit()
            return True
        else:
            return False

    def get_one(self, id):
        self.cursor.execute("SELECT * FROM blackmail WHERE id=?", id)
        return self.cursor.fetchone()

    def get_specific_from_owner(self, owner, id):
        self.cursor.execute("SELECT COUNT(*) FROM blackmail WHERE id=? AND owner=?")
        return self.cursor.fetchone()

    def get_all_from_owner(self, owner):
        self.cursor.execute("SELECT * FROM blackmail WHERE owner=?", owner)
        return self.cursor.fetchall()

    def get_all_from_target(self, target):
        self.cursor.execute("SELECT * FROM blackmail where said_by_user=?", target)
        return self.cursor.fetchall()

    def delete_one(self, id):
        if check_connection():
            if check_if_entry_exists(id) is None:
                raise Exception("Following ID: " + id + " does not exist in the database.")

            self.cursor.execute("DELETE FROM blackmail where id=?", id)
            self.cursor.commit()
            return True
        else:
            return False

    def check_if_entry_exists(self, id):
        self.cursor.execute("SELECT COUNT(*) FROM blackmail WHERE id=?", id)
        return self.cursor.fetchone()
