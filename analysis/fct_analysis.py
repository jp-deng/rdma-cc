# -*- coding: utf - 8 -*-
from optparse import OptionParser

def process_file(file_path):
    all_fct = []
    large_flow_fct = []
    small_flow_fct = []
    packets = []
    total_packet_size = 0
    all_start_time = []
    all_stop_time = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            data = line.strip().split(' ')
            packet_size = int(data[4])
            start_time = float(data[5])
            fct_value = float(data[6])

            total_packet_size += packet_size
            
            all_start_time.append(start_time)
            all_stop_time.append(start_time + fct_value)
            all_fct.append(fct_value)
            packets.append(packet_size)

            if packet_size >= 100* 1024:  # 10M in bytes
                large_flow_fct.append(fct_value)
            elif packet_size <= 100 * 1024:  # 100K in bytes
                small_flow_fct.append(fct_value)

    average_fct = sum(all_fct) / len(all_fct)
    large_flow_average_fct = sum(large_flow_fct) / len(large_flow_fct) if large_flow_fct else 0
    small_flow_average_fct = sum(small_flow_fct) / len(small_flow_fct) if small_flow_fct else 0

    all_fct.sort()
    index_99 = int(len(all_fct) * 0.99)
    index_95 = int(len(all_fct) * 0.95)

    fct_99 = all_fct[index_99]
    fct_95 = all_fct[index_95]

    all_start_time.sort()
    all_stop_time.sort()

    total_time = all_stop_time[-1] - all_start_time[0]
    average_goodput = total_packet_size * 8 / total_time / 256

    return average_fct, large_flow_average_fct, small_flow_average_fct, fct_99, fct_95, average_goodput

if __name__=="__main__":
    parser = OptionParser()

    parser.add_option("-m", "--traffic_mode", dest="traffic_mode",
                      help="traffic_mode parameter value", default="FbHdp")
    parser.add_option("-l", "--traffic_load", dest="traffic_load",
                      help="Value for the traffic_load parameter", default="0.3")
    parser.add_option("-c", "--congestion_control", dest="congestion_control",
                      help="congestion_control parameter value", default="mprpdma")

    options,args = parser.parse_args()
    file_path = "../simulation/mix/fct_spine_leaf_{}_{}_0.1_{}.txt".format(options.traffic_mode, options.traffic_load, options.congestion_control)
    # file_path = "../simulation/mix/fct_spine_leaf_{}_{}.txt".format(options.traffic_mode, options.congestion_control)
    results = process_file(file_path)
    print("平均FCT: {:.2f} ms".format(float(results[0]) / 1e6))
    print("大流平均FCT: {:.2f} ms".format(float(results[1]) / 1e6))
    print("小流平均FCT: {:.2f} us".format(float(results[2]) / 1e3))
    print("第99%大的FCT: {:.2f} ms".format(float(results[3]) / 1e6))
    print("第95%大的FCT: {:.2f} ms".format(float(results[4]) / 1e6))
    print("平均吞吐量: {:.2f} Gbps".format(float(results[5])))

