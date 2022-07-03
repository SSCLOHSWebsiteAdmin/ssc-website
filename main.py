from flask import Response, Flask, flash, session, render_template, redirect, url_for, request, send_from_directory
from db_managment import *
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import datetime

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# SITE SETUP
app = Flask(__name__)

app.secret_key = b'AmOngStrs_69/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        for file in files:
            if file.filename == '' or not allowed_file(file.filename):
                pass
                # files.pop(files.index(file))
            else:
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        names = [file.filename for file in files]
        return names

@app.route('/')
def index():

    return redirect('/home')

@app.route('/home')
def home():
    issues = getRecentIssues()
    return render_template('home.html', name="Home", issues=issues)

@app.route('/rss/issues')
def rssIssues():
    issues, thumbs = getPublicIssueBasic()

    items = ""

    if len(issues) > 10:
        length = 10
    else:
        length = len(issues)

    for i in range(length):
        title = issues[i][0]
        desc = issues[i][2]
        url = url_for('issue', id=issues[i][3])
        img = url_for('download_file', name=thumbs[i])

        items += '''<item>
        <title>''' + title + ''''</title>
        <link>''' + url + '''</link>
        <image>
            <url>''' + img + '''</url>
            <title>''' + title + ''' image</title>
            <link>''' + url + '''</link>
        </image>
        <description>''' + desc + '''</description>
        </item>'''

    xml = '''
    <rss version = "2.0">
    <channel>
    <title> LOHS SSC | Issues</title>
    <link> https://www.lohs.ca/ssc </link>
    <description>Research by Lillian Osborne High School's Student Solidarity Committee</description>
    ''' + items + '''
    </channel>
    </rss>
    '''

    return Response(xml, mimetype='text/xml')

@app.route('/rss/blog')
def rssBlog():
    posts = getPublicBlogPosts()

    items = ""

    if len(posts) > 10:
        length = 10
    else:
        length = len(posts)

    for i in range(length):
        title = posts[i][0]
        desc = posts[i][2]
        if len(posts[i][3]) > 0:
            img = url_for('download_file', name=posts[i][3][0])
        else:
            img = ""

        items += '''<item>
        <title>''' + title + ''''</title>
        <link>''' + url_for('blog') + '''</link>
        <image>
            <url>''' + img + '''</url>
            <title>''' + title + ''' image</title>
            <link>''' + url_for('blog') + '''</link>
        </image>
        <description>''' + desc + '''</description>
        </item>'''

    xml = '''
    <rss version = "2.0">
    <channel>
    <title> LOHS SSC | Issues</title>
    <link> https://www.lohs.ca/ssc </link>
    <description>Research by Lillian Osborne High School's Student Solidarity Committee</description>
    ''' + items + '''
    </channel>
    </rss>
    '''

    return Response(xml, mimetype='text/xml')

@app.route('/ShowYourSolidarity')
def SYS():
    return render_template('SYS.html', name="Show Your Solidarity")

@app.route('/issues')
def issues():
    issues, thumbs = getPublicIssueBasic()
    return render_template('issues.html', name="Issues", issues=issues, thumbs=thumbs)

@app.route('/issues/<id>')
def issue(id):
    issues, sections, texts = getIssue(id)
    return render_template('issue.html', name=issues[0], issue=issues, sections=sections, texts=texts)

@app.route('/CurrentEvents')
def currentEvents():
    return render_template('currentEvents.html', name="Current Events")

@app.route('/blog')
def blog():
    posts = getPublicBlogPosts()
    print(posts)
    return render_template('blog.html', name="Blog", posts=posts)

# Admin Stuff,  subdomain="admin"

def loggedIn():
    print("checking session!")
    if 'login' not in session:
        print("not logged in")
        return False
    else:
        return True

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    print("login")
    message = ""

    if request.method == 'POST':
        password = request.form['password']

        if password == "SAM_LOW_IS_COOL":
            session['login'] = 'logged in!'
            return redirect('/admin')
        else:
            message = "Wrong Password!"

    return render_template('login.html', message=message, name='login')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not loggedIn():
        return redirect('/admin/login')
    return render_template('admin.html', name="Admin Hub")

@app.route('/admin/issues', methods=['GET', 'POST'])
def adminIssues():
    if not loggedIn():
        return redirect('/admin/login')
    issues, thumbs = getIssueBasic()
    print("thumbs:")
    print(thumbs)
    print(issues)
    return render_template('admin-issues.html', name="Issues", issues=issues, thumbs=thumbs)

@app.route('/newIssue', methods=['POST'])
def newIssue():
    if not loggedIn():
        return redirect('/admin/login')
    url = request.form['newUrl']
    x = datetime.datetime.now()
    date = str(x.strftime("%Y") + x.strftime("%m") + x.strftime("%d"))

    addIssue("Unnamed", date, " ", url, [['p', ""]], [[""]])
    return redirect("/admin/issues/" + url)

@app.route('/changeIssue', methods=['POST'])
def changeIssue():
    if not loggedIn():
        return redirect('/admin/login')
    url = request.form['url']
    decision = request.form['decision']

    if decision == "toggle":
        toggleIssuePublicity(url)
    else:
        deleteIssue(url)
    return redirect('/admin/issues')

@app.route('/admin/issues/<id>', methods=['GET', 'POST'])
def adminIssue(id):
    if not loggedIn():
        return redirect('/admin/login')
    issue, sections, texts = getIssue(id)
    print("retrieved: ")
    print(texts)
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        text = request.form.getlist('text')
        texts = []
        group = []
        for item in text:
            if item != "Among us":
                group.append(item)
            else:
                texts.append(group)
                group = []
        print("saved:")
        print(texts)
        files = upload_file()

        pastImages = []
        for section in sections:
            pastImages.append(section[1])

        for i in range(len(files)):
            if files[i] == "":
                if i < len(pastImages):
                    files[i] = pastImages[i]

        x = datetime.datetime.now()
        date = str(x.strftime("%Y") + x.strftime("%m") + x.strftime("%d"))

        newFiles = [['p', x] for x in files]

        deleteIssue(id)
        addIssue(title, date, desc, id, newFiles, texts)
        return redirect("/admin/issues/"+id)

    return render_template('admin-editissue.html', name=issue[0], issue=issue, sections=sections, texts=texts)

@app.route('/admin/blog', methods=['GET', 'POST'])
def adminBlog():
    if not loggedIn():
        return redirect('/admin/login')
    if request.method == 'POST':
        id = request.form['number']
        if request.form['decision'] == 'delete':
            deletePost(id)
        else:
            toggleBlogPostPublicity(id)
    posts = getBlogPosts()
    return render_template('admin-blog.html', name="Blog", posts=posts)

@app.route('/admin/blog/upload', methods=['GET', 'POST'])
def uploadBlog():
    if not loggedIn():
        return redirect('/admin/login')
    x = datetime.datetime.now()
    date = str(x.strftime("%Y") + x.strftime("%m") + x.strftime("%d"))

    if request.method == 'POST':
        title = request.form['title']
        text  = request.form['text']
        imagename = upload_file()
        imagename.pop(-1)
        print(imagename)
        print("posting!")
        addBlogPost(title, date, text, imagename)
        return redirect('/admin/blog')

    return render_template('admin-uploadBlog.html', name='Upload to Blog')

'''
@app.route('/admin/blog/edit/<id>', methods=['GET', 'POST'])
def editBlog(id):
    post = getBlogPost(id)

    x = datetime.datetime.now()
    date = str(x.strftime("%Y") + x.strftime("%m") + x.strftime("%d"))

    if request.method == 'POST':
        title = request.form['title']
        text  = request.form['text']
        imagename = upload_file()
        print(imagename)
        print("posting!")
        updateBlogPost(title, date, text, imagename, id)

    return render_template('admin-editBlog.html', name='Upload to Blog', post=post)
'''

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')

# Upload content
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

# run the app
if __name__ == "__main__":
    app.run(debug=True)