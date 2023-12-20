import win32com.client
'''
返回用户电脑的网卡设备名字
'''
def GetNetworkAdapters():
    Adapters=[]
    wmi = win32com.client.GetObject ("winmgmts:")
    for adapter in wmi.InstancesOf ("Win32_NetworkAdapter"):
        Adapters.append({'value': adapter.Name, 'label': adapter.Name})
    return Adapters
def run():
    print('SearchNIC')

