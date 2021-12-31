import sqlite3
import pathlib

DATABASE_FILE = "database.db"

FIRST_RUN   = True
if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN   = False

con = sqlite3.connect(DATABASE_FILE)
cursor = con.cursor()

def resetDatebase():
    global con, cursor

    cursor.execute('''
        CREATE TABLE blog(
            title TEXT,
            date TEXT,
            text TEXT,
            images INTEGER
        )''')

    cursor.execute('''
        CREATE TABLE currentEvents(
            title TEXT,
            date TEXT,
            text TEXT,
            images INTEGER
        )''')

    cursor.execute('''
        CREATE TABLE images(
            group_id integer primary key 
        )''')

    cursor.execute('''
        CREATE TABLE image(
            filename TEXT,
            group_id INTEGER
        )''')

    con.commit()

def addCurrentEvent(title, data, text, images):
    global con, cursor
    cursor.execute('''
        INSERT INTO currentEvents (
            title ?,
            date ?,
            text ?,
            images ?            
        )''', (title, data, text, images))

if __name__ == "__main__":
    if FIRST_RUN == True:
        print("among")
        resetDatebase()