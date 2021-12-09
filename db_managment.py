import sqlite3

con = sqlite3.connect('database.db')
cursor = con.cursor()

def resetDatebase():
    global con, cursor
    print("Warning! Resetting the database will reset the database (duh). Doing this will completly delete all of the website's content")
    CHOICE = input("Enter 'Yes I do wish to delete everything 👍' if that is your true intention: ") == 'Yes I do wish to delete everything 👍'
    if CHOICE == True:

        cursor.execute('''
            CREATE TABLE currentEvents(
                title text,
                date text,
                text text,
                images integer
            )''')

        cursor.execute('''
            CREATE TABLE images(
                group_id integer primary key 
            )''')


        cursor.execute('''
            CREATE TABLE image(
                filename text,
                group_id integer
            )''')

        con.commit()

def addCurrentEvent(title, data, text, images):
    global con, cursor
    cursor.execute('''
        INSERT INTO 
    ''')

if __name__ == "__main__":
    pass