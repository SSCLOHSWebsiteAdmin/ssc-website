from flask import Flask, render_template, redirect, url_for, request

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
    return render_template('issues.html', name="Issues")

@app.route('/CurrentEvents')
def currentEvents():
    return render_template('currentEvents.html', name="Current Events")

@app.route('/blog')
def blog():
    return render_template('blog.html', name="Blog")

# run the app
if __name__ == "__main__":
    app.run(debug=True)