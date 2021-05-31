# views.py
from flask import render_template
from app import app

@app.route('/')
def index():
    return 'Hello World! from index'

@app.route('/about')
def about():
    return 'Hello World! from about'   