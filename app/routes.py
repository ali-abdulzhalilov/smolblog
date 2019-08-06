from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    posts = [{'title':'Hello', 'body':'Lorem ipsum dolor sit amet.'},
    {'title':'pep', 'body':'Ipsum lorem'}]
    return render_template('index.html', title='Home', posts=posts)
