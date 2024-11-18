#!/bin/bash

cd topology_gen
if [ ! -f spine_leaf.txt ]; then
    python spine_leaf.py
fi
cd ..

cd traffic_gen
param_load=$1
param_time=0.1
param_cdf=WebSearch
traffic_file="${param_cdf}_${param_load}_${param_time}.txt"
if [ ! -f $traffic_file ]; then
    python traffic_gen.py -c ${param_cdf}_distribution.txt -l $param_load -t $param_time -o $traffic_file
fi
cd ..

cd simulation
python run.py --trace ${param_cdf}_${param_load}_${param_time} --topo spine_leaf
cd ..