import sqlite3
import pathlib

DATABASE_FILE = "database.db"

FIRST_RUN   = True
if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN   = False

con = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
cursor = con.cursor()

def resetDatebase():
    global con, cursor

    cursor.execute('''
        CREATE TABLE blog(
            title TEXT,
            date INTEGER,
            text TEXT,
            images INTEGER
        )''')

    cursor.execute('''
        CREATE TABLE currentEvents(
            title TEXT,
            date INTEGER,
            text TEXT,
            images INTEGER
        )''')

    cursor.execute('''
        CREATE TABLE images(
            filename TEXT,
            group_id INTEGER
        )''')

    con.commit()

def addCurrentEvent(title, date, text, images):
    global con, cursor
    cursor.execute('''
        INSERT INTO currentEvents (
            title ?,
            date ?,
            text ?,
            images ?            
        )''', (title, date, text, images))

def addBlogPostByText():
    title = input("Title: ")
    date = int(input("Date: "))
    text = input("Text: ")

    images = []
    for i in range(int(input("How many images: "))):
        images.append(input("image: "))

    addBlogPost(title, date, text, images)

def addBlogPost(title, date, text, images):
    global con, cursor

    group_id = cursor.execute('''
        SELECT 
            group_id
        FROM
            images
        ORDER BY
            group_id DESC
    ;''').fetchone()

    if group_id == None:
        group_id = 0
    else:
        group_id = group_id[0] + 1

    for image in images:
        cursor.execute('''
            INSERT INTO 
                images (
                    filename,
                    group_id
                )
            VALUES(
                ?,?
                )
            ;''', (image, group_id))

    cursor.execute('''
        INSERT INTO blog(
            title,
            date,
            text,
            images
        )
        VALUES (
            ?, ?, ?, ?
        )
        ;''', (title, date, text, group_id))

    con.commit()

def getBlogPosts():
    global con, cursor

    posts = cursor.execute('''
        SELECT
            * 
        FROM
            blog
        ORDER BY
            date DESC
    ;''').fetchall()
    for i in range(len(posts)):
        posts[i] = list(posts[i])

        images = cursor.execute('''
            SELECT 
                filename
            FROM 
                images
            WHERE
                group_id = ?
        ;''', (posts[i][3],)).fetchall()

        posts[i][3] = images

    return posts

if FIRST_RUN == True:
    resetDatebase()

if __name__ == "__main__":

    addBlogPostByText()