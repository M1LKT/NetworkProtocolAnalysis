from flask import Flask,render_template,url_for,jsonify,request,send_from_directory
from markupsafe import escape
import utils.FlowCatch
import utils.CustomEncoder
from flask_cors import CORS
import json
import common.Result as R
import utils.SearchNIC
import utils.FlowClassify
import utils.ClassifyDataAnalysis
from utils.StandardizedData import standardizedData
import utils.StarFireAPI.AIAnalysisFlow as AIAnalysisFlow

#测试用
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)
app.json_encoder = utils.CustomEncoder.CustomJSONEncoder

NICPacket=utils.SearchNIC.GetNetworkAdapters()

@app.route('/user/<name>')
def user_page(name):
    return f'User page {escape(name)}' #使用 MarkupSafe（Flask 的依赖之一）提供的 escape() 函数对 name 变量进行转义处理，比如把 < 转换成 &lt;
@app.route('/',methods=['POST'])
def FlowPacket():
    utils.FlowCatch.Clear()
    data=request.get_data()
    Settings=json.loads(data)
    callback=utils.FlowCatch.catch(Settings['Counts'],Settings['Adapter'],Settings['Filter'])
    try:
        return jsonify(R.Result.success(data=callback)),{"Content-Type":"application/json"}
    except:
        print()
        print(callback)
        return jsonify(R.Result.success(data=callback)),{"Content-Type":"application/json"}
@app.route('/SearchNIC')
def NICSearch():
    return jsonify(R.Result.success(data=NICPacket)),{"Content-Type":"application/json"}
@app.route('/SendJson',methods=['POST'])
def Recive():
    utils.FlowCatch.Clear()
    data=request.get_data()
    Settings=json.loads(data)  #获得一个包含了Filter、Adapter、Counts属性的字典
    callback=utils.FlowCatch.catch(Settings['Counts'],Settings['Adapter'],Settings['Filter'])
    return jsonify(R.Result.success(data=callback)),{"Content-Type":"application/json"}
@app.route('/PcapFile',methods=['POST','GET'])
def PcapFile():
    global PreliminaryProcessingData
    if 'file' not in request.files:
        return jsonify(R.Result.error("No file part")), {"Content-Type": "application/json"}

    file = request.files['file']

    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分，所以需要检查文件是否存在
    if file.filename == '':
        return jsonify(R.Result.error("No selected file")), {"Content-Type": "application/json"}

    if file:
        filename = file.filename
        basename, extension = os.path.splitext(filename)
        if not(extension == '.pcap'or extension == '.pcapng'):
            return jsonify(R.Result.error(msg="请上传pcap或pcapng文件！")), {"Content-Type": "application/json"}
        # 使用 Werkzeug 的 secure_filename 函数确保文件名是安全的
        filename = secure_filename(file.filename)
        # 保存文件到服务器
        file.save(os.path.join('./pcapreceive', filename))
        PreliminaryProcessingData=utils.FlowClassify.classifyFlow(filename)
        #PreliminaryProcessingData:[ApplicationCategoryNameCount,CatchTime,TotalBytes,TotalRate,Bussiness,TransSpeed]
        AnalysisResult=utils.ClassifyDataAnalysis.analysisData(PreliminaryProcessingData)
        standarddata=standardizedData(
            AnalysisResult=AnalysisResult,
            Image1={'imageName':'ProportionOfBusinessTraffic.png'},
            Image2={'imageName':'NumberOfTrafficCommunicationHosts.png'},
            Image3={'imageName':'ServiceTrafficRate.png'}
            )
        return jsonify(R.Result.success(msg="分析完成!",data=standarddata)),{"Content-Type":"application/json"}
        #返回data中包含分析结果，一个列表，列表中是图片的字典，包含图片名，用于前端调用get_image函数
@app.route('/get_image/<image_name>',methods=['GET'])
def get_image(image_name):
    return send_from_directory('utils/analysisPic', image_name)

@app.route('/AIAnalysisFlow',methods=['POST'])
def AIAnswerTest():
    global PreliminaryProcessingData
    question=AIAnalysisFlow.questionTemplate(PreliminaryProcessingData)
    aianswer=AIAnalysisFlow.getAnswer(question)
    return jsonify(R.Result.success(data=aianswer)),{"Content-Type":"application/json"}
