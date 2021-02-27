from pathlib import Path
import sqlite3

DBPATH = ""
for path in Path(__file__).parents[2].rglob('blackmail.db'):
    DBPATH = path
if not DBPATH:
    DBPATH = Path(__file__).parents[1] / 'blackmail.db'


def db_connect():
    conn = sqlite3.connect(str(DBPATH))
    return conn


def add(blackmail):
    conn = db_connect()
    c = conn.cursor()
    sql = ''' INSERT INTO blackmail(owner, message, said_by_user)
    VALUES(?, ?, ?) '''
    c.execute(sql, blackmail)
    conn.commit()

    # To get a return ID
    c.execute('SELECT id FROM blackmail ORDER BY ID DESC LIMIT 1')
    fetched = c.fetchone()
    conn.close()
    return fetched


def get_one(blackmail_id: int):
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM blackmail WHERE id=?', (blackmail_id,))
    fetched = c.fetchone()
    conn.close()
    if not fetched:
        raise Exception("Nothing was fetched")
    else:
        return fetched


def is_owner_of_blackmail(owner: int, blackmail_id: int):
    conn = db_connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM blackmail WHERE id=? AND owner=?", (blackmail_id, owner))
    fetched = c.fetchone()
    conn.close()
    if int(fetched[0]) == 1:
        return True
    else:
        return False


def get_all_from_owner(owner: int):
    conn = db_connect()
    c = conn.cursor()
    c.execute("SELECT * FROM blackmail WHERE owner=? LIMIT 0,20", (owner,))
    fetched = c.fetchall()
    conn.close()
    return fetched


def count_all_from_owner(owner: int):
    conn = db_connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM blackmail where owner=?", (owner,))
    fetched = c.fetchone()
    conn.close()
    return int(fetched)


def get_all_from_target(target: int):
    conn = db_connect()
    c = conn.cursor()
    c.execute("SELECT * FROM blackmail WHERE said_by_user=? LIMIT 0,20", (target,))
    fetched = c.fetchall()
    conn.close()
    return fetched


def count_all_from_target(owner: int):
    conn = db_connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM blackmail where owner=?", (owner,))
    fetched = c.fetchone()
    conn.close()
    return int(fetched)


def delete_one(blackmail_id: int):
    if check_if_entry_exists(blackmail_id):
        conn = db_connect()
        c = conn.cursor()
        c.execute("DELETE FROM blackmail WHERE id=?", (blackmail_id,))
        conn.commit()
        conn.close()
        return True
    else:
        return False


def check_if_entry_exists(blackmail_id: int):
    conn = db_connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM blackmail WHERE id=?", (blackmail_id,))
    fetched = c.fetchone()
    conn.close()
    if int(fetched[0]) == 1:
        return True
    else:
        return False
