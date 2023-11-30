from flask import Flask
import escape

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello Totoro!</h1>'
@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'