import glob
import os

NUMBER_OF_NODES = "4_nodes"
BASE_PATH = "/home/hansika/gem5/gem5/scripts/"
CALCULATED_DIR_PATH = BASE_PATH + "calculated/"
RAW_DATA_DIR_PATH = BASE_PATH + "raw_dd/"
NUMPY_DATA_DIR_PATH = BASE_PATH + "numpy_data/"


def create_dir(path):
    if not os.path.exists(path):
       os.makedirs(path)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
   
def write_to_file(file, dirr, syntheticTrafficCount, niPacketCount, flitCount):
   with open(CALCULATED_DIR_PATH + NUMBER_OF_NODES + "/" + dirr + "/" +  file, 'w') as f:
        f.write("----synthetic traffic generation count---- \n")
        for key,value in syntheticTrafficCount.items():
            f.write("%s : %s\n" % (key, value))
        f.write("\n")     
        f.write("----packet count on network interface---- \n")
        for key,value in niPacketCount.items():
            f.write("%s : %s\n" % (key, value))
        f.write("\n")  
        f.write("----flit count on network link---- \n")
        for key,value in flitCount.items():
            f.write("%s : %s\n" % (key, value))

def convert_to_numpy(nlFlitIPD):
   print(nlFlitIPD)

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


def process_flit_flow(link, stream , ipd, flitCount, nlFlitIPD, no_of_nodes):
   link = remove_prefix(link, "system.ruby.network.ext_links")
   link = link.split(".")[0]
   if int(link) >= no_of_nodes:
      node = int(link) - no_of_nodes
   else:
      node = int(link)
   key = "link_" + link + "(" + str(node) + ")_" + stream
   if key in flitCount:
      nlFlitIPD[key].append(ipd)
      flitCount[key] += 1
   else:
      nlFlitIPD[key] = [ipd]
      flitCount[key] = 1  

def process_line(line, niPacketCount, syntheticTrafficCount, flitCount, nlFlitIPD, no_of_nodes):
  y = [x.strip() for x in line.split(':')]
  if y[1].startswith("system.cpu"):
     process_sythetic_traffic_count(y[3],y[5],syntheticTrafficCount)
  elif y[1].startswith("system.ruby.network.netifs"):
     process_ni_packet_count(y[3],y[5],niPacketCount, no_of_nodes)
  elif y[1].startswith("system.ruby.network.ext_links"):
     process_flit_flow(y[1],y[2],y[4],flitCount, nlFlitIPD, no_of_nodes)
      

def process_file(filename):
   niPacketCount = {}
   flitCount = {}
   syntheticTrafficCount = {}
   nlFlitIPD = {}
   with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
      fileN = os.path.basename(filename)
      file = fileN.split("_")
      no_of_nodes = int(file[0])
      node1 = int(file[1])
      node2 = int(file[2])
      print("processing file from " + str(node1) + " to " + str(node2) + " in " + str(no_of_nodes) + " node environment" )
      for line in f:
        process_line(line, niPacketCount, syntheticTrafficCount, flitCount, nlFlitIPD, no_of_nodes)
   write_to_file(fileN, str(node1) + "_" + str(node2), syntheticTrafficCount, niPacketCount, flitCount)
   convert_to_numpy(nlFlitIPD)


list_subfolders_with_paths = [f.path for f in os.scandir(RAW_DATA_DIR_PATH + NUMBER_OF_NODES + "/") if f.is_dir()]
print(RAW_DATA_DIR_PATH + NUMBER_OF_NODES + "/")
create_dir(CALCULATED_DIR_PATH + NUMBER_OF_NODES)

for sub_dir in list_subfolders_with_paths:
   create_dir(CALCULATED_DIR_PATH + NUMBER_OF_NODES + "/" + os.path.basename(sub_dir))
   for filename in glob.glob(sub_dir + "/[!stats]*.txt"): 
      process_file(filename)
   
