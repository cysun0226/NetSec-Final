import json
import os
from argparse import ArgumentParser

from wireshark_analyzer import packet_key_cnt, packet_ip_count

def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("file_path", help="Path to the test dataset.", type=str)
    return parser

def json_classifier(json_path):
    with open(json_path, "r", encoding="utf8", errors='ignore') as f:
        ws_data = json.load(f)

    tcp_ratio = 0.0
    udp_ratio = 0.0
    http_ratio = 0.0
    keys_count = packet_key_cnt(ws_data)
    for item, val, ratio in keys_count:
        if item == "udp":
            udp_ratio = ratio*100
        elif item == "tcp":
            tcp_ratio = ratio*100
        elif item == "http":
            http_ratio = ratio*100
    
    ip140_113_ratio = 0.0
    ip163_28_ratio = 0.0
    ip_count = packet_ip_count(ws_data)
    for ip, cnt, ratio in ip_count:
        if ip.startswith("140.113"):
            ip140_113_ratio += ratio*100
        elif ip.startswith("163.28"):
            ip163_28_ratio += ratio*100
    
    #print("tcp: {:.2f} \t udp: {:.2f} \t http: {:.2f} \t 140: {:.2f} \t 163: {:.2f}".format(tcp_ratio, udp_ratio, http_ratio, ip140_113_ratio, ip163_28_ratio))
    
    if udp_ratio >= 65:                   # Top rule: udp >= 60%, person 3
        return 3
    elif ip140_113_ratio >= 35:           # Strong rule: 140.113.x.x >= 35%, person 2 or person 4
        if ip140_113_ratio >= 65:         # Weak rule: 140.113.x.x >= 65%, person 2. <65%, person 4.
            return 2
        else:
            return 4
    elif ip163_28_ratio >= 35:            # Strong rule: 163.28.x.x >= 35%, person 5 or person 6
        if udp_ratio>=4 or http_ratio>=4: # Rule: udp >= 4% or http >= 4% ,person 6
            return 6
        else:
            return 5
    elif udp_ratio >= 15:                 # Rule: fail to meet all rules above, and udp >= 15%, person 1
        return 1

    del ws_data
    del keys_count
    del ip_count
    return 1

def main():
    args = build_argparser().parse_args()
    test_path = args.file_path
    
    #test_path = "./Example Test" 
    #test_path = "./Train"
    
    case_list = [os.path.join(test_path, o) for o in os.listdir(test_path) 
                if os.path.isdir(os.path.join(test_path,o))]
    
    for case_path in case_list:
        json_path = os.path.join(case_path, "Wireshark.json")
        result = json_classifier(json_path)
        print("{}: person {}".format(os.path.basename(case_path), result))
        
if __name__ == '__main__':
    main()

