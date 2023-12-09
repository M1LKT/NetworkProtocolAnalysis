from scapy.packet import Packet
import json

from scapy.layers.dns import DNSQR

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DNSQR):
            return str(obj)
        if isinstance(obj, bytes):
            return str(obj)  # 或者使用你需要的其他编码
        return super().default(obj)