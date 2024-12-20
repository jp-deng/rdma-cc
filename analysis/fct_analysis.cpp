#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>

int main(int argc, char* argv[]) {
    // 检查是否有足够的命令行参数
    if (argc < 2) {
        std::cerr << "请提供替换0.7的值作为命令行参数。" << std::endl;
        return 1;
    }

    // 手动将命令行参数转换为双精度浮点数
    double replacementValue = 0.0;
    double decimal = 1.0;
    bool decimalPointSeen = false;
    const std::string argStr = argv[1];

    for (size_t i = 0; i < argStr.size(); ++i) {
        if (argStr[i] >= '0' && argStr[i] <= '9') {
            if (decimalPointSeen) {
                decimal /= 10.0;
                replacementValue += (argStr[i] - '0') * decimal;
            } else {
                replacementValue = replacementValue * 10.0 + (argStr[i] - '0');
            }
        } else if (argStr[i] == '.') {
            decimalPointSeen = true;
        }
    }

    // 构建文件路径字符串
    std::string filePath = "../simulation/mix/fct_spine_leaf_WebSearch_";
    std::ostringstream oss;
    oss << replacementValue << "_0.1_timely.txt";
    filePath += oss.str();

    // 打开文件并读取
    std::ifstream file(filePath.c_str());
    if (!file.is_open()) {
        std::cerr << "无法打开文件！" << std::endl;
        return 1;
    }

    std::vector<int> fct_values;

    long total_fct = 0;
    long large_flow_fct = 0;
    long small_flow_fct = 0;
    int total_count = 0;
    int large_flow_count = 0;
    int small_flow_count = 0;

    std::string line;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::string item;
        int index = 1;
        long packet_size = 0;
        long fct = 0;

        // 逐项读取每行中的数据
        for (int i = 1; i <= 8; ++i) {
            iss >> item;
            std::stringstream convert(item);
            if (i == 5) 
                convert >> packet_size;  // 使用 stringstream 转换第5项数据包大小
            if (i == 7)
                convert >> fct;           // 使用 stringstream 转换第7项fct
        }
        // 统计所有流量的fct
        total_fct += fct;
        total_count++;
        fct_values.push_back(fct);

        // 分类统计大流和小流的fct
        if (packet_size >= 10 * 1024 * 1024) {  // 大流条件：数据包大小 >= 10M
            large_flow_fct += fct;
            large_flow_count++;
        } else if (packet_size <= 100 * 1024) { // 小流条件：数据包大小 <= 100K
            small_flow_fct += fct;
            small_flow_count++;
        }
    }

    file.close();

    // 计算平均fct
    double avg_fct = total_count > 0 ? (double)total_fct / total_count : 0;
    double avg_large_flow_fct = large_flow_count > 0 ? (double)large_flow_fct / large_flow_count : 0;
    double avg_small_flow_fct = small_flow_count > 0 ? (double)small_flow_fct / small_flow_count : 0;
    
    // 排序fct列表
    std::sort(fct_values.begin(), fct_values.end());

    // 计算第99%和第95%的fct值
    double fct_99_percentile = 0;
    double fct_95_percentile = 0;
    if (!fct_values.empty()) {
        int idx_99 = static_cast<int>(fct_values.size() * 0.99) - 1;
        int idx_95 = static_cast<int>(fct_values.size() * 0.95) - 1;

        // 确保索引在范围内
        idx_99 = std::min(idx_99, static_cast<int>(fct_values.size() - 1));
        idx_95 = std::min(idx_95, static_cast<int>(fct_values.size() - 1));

        fct_99_percentile = fct_values[idx_99];
        fct_95_percentile = fct_values[idx_95];
    }

    // 输出结果
    std::cout << "所有流的平均FCT: " << avg_fct << std::endl;
    std::cout << "大流的平均FCT: " << avg_large_flow_fct << std::endl;
    std::cout << "小流的平均FCT: " << avg_small_flow_fct << std::endl;
    std::cout << "第99%大的FCT: " << fct_99_percentile << std::endl;
    std::cout << "第95%大的FCT: " << fct_95_percentile << std::endl;

    return 0;
}
