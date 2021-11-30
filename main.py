from flask import Flask, render_template, redirect, url_for, request

# SITE SETUP
app = Flask(__name__)

@app.route('/')
def index():

    return render_template('home.html',name="Home")

# run the app
if __name__ == "__main__":
    app.run(debug=True)