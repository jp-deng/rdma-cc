# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

# 文件路径
throughput_file_path = 'rate_log2.txt'
intervals_file_path = 'link_log.txt'

# 从 throughput.txt 文件中读取数据
times = []
throughputs = []

with open(throughput_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        time, throughput = line.split(': ')
        times.append(int(time))
        throughputs.append(float(throughput))

# 从 intervals.txt 文件中读取数据
time_intervals = []

with open(intervals_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        start_time, end_time = line.split()
        time_intervals.append((int(start_time), int(end_time)))

# 创建图表
plt.figure(figsize=(14, 8))

# 绘制网络吞吐量曲线
plt.plot(times, throughputs, label='Network Throughput')

# 绘制时间区间阴影
for start_time, end_time in time_intervals:
    plt.axvline(x=start_time, color='b', linestyle='--')
    plt.axvline(x=end_time, color='r', linestyle='--')
    plt.fill_betweenx([0, max(throughputs)], start_time, end_time, color='gray', alpha=0.3)

# 添加标题和标签
plt.title('Network Throughput with Time Intervals')
plt.xlabel('Time')
plt.ylabel('Throughput')

# 显示图例
plt.legend()

# 格式化x轴以更清晰地显示时间
plt.xticks(rotation=45)

# 保存图表到文件
plt.savefig('combined_plot.png')
