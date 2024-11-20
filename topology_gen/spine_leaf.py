
output = "spine_leaf.txt"
ofile = open(output, "w")

optical_spine_num = 4
electric_spine_num = optical_spine_num
spine_num = optical_spine_num + electric_spine_num
leaf_num = spine_num * 2
per_leaf_host_num = spine_num * 2
host_num = leaf_num * per_leaf_host_num

node_num = spine_num + leaf_num + host_num
electric_switch_num = electric_spine_num + leaf_num
optical_switch_num = optical_spine_num
link_num = host_num + spine_num * leaf_num

ofile.write("%d %d %d %d\n"%(node_num, electric_switch_num, optical_switch_num, link_num))

for i in range(optical_switch_num):
    ofile.write("%d "%(host_num + i))
ofile.write("\n")

for i in range(electric_switch_num):
    ofile.write("%d "%(host_num + optical_switch_num + i))
ofile.write("\n")

# connect optical spine and leaf
for os in range(optical_spine_num):
    for l in range(leaf_num):
        src = host_num + os
        dst = host_num + spine_num + l
        ofile.write("%d %d 100Gbps 1us 0 2\n"%(src, dst))

# connect eletric spine and leaf
for es in range(electric_spine_num):
    for l in range(leaf_num):
        src = host_num + optical_spine_num + es
        dst = host_num + spine_num + l
        ofile.write("%d %d 40Gbps 1us 0 1\n"%(src, dst))

# connect host and leaf
for l in range(leaf_num):
    for h in range(per_leaf_host_num):
        src = host_num + spine_num + l
        dst = l * per_leaf_host_num + h
        ofile.write("%d %d 10Gbps 1us 0 1\n"%(src, dst))

ofile.close()

