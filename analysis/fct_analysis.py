def process_file(file_path):
    all_fct = []
    large_flow_fct = []
    small_flow_fct = []
    packets = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            data = line.strip().split(' ')
            packet_size = int(data[4])
            fct_value = float(data[6])

            all_fct.append(fct_value)
            packets.append(packet_size)

            if packet_size >= 10 * 1024 * 1024:  # 10M in bytes
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

    return average_fct, large_flow_average_fct, small_flow_average_fct, fct_99, fct_95

if __name__=="__main__":
	file_path = 'your_file_path.txt'  # 替换为实际的文件路径
    results = process_file(file_path)
    print("平均FCT:", results[0])
    print("大流平均FCT:", results[1])
    print("小流平均FCT:", results[2])
    print("第99%大的FCT:", results[3])
    print("第95%大的FCT:", results[4])
