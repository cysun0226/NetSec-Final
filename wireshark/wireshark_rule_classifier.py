import json
import os
import math
from argparse import ArgumentParser

from .wireshark_analyzer import packet_key_cnt, packet_ip_count

train_weight ={
    1: {"tcp": 74.13, "udp": 25.76, "http": 1.18, "140": 0.52, "163": 0.50},
    2: {"tcp": 99.15, "udp": 0.84, "http": 0.03, "140": 72.64, "163": 0.27},
    3: {"tcp": 8.70, "udp": 91.27, "http": 0.00, "140": 61.23, "163": 0.00},
    4: {"tcp": 99.49, "udp": 0.51, "http": 0.11, "140": 59.91, "163": 1.21},
    5: {"tcp": 98.25, "udp": 1.74, "http": 1.35, "140": 0.31, "163": 84.95},
    6: {"tcp": 91.59, "udp": 8.39, "http": 8.53, "140": 0.09, "163": 58.71}
}

def cosine_similarity(dic1,dic2):
    sum11, sum12, sum22 = 0, 0, 0
    for key in dic1:
        x = dic1[key]; y = dic2[key]
        sum11 += x*x
        sum22 += y*y
        sum12 += x*y
    return sum12/math.sqrt(sum11*sum22)


def euclidean_distance_similarity(dic1,dic2):
    sum_distance = 0.0
    for key in dic1:
        sum_distance += pow(dic1[key] - dic2[key], 2)
    return 1/math.sqrt(sum_distance)


def json_classifier(json_path):
    with open(json_path, "r", encoding="utf8", errors='ignore') as f:
        ws_data = json.load(f)

    rating = {"tcp": 0.0, "udp": 0.0, "http": 0.0, "140": 0.0, "163": 0.0}

    keys_count = packet_key_cnt(ws_data)
    for item, val, ratio in keys_count:
        if item == "udp":
            rating["udp"] = ratio*100
        elif item == "tcp":
            rating["tcp"] = ratio*100
        elif item == "http":
            rating["http"] = ratio*100
    
    ip_count = packet_ip_count(ws_data)
    for ip, cnt, ratio in ip_count:
        if ip.startswith("140.113"):
            rating["140"] += ratio*100
        elif ip.startswith("163.28"):
            rating["163"] += ratio*100
    
    raw_result = {1:0.0, 2:0.0, 3:0.0, 4:0.0, 5:0.0, 6:0.0}
    normalized_result = {}

    tmp_sum = 0.0
    for i in range(1,7):
        raw_result[i] = cosine_similarity(rating, train_weight[i])
        tmp_sum += raw_result[i]

    for i in range(1,7):
        normalized_result[i] = raw_result[i]/tmp_sum

    del ws_data
    del keys_count
    del ip_count
    return normalized_result

def wireshark_predict(json_path):
    return json_classifier(json_path)

# def main():
#     args = build_argparser().parse_args()
#     test_path = args.file_path
    
#     #test_path = "./Example Test" 
#     #test_path = "./Train"
    
#     case_list = [os.path.join(test_path, o) for o in os.listdir(test_path) 
#                 if os.path.isdir(os.path.join(test_path,o))]
    
#     for case_path in case_list:
#         json_path = os.path.join(case_path, "Wireshark.json")
#         json_result = json_classifier(json_path)
        
#         ### json_result = {1:val, 2:val, 3:val, 4:val, 5:val, 6:val}
#         ### sum of val = 1.0

#         result = max(json_result, key=json_result.get)
#         print("{}: person {}".format(os.path.basename(case_path), result))
        
# if __name__ == '__main__':
#     main()

