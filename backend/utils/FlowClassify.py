from scapy.all import *
import nfstream
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from matplotlib.font_manager import FontProperties
import math

plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei是黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
os.getcwd()
class FlowSet:
    count=0
    hostset=set()
    totalbytes=0
    
    def bytesAdd(self,bytes):
        self.totalbytes+=bytes
    
    def hostAdd(self,host):
        self.hostset.add(host)
    
    def countAdd(self):
        self.count+=1

    def getHostNum(self):
        return len(self.hostset)
    
    def __init__(self):
        self.count = 0
        self.hostset = set()
        self.totalbytes = 0

    def averageRateOfServiceTraffic(self,catchtime):
        #单位：Bps
        return self.totalbytes/(catchtime)

def log10_positive(x):
    return math.log10(x) if x > 0 else 0

def classifyFlow(pcapfilename):
    ProcessedData=[]
    # 读取pcap文件
    analysisFilePath=f"pcapreceive\\{pcapfilename}"
    packets = rdpcap(analysisFilePath)
    CatchTime=packets[-1].time-packets[0].time
    streamer = nfstream.NFStreamer(source=analysisFilePath)
    # streamer = nfstream.NFStreamer(source="Packet\\shortcatch.pcapng")
    # 打印每个流的详细信息
    ApplicationCategoryNameCount=dict()
    Bussiness={"Lowlatency":0,"Guaranteedlatency":0,"GuaranteedDelivery":0,"BestEffortDelivery":0,"Other":0}
    '''
    Lowlatency：VoIP、Game 
    Guaranteedlatency：Web、Network 、Media
    GuaranteedDelivery：Download、Collaborative、Cloud、SoftwareUpdate
    BestEffortDelivery:System、Chat、Advertisement
    other:Unspecified
    '''
    Lowlatency=FlowSet()
    Guaranteedlatency=FlowSet()
    GuaranteedDelivery=FlowSet()
    BestEffortDelivery=FlowSet()
    Other=FlowSet()

    for flow in streamer:
        if flow.application_category_name in ApplicationCategoryNameCount:
            ApplicationCategoryNameCount[flow.application_category_name]+=1
        else:
            ApplicationCategoryNameCount[flow.application_category_name]=1
        if flow.application_category_name=="VoIP" or flow.application_category_name=="Game":
            Bussiness["Lowlatency"]+=1
            Lowlatency.countAdd()
            Lowlatency.hostAdd(flow.src_mac)
            Lowlatency.hostAdd(flow.dst_mac)
            Lowlatency.bytesAdd(flow.bidirectional_bytes)
        elif flow.application_category_name=="Web" or flow.application_category_name=="Network" or flow.application_category_name=="Media":
            Bussiness["Guaranteedlatency"]+=1
            Guaranteedlatency.countAdd()
            Guaranteedlatency.hostAdd(flow.src_mac)
            Guaranteedlatency.hostAdd(flow.dst_mac)
            Guaranteedlatency.bytesAdd(flow.bidirectional_bytes)
        elif flow.application_category_name=="Download" or flow.application_category_name=="Collaborative" or flow.application_category_name=="Cloud" or flow.application_category_name=="SoftwareUpdate":
            Bussiness["GuaranteedDelivery"]+=1
            GuaranteedDelivery.countAdd()
            GuaranteedDelivery.hostAdd(flow.src_mac)
            GuaranteedDelivery.hostAdd(flow.dst_mac)
            GuaranteedDelivery.bytesAdd(flow.bidirectional_bytes)
        elif flow.application_category_name=="System" or flow.application_category_name=="Chat" or flow.application_category_name=="Advertisement":
            Bussiness["BestEffortDelivery"]+=1
            BestEffortDelivery.countAdd()
            BestEffortDelivery.hostAdd(flow.src_mac)
            BestEffortDelivery.hostAdd(flow.dst_mac)
            BestEffortDelivery.bytesAdd(flow.bidirectional_bytes)
        else:
            Bussiness["Other"]+=1
            Other.countAdd()
            Other.hostAdd(flow.src_mac)
            Other.hostAdd(flow.dst_mac)
            Other.bytesAdd(flow.bidirectional_bytes)
    print(ApplicationCategoryNameCount)
    ProcessedData.append(ApplicationCategoryNameCount)
    print(Bussiness)

    # 创建饼图
    categories = ['低延时', '保证延时', '保证交付', '尽最大努力交付', '其他业务']
    font=FontProperties(fname='C:\Windows\Fonts\simhei.ttf')
    plt.figure()
    plt.pie(list(Bussiness.values()), labels=categories, autopct='%1.1f%%')
    plt.savefig('utils/analysisPic/ProportionOfBusinessTraffic.png')
    plt.figure()
    plt.figure(figsize=(10, 8))
    plt.bar(categories, [Lowlatency.getHostNum(),Guaranteedlatency.getHostNum(),GuaranteedDelivery.getHostNum(),BestEffortDelivery.getHostNum(),Other.getHostNum()])
    for bar in plt.bar(categories, [Lowlatency.getHostNum(),Guaranteedlatency.getHostNum(),GuaranteedDelivery.getHostNum(),BestEffortDelivery.getHostNum(),Other.getHostNum()]):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.03, yval, ha='center', va='bottom')  
    plt.xticks(rotation=315,fontproperties=font)
    plt.ylabel('主机数量（台）',fontproperties=font)
    plt.savefig('utils/analysisPic/NumberOfTrafficCommunicationHosts.png')

    i=0
    ProcessedData.append(CatchTime)
    TransSpeed=[
        Lowlatency.averageRateOfServiceTraffic(CatchTime),
        Guaranteedlatency.averageRateOfServiceTraffic(CatchTime),
        GuaranteedDelivery.averageRateOfServiceTraffic(CatchTime),
        BestEffortDelivery.averageRateOfServiceTraffic(CatchTime),
        Other.averageRateOfServiceTraffic(CatchTime)]
    DisposedSpeed=list(map(log10_positive,TransSpeed)) 
    plt.figure(figsize=(10, 8))
    plt.bar(categories, DisposedSpeed)
    for bar in plt.bar(categories, DisposedSpeed):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.03, f'{TransSpeed[i]:.2f}Bps', ha='center', va='bottom')
        i+=1
    plt.xticks(rotation=315,fontproperties=font)
    plt.ylabel('平均业务流量速率（经过对数处理）',fontproperties=font)
    plt.savefig('utils/analysisPic/ServiceTrafficRate.png')
    ProcessedData.append(Lowlatency.totalbytes+Guaranteedlatency.totalbytes+GuaranteedDelivery.totalbytes+BestEffortDelivery.totalbytes+Other.totalbytes) 
    #ProcessedData: [ApplicationCategoryNameCount,CatchTime,TotalBytes]
    ProcessedData.append(ProcessedData[2]/ProcessedData[1])
    #ProcessedData: [ApplicationCategoryNameCount,CatchTime,TotalBytes,TotalRate]
    return ProcessedData
def main():
    classifyFlow('Catch1.pcapng')
if __name__ == '__main__':
    main() 