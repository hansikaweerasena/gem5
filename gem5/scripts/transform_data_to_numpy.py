import glob
import os
import numpy as np
from random import randint
import argparse, sys


NUMBER_OF_NODES = "64_nodes_111"
BASE_PATH = "/home/hansika/gem5/gem5/scripts/"
CALCULATED_DIR_PATH = BASE_PATH + "calculated_test/"
RAW_DATA_DIR_PATH = BASE_PATH + "dummy_raw_data/"
NUMPY_DATA_DIR_PATH = BASE_PATH + "numpy_data_test/"

NUM_ITERATIONS_PER_FILE = 100
MIN_MAX_LENGTH = 450
calculate_reduced = True


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def write_to_file(file, dirr, syntheticTrafficCount, niPacketCount, flitCount):
    with open(CALCULATED_DIR_PATH + NUMBER_OF_NODES + "/" + dirr + "/" + file, 'w') as f:
        f.write("----synthetic traffic generation count---- \n")
        for key, value in syntheticTrafficCount.items():
            f.write("%s : %s\n" % (key, value))
        f.write("\n")
        f.write("----packet count on network interface---- \n")
        for key, value in niPacketCount.items():
            f.write("%s : %s\n" % (key, value))
        f.write("\n")
        f.write("----flit count on network link---- \n")
        for key, value in flitCount.items():
            f.write("%s : %s\n" % (key, value))


def isCorrelated(node1, node2, up_key, down_key, no_of_nodes):
    if node1 == up_key and node2 == down_key - no_of_nodes:
        x = 1
    elif node2 == up_key and node1 == down_key - no_of_nodes:
        x = 1
    else:
        x = 0
    return x


def convert_to_numpy(up_flit_ipd, down_flit_ipd, node1, node2, no_of_nodes, numpy_for_dir, correlation_dir):
    for up_key, up_value in up_flit_ipd.items():
        for down_key, down_value in down_flit_ipd.items():
            if up_key != down_key - no_of_nodes:
                correlation = isCorrelated(node1, node2, up_key, down_key, no_of_nodes)
                up_flow = np.array(up_value)
                down_flow = np.array(down_value)
                up_flow.resize(MIN_MAX_LENGTH, refcheck=False)
                down_flow.resize(MIN_MAX_LENGTH, refcheck=False)
                flow_pair = [up_flow, down_flow]
                numpy_for_dir.append(np.array(flow_pair))
                correlation_dir.append(correlation)

def generate_random(range_start, range_end, exclude_list):
    rand_node = randint(range_start,range_end)
    while(rand_node in exclude_list):
        rand_node = randint(range_start,range_end)
    return rand_node

def convert_to_numpy_reduced(up_flit_ipd, down_flit_ipd, node1, node2, no_of_nodes, numpy_for_dir, correlation_dir):
    cur_node_list = [node1,node2]
    node3 = generate_random(0, no_of_nodes - 1, cur_node_list) 
    cur_node_list.append(node3)
    node4 = generate_random(0, no_of_nodes - 1, cur_node_list)

    convert_to_numpy_local(up_flit_ipd.get(node1), down_flit_ipd.get(node2 + no_of_nodes), 1, numpy_for_dir, correlation_dir)
    convert_to_numpy_local(up_flit_ipd.get(node2), down_flit_ipd.get(node1 + no_of_nodes), 1, numpy_for_dir, correlation_dir)
    convert_to_numpy_local(up_flit_ipd.get(node1), down_flit_ipd.get(node3 + no_of_nodes), 0, numpy_for_dir, correlation_dir)
    convert_to_numpy_local(up_flit_ipd.get(node4), down_flit_ipd.get(node2 + no_of_nodes), 0, numpy_for_dir, correlation_dir)
    convert_to_numpy_local(up_flit_ipd.get(node3), down_flit_ipd.get(node4 + no_of_nodes), 0, numpy_for_dir, correlation_dir)
    convert_to_numpy_local(up_flit_ipd.get(node4), down_flit_ipd.get(node3 + no_of_nodes), 0, numpy_for_dir, correlation_dir)


def convert_to_numpy_local(up_value, down_value, correlation, numpy_for_dir, correlation_dir):
    up_flow = np.array(up_value)
    down_flow = np.array(down_value)
    up_flow.resize(MIN_MAX_LENGTH, refcheck=False)
    down_flow.resize(MIN_MAX_LENGTH, refcheck=False)
    flow_pair = [up_flow, down_flow]
    numpy_for_dir.append(np.array(flow_pair))
    correlation_dir.append(correlation)

def process_sythetic_traffic_count(frm, to, syntheticTrafficCount):
    key = frm + "->" + to
    if key in syntheticTrafficCount:
        syntheticTrafficCount[key] += 1
    else:
        syntheticTrafficCount[key] = 1


def process_ni_packet_count(frm, to, niPacketCount, no_of_nodes):
    if int(to) >= no_of_nodes:
        to_node = int(to) - no_of_nodes
    else:
        to_node = int(to)
    key = frm + "->" + to + "(" + str(to_node) + ")"
    if key in niPacketCount:
        niPacketCount[key] += 1
    else:
        niPacketCount[key] = 1


def process_flit_flow(link, stream, ipd, flitCount, up_flit_ipd, down_flit_ipd, no_of_nodes):
    link = remove_prefix(link, "system.ruby.network.ext_links")
    link = link.split(".")[0]
    key = "link_" + link + "_" + stream
    ipd = int(ipd)
    link = int(link)
    if stream == "Upstream":
        if key in flitCount:
            up_flit_ipd[link].append(ipd)
            flitCount[key] += 1
        else:
            up_flit_ipd[link] = [ipd]
            flitCount[key] = 1
    else:
        if key in flitCount:
            down_flit_ipd[link].append(ipd)
            flitCount[key] += 1
        else:
            down_flit_ipd[link] = [ipd]
            flitCount[key] = 1


def process_line(line, niPacketCount, syntheticTrafficCount, flitCount, down_flit_ipd, up_flit_ipd, no_of_nodes):
    y = [x.strip() for x in line.split(':')]
    if y[1].startswith("system.cpu"):
        process_sythetic_traffic_count(y[3], y[5], syntheticTrafficCount)
    elif y[1].startswith("system.ruby.network.netifs"):
        process_ni_packet_count(y[3], y[5], niPacketCount, no_of_nodes)
    elif y[1].startswith("system.ruby.network.ext_links"):
        process_flit_flow(y[1], y[2], y[4], flitCount, up_flit_ipd, down_flit_ipd, no_of_nodes)


def process_file(filename, numpy_for_dir, correlation_dir):
    niPacketCount = {}
    flitCount = {}
    syntheticTrafficCount = {}
    down_flit_ipd = {}
    up_flit_ipd = {}
    with open(os.path.join(os.getcwd(), filename), 'r') as f:  # open in readonly mode
        fileN = os.path.basename(filename)
        file = fileN.split("_")
        no_of_nodes = int(file[0])
        node1 = int(file[1])
        node2 = int(file[2])
        print("processing file from " + str(node1) + " to " + str(node2) + " in " + str(
            no_of_nodes) + " node environment")
        for line in f:
            process_line(line, niPacketCount, syntheticTrafficCount, flitCount, down_flit_ipd, up_flit_ipd, no_of_nodes)
    write_to_file(fileN, str(node1) + "_" + str(node2), syntheticTrafficCount, niPacketCount, flitCount)
    if calculate_reduced:
        convert_to_numpy_reduced(up_flit_ipd, down_flit_ipd, node1, node2, no_of_nodes, numpy_for_dir, correlation_dir)
    else:
        convert_to_numpy(up_flit_ipd, down_flit_ipd, node1, node2, no_of_nodes, numpy_for_dir, correlation_dir)


def save_numpy_array(numpy_for_dir, correlation_dir, index):
    np.save(os.path.join(NUMPY_DATA_DIR_PATH + NUMBER_OF_NODES + "/X", index), np.array(numpy_for_dir))
    np.save(os.path.join(NUMPY_DATA_DIR_PATH + NUMBER_OF_NODES + "/Y", index), np.array(correlation_dir))


parser=argparse.ArgumentParser()

parser.add_argument('--no-of-nodes', help='Number of nodes eg: 64_nodes_100_c')
parser.add_argument('--base-path', help='base path of the data')
parser.add_argument('--cal-dir-path', help='calculated dir path')
parser.add_argument('--rawd-dir-path', help='raw data dir path')
parser.add_argument('--numpy-dir-path', help='numpy dir path')

args=parser.parse_args()

if args.no_of_nodes != None:
    NUMBER_OF_NODES = args.no_of_nodes
if args.base_path != None:
    BASE_PATH = args.base_path
if args.cal_dir_path != None:
    CALCULATED_DIR_PATH = BASE_PATH + args.cal_dir_path
if args.rawd_dir_path != None:
    RAW_DATA_DIR_PATH = BASE_PATH + args.rawd_dir_path
if args.numpy_dir_path != None:
    NUMPY_DATA_DIR_PATH = BASE_PATH + args.numpy_dir_path


if calculate_reduced:
    NUMPY_DATA_DIR_PATH = BASE_PATH + "numpy_data_reduced/"

list_subdir_with_paths = [f.path for f in os.scandir(RAW_DATA_DIR_PATH + NUMBER_OF_NODES + "/") if f.is_dir()]
print(RAW_DATA_DIR_PATH + NUMBER_OF_NODES + "/")
create_dir(CALCULATED_DIR_PATH + NUMBER_OF_NODES)
create_dir(NUMPY_DATA_DIR_PATH + NUMBER_OF_NODES +"/X")
create_dir(NUMPY_DATA_DIR_PATH + NUMBER_OF_NODES +"/Y")

numpy_for_dir = []
correlation_dir = []
i = 1
j = 0
for sub_dir in list_subdir_with_paths:
    create_dir(CALCULATED_DIR_PATH + NUMBER_OF_NODES + "/" + os.path.basename(sub_dir))
    for filename in glob.glob(sub_dir + "/[!stats]*.txt"):
        process_file(filename, numpy_for_dir, correlation_dir)
        i += 1
        if i == NUM_ITERATIONS_PER_FILE:
            save_numpy_array(numpy_for_dir, correlation_dir, str(j))
            j += 1
            i = 1
            numpy_for_dir = []
            correlation_dir = []
if len(numpy_for_dir) > 0:
    save_numpy_array(numpy_for_dir, correlation_dir, str(j))
