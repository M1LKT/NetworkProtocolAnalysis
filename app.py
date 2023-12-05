from flask import Flask,render_template,url_for,jsonify
from markupsafe import escape
import utils.FlowCatch
from flask_cors import CORS
import json
import common.Result as R

app = Flask(__name__)
CORS(app)

@app.route('/hello')
def hello():
    return '<h1>Hello Totoro!</h1>'
@app.route('/user/<name>')
def user_page(name):
    return f'User page {escape(name)}' #使用 MarkupSafe（Flask 的依赖之一）提供的 escape() 函数对 name 变量进行转义处理，比如把 < 转换成 &lt;
@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='greyli'))
    print(utils.FlowCatch.Catch())
    return 'Test page'
@app.route('/FlowCatch/<FlowNum>')
def CatchFlow(FlowNum:int):
    if not FlowNum >=0:
        FlowNum=5
    utils.FlowCatch.Clear()
    callback=utils.FlowCatch.Catch(FlowNum) 
    return render_template('result.html',callback=callback )
@app.route('/')
def FlowPacket():
    utils.FlowCatch.Clear()
    callback=utils.FlowCatch.catch(5) #获得一个data
    return jsonify(R.Result.success(callback)),{"Content-Type":"application/json"}