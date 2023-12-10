from scapy.all import *
import time
import datetime
import utils.scapy_http as http
import scapy.layers.http as Http

CallBack=[]
PacketObject=[]
def DnsrrDict(dnsrr_packet):
    dnsrrDict={
        "rrname":dnsrr_packet.rrname,
        "type":dnsrr_packet.type,
        "rclass":dnsrr_packet.rclass,
        "ttl":dnsrr_packet.ttl,
        "rdlen":dnsrr_packet.rdlen,
        "rdata":dnsrr_packet.rdata
    }
    return dnsrrDict
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
        for i, option in enumerate(TCP_options):
            if isinstance(option[1], bytes):
                TCP_options[i] = (option[0], option[1].decode())
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
        Dns_qd={
            "qname":str(Dns_packet.qd.qname),
            "qtype":Dns_packet.qd.qtype,
            "qclass":Dns_packet.qd.qclass
        }
        Dns_an=str(Dns_packet.an)
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
    if packet.haslayer('Raw'):
        Raw_packet = packet['Raw']
        Raw_load = Raw_packet.load
        try:
            http_packet=Http.HTTP(Raw_load)
            DataCache['HTTP']={
                "load":http_packet.fields,
            }
            # Http_request = http.HTTPRequest(Raw_load)
            # Http_method = Http_request.Method
            # Http_path = Http_request.Path
            # Http_version = Http_request.Http_Version
            # Http_host = Http_request.Host
            # Http_user_agent = Http_request.User_Agent
            # Http_accept = Http_request.Accept
            # Http_accept_language = Http_request.Accept_Language
            # Http_accept_encoding = Http_request.Accept_Encoding
            # Http_accept_charset = Http_request.Accept_Charset
            # Http_referer = Http_request.Referer
            # Http_authorization = Http_request.Authorization
            # Http_expect = Http_request.Expect
            # Http_from = Http_request.From
            # Http_if_match = Http_request.If_Match
            # Http_if_modified_since = Http_request.If_Modified_Since
            # Http_if_none_match = Http_request.If_None_Match
            # Http_if_range = Http_request.If_Range
            # Http_if_unmodified_since = Http_request.If_Unmodified_Since
            # Http_max_forwards = Http_request.Max_Forwards
            # Http_proxy_authorization = Http_request.Proxy_Authorization
            # Http_range = Http_request.Range
            # Http_te = Http_request.TE
            # Http_cache_control = Http_request.Cache_Control
            # Http_connection = Http_request.Connection
            # Http_date = Http_request.Date
            # Http_pragma = Http_request.Pragma
            # Http_trailer = Http_request.Trailer
            # Http_transfer_encoding = Http_request.Transfer_Encoding
            # Http_upgrade = Http_request.Upgrade
            # Http_via = Http_request.Via
            # Http_warning = Http_request.Warning
            # Http_keep_alive = Http_request.Keep_Alive
            # Http_allow = Http_request.Allow
            # Http_content_encoding = Http_request.Content_Encoding
            # Http_content_language = Http_request.Content_Language
            # Http_content_length = Http_request.Content_Length
            # Http_content_location = Http_request.Content_Location
            # Http_content_md5 = Http_request.Content_MD5
            # Http_content_range = Http_request.Content_Range
            # Http_content_type = Http_request.Content_Type
            # Http_expires = Http_request.Expires
            # Http_last_modified = Http_request.Last_Modified
            # Http_cookie = Http_request.Cookie
            # Http_headers = Http_request.Headers
            # Http_additional_headers = Http_request.Additional_Headers

            # DataCache['HTTP'] = {
            #     "Method": Http_method,
            #     "Path": Http_path,
            #     "Http_Version": Http_version,
            #     "Host": Http_host,
            #     "User_Agent": Http_user_agent,
            #     "Accept": Http_accept,
            #     "Accept_Language": Http_accept_language,
            #     "Accept_Encoding": Http_accept_encoding,
            #     "Accept_Charset": Http_accept_charset,
            #     "Referer": Http_referer,
            #     "Authorization": Http_authorization,
            #     "Expect": Http_expect,
            #     "From": Http_from,
            #     "If_Match": Http_if_match,
            #     "If_Modified_Since": Http_if_modified_since,
            #     "If_None_Match": Http_if_none_match,
            #     "If_Range": Http_if_range,
            #     "If_Unmodified_Since": Http_if_unmodified_since,
            #     "Max_Forwards": Http_max_forwards,
            #     "Proxy_Authorization": Http_proxy_authorization,
            #     "Range": Http_range,
            #     "TE": Http_te,
            #     "Cache_Control": Http_cache_control,
            #     "Connection": Http_connection,
            #     "Date": Http_date,
            #     "Pragma": Http_pragma,
            #     "Trailer": Http_trailer,
            #     "Transfer_Encoding": Http_transfer_encoding,
            #     "Upgrade": Http_upgrade,
            #     "Via": Http_via,
            #     "Warning": Http_warning,
            #     "Keep_Alive": Http_keep_alive,
            #     "Allow": Http_allow,
            #     "Content_Encoding": Http_content_encoding,
            #     "Content_Language": Http_content_language,
            #     "Content_Length": Http_content_length,
            #     "Content_Location": Http_content_location,
            #     "Content_MD5": Http_content_md5,
            #     "Content_Range": Http_content_range,
            #     "Content_Type": Http_content_type,
            #     "Expires": Http_expires,
            #     "Last_Modified": Http_last_modified,
            #     "Cookie": Http_cookie,
            #     "Headers": Http_headers,
            #     "Additional_Headers": Http_additional_headers
            # }
        except:
            DataCache['Raw'] = {
            "load": str(Raw_load)
            }
    if packet.haslayer('Padding'):
        Padding_packet=packet['Padding']
        Padding_laod=Padding_packet.load
        DataCache['Padding']={
            "load":str(Padding_laod)
        }
    FlowDict={"summary":packet.summary(),"exactinfo":DataCache}
    PacketObject.append(FlowDict)
    CallBack.append(packet.summary())
    print(packet.show())
def Catch(count:int):
    sniff(prn=packet_callback,count=count,iface='Realtek Gaming 2.5GbE Family Controller',filter='')
    return CallBack
def catch(count:int=5,Adapter='',Filter=''):
    sniff(prn=packet_callback,count=count,iface=Adapter,filter=Filter)
    return PacketObject
def Clear():
    CallBack.clear()
    PacketObject.clear()