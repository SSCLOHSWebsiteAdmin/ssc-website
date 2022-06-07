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
            date TEXT,
            text TEXT,
            images INTEGER,
            id INTEGER NOT NULL PRIMARY KEY,
            public BOOL
        )''')

    cursor.execute('''
        CREATE TABLE issue(
            title TEXT,
            date TEXT,
            desc TEXT,
            urlCode, TEXT,
            public BOOL
        )''')

    cursor.execute('''
        CREATE TABLE issueSection(
            type TEXT,
            link TEXT,
            sectionId INTEGER,
            urlCode INTEGER
        )''')

    cursor.execute('''
        CREATE TABLE issueText(
            text TEXT,
            textId INTEGER,
            sectionId INTEGER,
            urlCode INTEGER
        )''')

    cursor.execute('''
        CREATE TABLE currentEvents(
            title TEXT,
            date TEXT,
            text TEXT,
            images INTEGER,
            id INTEGER NOT NULL PRIMARY KEY,
            public BOOL
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

# Issue
def addIssueByText():
    title   = input("Title: ")
    date    = input("Date: ")
    desc    = input("Description: ")
    url     = input("Url code: ")

    sections    = []
    texts       = []

    while input("Add more? y/n: ") == "y":
        type = input("Type (p=photo, y=youtube, e=embed): ")
        link = input("link: ")

        sections.append([type, link])

        textSection = []
        print("enter 'end' to end")
        newText = input("Text: ")
        while newText != 'end':
            textSection.append(newText)
            newText = input("Text: ")
        texts.append(textSection)

    addIssue(title, date, desc, url, sections, texts)

def deleteIssue():
    global con, cursor

    issues = cursor.execute('''
        SELECT
            urlCode
        FROM
            issue
        ORDER BY
            date DESC
    ;''').fetchall()

    print("you are deleting an issue.")
    for issue in enumerate(issues):
        #print(issue)
        print(str(issue[0]+1) + '. ' + issue[1][0])

    choice = input("which issue to delete ('n' to cancel): ")

    if choice != 'n':
        deleted = issues[int(choice)-1][0]
        cursor.execute('''
            DELETE FROM
                issue
            WHERE
                urlCode = ?
            ;''',(deleted,))
    else:
        print('canceled!')

    con.commit()

    print(deleted + " has been deleted")

def addIssue(title, date, desc, url, sections, texts):
    global con, cursor

    cursor.execute('''
        INSERT INTO issue(
            title,
            date,
            desc,
            urlCode,
            public
        )
        VALUES (
            ?, ?, ?, ?, False
        )
        ;''', (title, date, desc, url))

    for section in enumerate(sections):
        cursor.execute('''
            INSERT INTO 
                issueSection (
                    type,
                    link,
                    sectionId,
                    urlCode
                )
            VALUES(
                ?,?,?,?
                )
            ;''', (section[1][0], section[1][1], section[0], url))

    sectionId = 0
    for textSection in texts:
        for text in enumerate(textSection):
            cursor.execute('''
                INSERT INTO 
                    issueText (
                        text,
                        textId,
                        sectionId,
                        urlCode
                    )
                VALUES(
                    ?,?,?,?
                    )
                ;''', (text[1], text[0], sectionId, url))
        sectionId += 1

    con.commit()

def getIssue(urlCode):
    global con, cursor

    issue = cursor.execute('''
            SELECT
                *
            FROM
                issue
            WHERE
                urlCode = ?
        ;''',(urlCode,)).fetchone()

    print(issue)
    issueId = issue[4]
    print(issueId)
    sections = cursor.execute('''
            SELECT
                *
            FROM
                issueSection
            WHERE
                urlCode = ?
            ORDER BY
                sectionId ASC
        ;''',(urlCode,)).fetchall()

    texts = []

    for sectionId in range(len(sections)):
        newTexts = cursor.execute('''
            SELECT
                text
            FROM
                issueText
            WHERE
                urlCode = ? AND sectionId = ?
            ORDER BY
                textId ASC
        ;''',(urlCode, sectionId)).fetchall()

        texts.append(newTexts)
    return issue, sections, texts

def getIssueBasic():
    global con, cursor

    basic = cursor.execute('''
            SELECT
                title,
                date,
                desc,
                urlCode
            FROM
                issue
            ORDER BY
                date DESC
        ;''').fetchall()

    return basic

# Blog
def deletePost():
    global con, cursor

    blog = cursor.execute('''
        SELECT
            title
        FROM
            blog
        ORDER BY
            date DESC
    ;''').fetchall()

    print("you are deleting an issue.")
    for issue in enumerate(blog):
        #print(issue)
        print(str(issue[0]+1) + '. ' + issue[1][0])

    choice = input("which issue to delete ('n' to cancel): ")

    if choice != 'n':
        deleted = blog[int(choice)-1][0]
        cursor.execute('''
            DELETE FROM
                blog
            WHERE
                title = ?
            ;''',(deleted,))
    else:
        print('canceled!')

    con.commit()

    print(deleted + " has been deleted")

def addBlogPostByText():
    title = input("Title: ")
    date = input("Date: ")
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
            images,
            public
        )
        VALUES (
            ?, ?, ?, ?, False
        )
        ;''', (title, date, text, group_id))

    con.commit()

def toggleBlogPostPublicity(id):
    global con, cursor

    public = cursor.execute('''
        SELECT public
        FROM blog
        WHERE id = ?
    ;''', (id,)).fetchone()[0]
    if public == 0:
        cursor.execute('''
            UPDATE blog
            SET public = True
            WHERE id = ?
        ;''', (id,))
    else:
        cursor.execute('''
            UPDATE blog
            SET public = False
            WHERE id = ?
        ;''', (id,))

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

        posts[i][3] = images[0]

    print(posts)
    return posts

def getPublicBlogPosts():
    global con, cursor

    posts = cursor.execute('''
        SELECT
            * 
        FROM
            blog
        WHERE
            public = True
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

def getBlogPost(id):
    global con, cursor

    post = cursor.execute('''
        SELECT 
            *
        FROM
            blog
        WHERE 
            id = ?
    ;''',(id,)).fetchone()

    images = cursor.execute('''
        SELECT 
            filename
        FROM
            images
        WHERE 
            group_id = ?
    ;''',(post[3],)).fetchall()
    print(images)
    fullPost = list(post)
    print(fullPost)
    fullPost[3] = images
    print(fullPost)
    return fullPost

def updateBlogPost(title, date, text, images, id):
    global con, cursor

    cursor.execute('''
        UPDATE blog
        SET
            title = ?,
            date = ?,
            text = ?
        WHERE id = ?
    ;''', [title, date, text, id])

    con.commit()

if FIRST_RUN == True:
    resetDatebase()

if __name__ == "__main__":
    choice = input('0: add blog post\n1: add issue\n2: delete issue\n3: delete post\n4: rest database\n\nchoice: ')
    if choice == '0':
        addBlogPostByText()
    elif choice == '1':
        addIssueByText()
    elif choice == '2':
        deleteIssue()
    elif choice == '3':
        deletePost()
    elif choice == '4':
        resetDatebase()