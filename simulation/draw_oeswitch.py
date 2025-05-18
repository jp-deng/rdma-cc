# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

# 文件路径
hpcc_throughput_file_path = 'rate_log1.txt'
# dcqcn_throughput_file_path = 'rate_dcqcn.txt'
# timely_throughput_file_path = 'rate_timely.txt'
# newcc_throughput_file_path = 'rate_newcc.txt'
intervals_file_path = 'link_log.txt'

# 从 throughput.txt 文件中读取数据
hpcc_times = []
hpcc_throughputs = []
timely_times = []
timely_throughputs = []
dcqcn_times = []
dcqcn_throughputs = []
newcc_times = []
newcc_throughputs = []

start_index = 500
end_index = 3300

with open(hpcc_throughput_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        time, throughput = line.split(': ')
        if int(time) >= start_index and int(time) <= end_index:
            hpcc_times.append(int(time) - start_index)
            hpcc_throughputs.append(float(throughput))

# with open(timely_throughput_file_path, 'r', encoding='utf-8') as file:
#     for line in file:
#         time, throughput = line.split(': ')
#         if int(time) >= start_index and int(time) <= end_index:
#             timely_times.append(int(time)  - start_index)
#             timely_throughputs.append(float(throughput))

# with open(dcqcn_throughput_file_path, 'r', encoding='utf-8') as file:
#     for line in file:
#         time, throughput = line.split(': ')
#         if int(time) >= start_index and int(time) <= end_index:
#             dcqcn_times.append(int(time)  - start_index)
#             dcqcn_throughputs.append(float(throughput))

# with open(newcc_throughput_file_path, 'r', encoding='utf-8') as file:
#     for line in file:
#         time, throughput = line.split(': ')
#         if int(time) >= start_index and int(time) <= end_index:
#             newcc_times.append(int(time)  - start_index)
#             newcc_throughputs.append(float(throughput))   

# 从 intervals.txt 文件中读取数据
time_intervals = []

with open(intervals_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        start_time, end_time = line.split()
        if int(start_time) >= start_index and int(end_time) <= end_index:
            time_intervals.append(((int(start_time) - start_index) , (int(end_time) - start_index)))

# 创建图表
plt.figure(figsize=(10, 4))
plt.rcParams['font.family'] = 'Times New Roman'
# 设置坐标轴字体大小和样式
plt.tick_params(axis='both', which='major', labelsize=20)  # 调整刻度字体大小
# 移除边距
plt.margins(x=0, y=0)
# 减少留白
plt.subplots_adjust(left=0.05, right=0.98)
plt.subplots_adjust(bottom=0.1, top=0.95)
# 避免科学计数法
plt.ticklabel_format(style='plain')

# 绘制网络吞吐量曲线
plt.plot(hpcc_times, hpcc_throughputs, color='r', linewidth=3)
# plt.plot(timely_times, timely_throughputs, color='r', linewidth=3)
# plt.plot(dcqcn_times, dcqcn_throughputs, color='r', linewidth=3)
# plt.plot(newcc_times, newcc_throughputs, color='r', linewidth=3)

# # 绘制时间区间阴影
for start_time, end_time in time_intervals:
    plt.axvline(x=start_time, linestyle='--')
    plt.axvline(x=end_time, linestyle='--')
    plt.fill_betweenx([0, 11], start_time, end_time, color='b', alpha=0.1)

# # 显示图例
# plt.legend()

# 格式化x轴以更清晰地显示时间
# plt.xticks(rotation=45)

# 保存图表到文件
plt.savefig('convergence.png', dpi=600)
