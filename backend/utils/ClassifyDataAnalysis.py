def betterBytes(data):
    if data>=1024*1024*1024:
        data=data/(1024*1024*1024)
        data=f'{data:.2f}GB'
    elif data>=1024*1024:
        data=data/(1024*1024)
        data=f'{data:.2f}MB'
    elif data>=1024:
        data=data/1024
        data=f'{data:.2f}KB'
    else:
        data=f'{data:.2f}B'
    return data

def analysisData(PreliminaryProcessingData:list):
    #ProcessedData: [ApplicationCategoryNameCount,CatchTime,TotalBytes,TotalRate]
    FlowNum=0
    ApplicationCategoryNameCount=PreliminaryProcessingData[0]
    for i in ApplicationCategoryNameCount:
        FlowNum+=ApplicationCategoryNameCount[i]
    CatchTime=PreliminaryProcessingData[1]
    TotalBytes=PreliminaryProcessingData[2]
    TotalRate=PreliminaryProcessingData[3]
    TotalBytes=betterBytes(TotalBytes)
    TotalRate=betterBytes(TotalRate)
    analysis=f'本次抓包共捕获{FlowNum}条流量，抓包时间为{CatchTime:.2f}秒，总流量为{TotalBytes}，平均流量速率为{TotalRate}ps。'


    return analysis