from scapy.all import *
import time
import datetime

CallBack=[]
PacketObject=[]
def packet_callback(packet):
    if packet.haslayer('IP'):
        Ehter_packet=packet['Ether']
        ip_packet = packet['IP']
        src_mac=Ehter_packet.src
        dst_mac=Ehter_packet.dst
        timestamp = packet.time
        local_time = datetime.datetime.fromtimestamp(timestamp)
        formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
        src_ip = ip_packet.src
        dst_ip = ip_packet.dst
        protocol = ip_packet.proto
        total_length = ip_packet.len
        ttl = ip_packet.ttl
        df = ip_packet.flags.DF
        mf = ip_packet.flags.MF
        offset = ip_packet.frag
        checksum = ip_packet.chksum
    if packet.haslayer('UDP'):
        Udp_packet=packet['UDP']
        src_port=Udp_packet.sport
        dst_port=packet['UDP'].dport
    if packet.haslayer('TCP'):
        src_port=packet['TCP'].sport
        dst_port=packet['TCP'].dport
    print()
    FlowDict={"summary":packet.summary()}
    PacketObject.append(FlowDict)
    CallBack.append(packet.summary())
def Catch(count:int):
    sniff(prn=packet_callback,count=count,iface='Realtek Gaming 2.5GbE Family Controller',filter='')
    return CallBack
def catch(count:int=5):
    sniff(prn=packet_callback,count=count,iface='Realtek Gaming 2.5GbE Family Controller',filter='')
    return PacketObject
def Clear():
    CallBack.clear()
    PacketObject.clear()