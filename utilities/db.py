from pathlib import Path
import sqlite3

DBPATH = ""
for path in Path(__file__).parents[2].rglob('blackmail.db'):
    DBPATH = path
if not DBPATH:
    DBPATH = Path(__file__).parents[1] / 'blackmail.db'


def db_connect():
    try:
        conn = sqlite3.connect(str(DBPATH))
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(e)


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


def count_all_from_owner(owner: int):
    conn = db_connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM blackmail where owner=?", (owner,))
    fetched = c.fetchone()
    conn.close()
    return int(fetched)


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


def query_db(query, args=(), one=False):
    cur = db_connect().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
