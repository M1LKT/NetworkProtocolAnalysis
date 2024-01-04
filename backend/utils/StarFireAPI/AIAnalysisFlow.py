import utils.StarFireAPI.SparkApi as SparkApi
import json
def load_config():
    with open('utils\\StarFireAPI\\config.json', 'r') as f:
        config = json.load(f)
    return config

config = load_config()
#以下密钥信息从控制台获取
appid = config['AppId']     #填写控制台中获取的 APPID 信息
api_secret = config['APISecret']   #填写控制台中获取的 APISecret 信息
api_key =config['APIKey']    #填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
domain = config['domain']   # v1.5版本
# domain = "generalv2"    # v2.0版本
#云端环境的服务地址
Spark_url = config['Spark_url']  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


text =[]

# length = 0

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    

# testquestion='''这是我抓取的流量，我将他进行了统计,其中第一行中的信息是各个应用经过的流量数量，第二个是将这些应用分类为'低延时', '保证延时', '保证交付', '尽最大努力交付', '其他业务'五种业务，再统计业务的流量数量，第三行是和第二行一一对应的五种业务的流量速率，单位是Bps。请注意：第一、二行是流量的数量，单位是条。{'Web': 230, 'Unspecified': 25, 'Network': 124, 'Chat': 11, 'Download': 4, 'Cloud': 19, 'System': 6, 'Collaborative': 1}
# {'Lowlatency': 0, 'Guaranteedlatency': 354, 'GuaranteedDelivery': 24, 'BestEffortDelivery': 17, 'Other': 25},[Decimal('0E+6'), Decimal('3738.431460398619252626316723'), Decimal('990.6789087367056426786108809'), Decimal('315.8161905254379414592377629'), Decimal('61581.18771585021858350070868')] 你能对这些数据进行分析并且给出一些意见吗'''
testquestion='你好'


def getAnswer(question :str =testquestion):
    text.clear
    question = checklen(getText("user",question))
    SparkApi.answer =""
    SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    getText("assistant",SparkApi.answer)
    return SparkApi.answer

def questionTemplate(ProcessedData):
    #ProcessedData: [ApplicationCategoryNameCount,CatchTime,TotalBytes,TotalRate,Bussiness,TransSpeed]
    question=f"这是我抓取的流量，我将他进行了统计,其中第一行中的信息是各个应用经过的流量数量，第二个是将这些应用分类为'低延时', '保证延时', '保证交付', '尽最大努力交付', '其他业务'五种业务，再统计业务的流量数量，第三行是和第二行一一对应的五种业务的流量速率，单位是Bps。请注意：第一、二行是流量的数量，单位是条。{ProcessedData[0]},{ProcessedData[4]},{ProcessedData[5]} 你能对这些数据进行分析并且给出一些意见吗"
    return question
