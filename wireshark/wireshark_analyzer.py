import json

def packet_combination(ws_data):
    keys_map = {}
    for i in range(len(ws_data)):
        if str(ws_data[i]["_source"]["layers"].keys()) not in keys_map:
            keys_map[str(ws_data[i]["_source"]["layers"].keys())] = 1
        else:
            keys_map[str(ws_data[i]["_source"]["layers"].keys())] += 1
    keys_list = sorted(keys_map.items(), key=lambda d: d[1], reverse=True)
    del keys_map
    return keys_list

def packet_key_cnt(ws_data):
    keys_count = {}
    for i in range(len(ws_data)):
        key_list = ws_data[i]["_source"]["layers"].keys()
        for key in key_list:
            if key in keys_count:
                keys_count[key] += 1
            else:
                keys_count[key] = 1
    keys_count = sorted(keys_count.items(), key=lambda d: d[1], reverse=True)
    #sum = 0
    #for i in range(len(keys_count)):
    #    sum += keys_count[i][1]
    for i in range(len(keys_count)):
        tmp = list(keys_count[i])
        #tmp.append(float(keys_count[i][1])/float(sum))
        tmp.append(float(keys_count[i][1])/float(keys_count[0][1])) # Divide by frame (packet based)
        keys_count[i] = tuple(tmp)
    return keys_count

    
def packet_ip_connection(ws_data):
    ip_map = {}
    sum_cnt = 0
    for i in range(len(ws_data)):
        if "ip" in ws_data[i]["_source"]["layers"].keys():
            ipsrc = ws_data[i]["_source"]["layers"]["ip"]["ip.src"]
            ipdst = ws_data[i]["_source"]["layers"]["ip"]["ip.dst"]
            sum_cnt += 1
            if ipsrc not in ip_map.keys():
                ip_map[ipsrc] = {}
                ip_map[ipsrc][ipdst] = 1
            else:
                if ipdst not in ip_map[ipsrc].keys():
                    ip_map[ipsrc][ipdst] = 1
                else:
                    ip_map[ipsrc][ipdst] += 1
    sort_ip = []
    for src_ip in ip_map.keys():
        for dst_ip in ip_map[src_ip].keys():
            tmp = []
            tmp.append("{:<16} - {:<16}".format(src_ip, dst_ip))
            tmp.append(ip_map[src_ip][dst_ip])
            tmp.append(float(ip_map[src_ip][dst_ip])/float(sum_cnt))
            sort_ip.append(tuple(tmp))
    sort_ip.sort(key=lambda tup: tup[1], reverse=True)
    return sort_ip


def packet_ip_count(ws_data):
    ip_map = {}
    sum_cnt = 0
    for i in range(len(ws_data)):
        if "ip" in ws_data[i]["_source"]["layers"].keys():
            ipsrc = ws_data[i]["_source"]["layers"]["ip"]["ip.src"]
            ipdst = ws_data[i]["_source"]["layers"]["ip"]["ip.dst"]
            sum_cnt += 1
            if ipsrc not in ip_map.keys():
                ip_map[ipsrc] = 1
            else:
                ip_map[ipsrc] += 1
            if ipdst not in ip_map.keys():
                ip_map[ipdst] = 1
            else:
                ip_map[ipdst] += 1
    ip_count = []
    for ip in ip_map.keys():
        tmp = []
        tmp.append("{:<16}".format(ip))
        tmp.append(ip_map[ip])
        tmp.append(float(ip_map[ip])/float(sum_cnt))
        ip_count.append(tuple(tmp))
    ip_count.sort(key=lambda tup: tup[1], reverse=True)
    return ip_count

    
def json_analyze(path_list):
    keys_list = {}
    keys_count = {}
    sort_ip = {}
    ip_count = {}
    
    for json_path in path_list:
        print(f"\n\n{json_path}")

        with open(json_path, "r", encoding="utf8", errors='ignore') as f:
            ws_data = json.load(f)
            
        print(f"\nPacket combination")
        keys_list[json_path] = packet_combination(ws_data)
        for item, val in keys_list[json_path]:
            print(f"{val} \t {item}")
            
            
        print(f"\nPacket keys count")
        keys_count[json_path] = packet_key_cnt(ws_data)
        for item, val, ratio in keys_count[json_path]:
            print("{} \t {:.2f} % \t {}".format(val, ratio*100, item))
    

        print(f"\nPacket IP connection")
        sort_ip[json_path] = packet_ip_connection(ws_data)
        for ip, cnt, ratio in sort_ip[json_path]:
            print("{} \t {:.2f} % \t {}".format(cnt, ratio*100, ip))
            if ratio*100 < 0.1:
                break
            
        print(f"\nPacket IP count")
        ip_count[json_path] = packet_ip_count(ws_data)
        for ip, cnt, ratio in ip_count[json_path]:
            print("{} \t {:.2f} % \t {}".format(cnt, ratio*100, ip))
            if ratio*100 < 0.1:
                break
            
        del ws_data
    del keys_count
    del keys_list
    del sort_ip
    del ip_count
    
#path_list = ["Train/Person_"+ str(person) +"/Wireshark.json" for person in range(1,7)]
#path_list += ["Example Test/Test_"+ str(person) +"/Wireshark.json" for person in range(1,3)]
#json_analyze(path_list)

