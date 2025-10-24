from flask import render_template
from app import app

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('authentication/login.html')

@app.route('/signup')
def signup():
    return render_template('authentication/signup.html')
