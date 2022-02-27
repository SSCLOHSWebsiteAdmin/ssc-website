from flask import Flask, render_template, redirect, url_for, request
from db_managment import *

# SITE SETUP
app = Flask(__name__)

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
    posts = getBlogPosts()
    print(posts)
    return render_template('blog.html', name="Blog", posts=posts)

# run the app
if __name__ == "__main__":
    app.run(debug=True)