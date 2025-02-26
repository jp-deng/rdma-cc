import matplotlib.pyplot as plt
import numpy as np

websearch_file = 'WebSearch.txt'
fbhdp_file = 'FbHdp.txt'
alistorge_file = 'AliStorage2019.txt'

# 创建图表
plt.figure(figsize=(10, 6))
plt.rcParams['font.family'] = 'Times New Roman'
# 设置坐标轴字体大小和样式
plt.tick_params(axis='both', which='major', labelsize=20)  # 调整刻度字体大小
# # 减少留白
# plt.subplots_adjust(left=0.05, right=0.99)
# plt.subplots_adjust(bottom=0.07, top=0.99)    
plt.xscale('log')

x, y = [], []
with open(websearch_file, 'r') as file:
    for line in file:
        # 去除行末的换行符并按空格分割
        parts = line.strip().split()
        if len(parts) == 2:
            x_val, y_val = float(parts[0]), float(parts[1])
            x.append(x_val)
            y.append(y_val)
plt.plot(x, y, marker='o', linestyle='-', color='r', label='WebSearch')

x, y = [], []
with open(fbhdp_file, 'r') as file:
    for line in file:
        # 去除行末的换行符并按空格分割
        parts = line.strip().split()
        if len(parts) == 2:
            x_val, y_val = float(parts[0]), float(parts[1])
            x.append(x_val)
            y.append(y_val)
plt.plot(x, y, marker='o', linestyle='-', color='g', label='FbHdp')

x, y = [], []
with open(alistorge_file, 'r') as file:
    for line in file:
        # 去除行末的换行符并按空格分割
        parts = line.strip().split()
        if len(parts) == 2:
            x_val, y_val = float(parts[0]), float(parts[1])
            x.append(x_val)
            y.append(y_val)
plt.plot(x, y, marker='o', linestyle='-', color='b', label='AliStorage2019')

plt.legend(fontsize=16, loc='upper left')


# 保存图表到文件
plt.savefig('traffic.png')
