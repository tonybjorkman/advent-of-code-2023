import re
from math import gcd
from collections import defaultdict

network={}
directions=[]
with open('input') as f:
    directions = next(f).strip()
    for line in f:
        if line.strip() == '':
            continue
        else:
            nodes = re.findall(r'[A-Z0-9]+',line)
            network[nodes[0]]=(nodes[1],nodes[2])

# create the complete direction cycle
directions = directions*(len(directions))

def node_travel(node_start,start_index=0):
    current_node = node_start
    counter=start_index
    for dir_inx in range(start_index,len(directions)):
        dir = directions[dir_inx]
        current_node = network[current_node][dir=='R']
        if current_node[2] == 'Z':
            return current_node, counter
        counter+=1
    return None

starting_node_hit_map = defaultdict(list)
for start_node_key in [node_key for node_key in network if node_key[2] == 'A']:
    direction_index=0
    current_node=start_node_key
    count=0
    while(True):
        result = node_travel(current_node,direction_index) 
        if result is None:
            break
        current_node , direction_index = result
        starting_node_hit_map[start_node_key].append(direction_index+1)#use one-index.
        # to continue node_travel with next direction, add 1 else it uses same twice.
        direction_index+=1

def least_common_denom(a):
    lcm = 1
    for i in a:
        lcm = lcm*i//gcd(lcm, i)
    return lcm
# get where the travel first hits a Z for each startnode
mins = [min(value) for key,value in starting_node_hit_map.items()]
travel =node_travel('AAA',0)[1]+1
print(f'part1 travel from A to Z:{travel}')
print(f'part2 number steps until all on Z: {least_common_denom(mins)}')

# For each Node ending with an A.
# Get the interval of which each such node will reach a node ending with Z

# so Each endA node will get associated with a list of numbers which will repeat in 
# sequence. 

# Then find the least common denominator for all the nodes.
# if one node hits Z and #10 and #15 and second node hits each #3 and third node
# hits on #5 
# least common denominator is 15 (15/3)=natural number 15/5=natural number

# How about the wrap-around effect of the directions?
# RLRLRLLL
# A startnode will not repeat the same pattern as when it first traveled
# but it will not have more patterns than the number of direction inputs which is
# 263. After that it will once again repeat. So I only need to do a 'full travel' for each
# node 263 times to get the complete pattern
