import sqlite3

def resetDatebase():
    print("Warning! Resetting the database will reset the database (duh). Doing this will completly delete all of the website's content")
    CHOICE = input("Enter 'Yes I do wish to delete everything 👍' if that is your true intention: ") == 'Yes I do wish to delete everything 👍'
    if CHOICE == True:
        con = sqlite3.connect('database.db')
        cursor = con.cursor()

        cursor.execute('''
            CREATE TABLE currentEvents(
                title text,
                date text,
                text text,
                images int
            )''')

        cursor.execute('''
            CREATE TABLE image(
                filename text,
                group_id int
            )''')

        con.commit()
if __name__ == "__main__":
    pass