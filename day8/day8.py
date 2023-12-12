import re
class Node:
    def __init__(self) -> None:
        self.left = None
        self.right = None


with open('input') as f:
    directions = next(f).strip()
    network = {}
    for line in f:
        if line.strip() == '':
            continue
        else:
            nodes = re.findall(r'[A-Z]+',line)
            network[nodes[0]]=(nodes[1],nodes[2])
    current_node = 'AAA'
    finish=False
    counter=0
    while(not finish):
        for dir in directions:
            counter+=1
            current_node = network[current_node][dir=='R']
            if current_node == 'ZZZ':
                finish=True
                break
    print(counter) 

