from flask import Flask,render_template,url_for,jsonify,request
from markupsafe import escape
import utils.FlowCatch
import utils.CustomEncoder
from flask_cors import CORS
import json
import common.Result as R
import utils.SearchNIC

app = Flask(__name__)
CORS(app)
app.json_encoder = utils.CustomEncoder.CustomJSONEncoder

NICPacket=utils.SearchNIC.GetNetworkAdapters()
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
@app.route('/',methods=['POST'])
def FlowPacket():
    utils.FlowCatch.Clear()
    data=request.get_data()
    Settings=json.loads(data)
    callback=utils.FlowCatch.catch(Settings['Counts'],Settings['Adapter'],Settings['Filter'])
    try:
        return jsonify(R.Result.success(callback)),{"Content-Type":"application/json"}
    except:
        print()
        print(callback)
        return jsonify(R.Result.success(callback)),{"Content-Type":"application/json"}
@app.route('/SearchNIC')
def NICSearch():
    return jsonify(R.Result.success(NICPacket)),{"Content-Type":"application/json"}
@app.route('/SendJson',methods=['POST'])
def Recive():
    utils.FlowCatch.Clear()
    data=request.get_data()
    Settings=json.loads(data)  #获得一个包含了Filter、Adapter、Counts属性的字典
    callback=utils.FlowCatch.catch(Settings['Counts'],Settings['Adapter'],Settings['Filter'])
    return jsonify(R.Result.success(callback)),{"Content-Type":"application/json"}