from flask import Flask, flash, render_template, redirect, url_for, request, send_from_directory
from db_managment import *
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import datetime

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# SITE SETUP
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            flash('No file part')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return file.filename

@app.route('/')
def index():

    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html', name="Home")

@app.route('/ShowYourSolidarity')
def SYS():
    return render_template('SYS.html', name="Show Your Solidarity")

@app.route('/issues')
def issues():
    issues = getIssueBasic()
    return render_template('issues.html', name="Issues", issues=issues)

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
@app.route('/admin/blog', methods=['GET', 'POST'])
def adminBlog():
    if request.method == 'POST':
        print("yo")
        id = request.form['postNumber']
        toggleBlogPostPublicity(id)
    posts = getBlogPosts()
    return render_template('adminBlog.html', name="Blog", posts=posts)

@app.route('/admin/blog/upload', methods=['GET', 'POST'])
def uploadBlog():
    x = datetime.datetime.now()
    date = str(x.strftime("%Y") + x.strftime("%m") + x.strftime("%d"))

    if request.method == 'POST':
        title = request.form['title']
        text  = request.form['text']
        imagename = upload_file()
        print(imagename)
        print("posting!")
        addBlogPost(title, date, text, [imagename])

    return render_template('uploadBlog.html', name='Upload to Blog')

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
        updateBlogPost(title, date, text, [imagename], id)

    return render_template('editBlog.html', name='Upload to Blog', post=post)

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