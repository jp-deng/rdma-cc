# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

# 文件路径
throughput1_file_path = 'rate_log1.txt'
throughput2_file_path = 'rate_log2.txt'
throughput3_file_path = 'rate_log3.txt'
throughput4_file_path = 'rate_log4.txt'

# 从 throughput.txt 文件中读取数据
times1 = []
throughputs1 = []
times2 = []
throughputs2 = []
times3 = []
throughputs3 = []
times4 = []
throughputs4 = []

with open(throughput1_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        time, throughput = line.split(': ')
        times1.append(int(time)/1000)
        throughputs1.append(float(throughput))   

with open(throughput2_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        time, throughput = line.split(': ')
        times2.append(int(time)/1000)
        throughputs2.append(float(throughput))

with open(throughput3_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        time, throughput = line.split(': ')
        times3.append(int(time)/1000)
        throughputs3.append(float(throughput))

with open(throughput4_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        time, throughput = line.split(': ')
        times4.append(int(time)/1000)
        throughputs4.append(float(throughput))                        

# 创建图表
plt.figure(figsize=(10, 6))
plt.rcParams['font.family'] = 'Times New Roman'
# 设置坐标轴字体大小和样式
plt.tick_params(axis='both', which='major', labelsize=30)  # 调整刻度字体大小
# 移除边距
plt.margins(x=0, y=0)
# 减少留白
plt.subplots_adjust(left=0.05, right=0.99)
plt.subplots_adjust(bottom=0.07, top=0.99)
# 避免科学计数法
# plt.ticklabel_format(style='plain')

# 绘制网络吞吐量曲线
plt.ylim(0, 11)
plt.plot(times1, throughputs1, color='r', linewidth=3, label='flow1')
plt.plot(times2, throughputs2, color='g', linewidth=3, label='flow2')
plt.plot(times3, throughputs3, color='b', linewidth=3, label='flow3')
plt.plot(times4, throughputs4, color='y', linewidth=3, label='flow4')

# # 显示图例
# plt.legend(fontsize=16, loc='upper right')

# 格式化x轴以更清晰地显示时间
# plt.xticks(rotation=45)

# 保存图表到文件
plt.savefig('convergence.png')
