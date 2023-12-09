from scapy.all import *
import time
import datetime

CallBack=[]
PacketObject=[]
def flagvalue_to_json(flagvalue):
    # 将 FlagValue 对象转换为可以序列化为 JSON 的数据
    return str(flagvalue)
def packet_callback(packet):
    DataCache=dict()
    if packet.haslayer('Ether'):
        Ehter_packet=packet['Ether']
        src_mac=Ehter_packet.src
        dst_mac=Ehter_packet.dst
        Ethtype=Ehter_packet.type
        DataCache['Ether']={"src":src_mac,"dst":dst_mac,"type":Ethtype}
    if packet.haslayer('IP'):
        ip_packet = packet['IP']
        timestamp = packet.time
        src_ip = ip_packet.src
        dst_ip = ip_packet.dst
        protocol = ip_packet.proto
        total_length = ip_packet.len
        ttl = ip_packet.ttl
        df = flagvalue_to_json(ip_packet.flags.DF)
        mf = flagvalue_to_json(ip_packet.flags.MF)
        offset = ip_packet.frag
        checksum = ip_packet.chksum
        DataCache['IP'] = {
        "timestamp": timestamp,
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "protocol": protocol,
        "total_length": total_length,
        "ttl": ttl,
        "df": df,
        "mf": mf,
        "offset": offset,
        "checksum": checksum
        }
    if packet.haslayer('IPV6'):
        ipv6_packet = packet['IPV6']
        timestamp = packet.time
        src_ip = ipv6_packet.src
        dst_ip = ipv6_packet.dst
        next_header = ipv6_packet.nh
        hop_limit = ipv6_packet.hlim
        flow_label = ipv6_packet.fl
        payload_length = ipv6_packet.plen
        traffic_class = ipv6_packet.tc
        DataCache['IPV6'] = {
            "timestamp": timestamp,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "next_header": next_header,
            "hop_limit": hop_limit,
            "flow_label": flow_label,
            "payload_length": payload_length,
            "traffic_class": traffic_class
        }
    if packet.haslayer('TCP'):
        TCP_packet = packet['TCP']
        TCP_src_port = TCP_packet.sport
        TCP_dst_port = TCP_packet.dport
        TCP_seq = TCP_packet.seq
        TCP_ack = TCP_packet.ack
        TCP_dataofs = TCP_packet.dataofs
        TCP_reserved = TCP_packet.reserved
        TCP_flags = flagvalue_to_json(TCP_packet.flags)
        TCP_window = TCP_packet.window
        TCP_chksum = TCP_packet.chksum
        TCP_urgptr = TCP_packet.urgptr
        TCP_options = TCP_packet.options
        DataCache['TCP'] = {
            "src_port": TCP_src_port,
            "dst_port": TCP_dst_port,
            "seq": TCP_seq,
            "ack": TCP_ack,
            "dataofs": TCP_dataofs,
            "reserved": TCP_reserved,
            "flags": TCP_flags,
            "window": TCP_window,
            "chksum": TCP_chksum,
            "urgptr": TCP_urgptr,
            "options": TCP_options
        }
    if packet.haslayer('UDP'):
        Udp_packet = packet['UDP']
        Udp_sport = Udp_packet.sport
        Udp_dport = Udp_packet.dport
        Udp_len=Udp_packet.len
        Udp_chksum=Udp_packet.chksum
        Udp_data = Udp_packet.payload
        DataCache['UDP'] = {
            "src_port": Udp_sport,
            "dst_port": Udp_dport,
            "len":Udp_len,
            "chksum":Udp_chksum,
        }
    if packet.haslayer('DNS'):
        Dns_packet = packet['DNS']
        Dns_id = Dns_packet.id
        Dns_qr = flagvalue_to_json(Dns_packet.qr)
        Dns_opcode = Dns_packet.opcode
        Dns_aa = Dns_packet.aa
        Dns_tc = Dns_packet.tc
        Dns_rd = Dns_packet.rd
        Dns_ra = Dns_packet.ra
        Dns_z = Dns_packet.z
        Dns_ad = Dns_packet.ad
        Dns_cd = Dns_packet.cd
        Dns_rcode = Dns_packet.rcode
        Dns_qdcount = Dns_packet.qdcount
        Dns_ancount = Dns_packet.ancount
        Dns_nscount = Dns_packet.nscount
        Dns_arcount = Dns_packet.arcount
        Dns_qd=Dns_packet.qd
        Dns_an=Dns_packet.an
        Dns_ns=Dns_packet.ns
        Dns_ar=Dns_packet.ar
        DataCache['DNS'] = {
            "id": Dns_id,
            "qr": Dns_qr,
            "opcode": Dns_opcode,
            "aa": Dns_aa,
            "tc": Dns_tc,
            "rd": Dns_rd,
            "ra": Dns_ra,
            "z": Dns_z,
            "ad": Dns_ad,
            "cd": Dns_cd,
            "rcode": Dns_rcode,
            "qdcount": Dns_qdcount,
            "ancount": Dns_ancount,
            "nscount": Dns_nscount,
            "arcount": Dns_arcount,
            "qd":Dns_qd,
            "an":Dns_an,
            "ns":Dns_ns,
            "ar":Dns_ar
        }
    print(DataCache)
    FlowDict={"summary":packet.summary(),"exactinfo":DataCache}
    PacketObject.append(FlowDict)
    CallBack.append(packet.summary())
def Catch(count:int):
    sniff(prn=packet_callback,count=count,iface='Realtek Gaming 2.5GbE Family Controller',filter='')
    return CallBack
def catch(count:int=5,Adapter='',Filter=''):
    sniff(prn=packet_callback,count=count,iface=Adapter,filter=Filter)
    return PacketObject
def Clear():
    CallBack.clear()
    PacketObject.clear()