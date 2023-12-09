from collections import defaultdict
import os
from itertools import chain
import logging
import tqdm
import sys

# Set the logging level to DEBUG when you want to enable debug debug_prints
logging.basicConfig(level=logging.INFO)

def debug_print(message,end='\n'):
    logging.debug(message,end=end)

class Range:
    '''
    Used instead of the inbuilt 'range' since more operations are needed.
    '''
    def __init__(self,start,stop) -> None:
        self.start = start 
        self.stop = stop 

    def add(self,num):
        self.start+=num
        self.stop+=num

    def find_intersection_and_remainder(self,rule):
        '''
        range=[1,2]
        rule=[2,3]
        range element 2 get intersected
        '''
    # Convert range objects to tuples
        rule_start, rule_end = rule.start, rule.stop
        self.start, self.stop = self.start, self.stop

        # Check for overlapping conditions
        if rule_end < self.start or self.stop < rule_start:
            # Ranges do not overlap
            return None, Range(self.start,self.stop)

        # Calculate the intersection
        intersection_start = max(rule_start, self.start)
        intersection_end = min(rule_end, self.stop)
        intersection = Range(intersection_start, intersection_end)

        # Calculate the non-intersecting ranges
        non_intersecting_ranges = []
        if self.start < intersection_start:
            non_intersecting_ranges.append(Range(self.start, intersection_start-1))
        if intersection_end < self.stop:
            non_intersecting_ranges.append(Range(intersection_end+1, self.stop))

        return intersection, non_intersecting_ranges

    def __repr__(self):
        return f'Range {self.start}-{self.stop} '

def test_range_intersect():
    r1 = Range(2,5)  #[2,3,4,5]
    rule = Range(3,4)  #[3,4]n

    i,r = r1.find_intersection_and_remainder(rule)
    print(i)
    print('remainders')
    print([x for x in r])

class MapRule(Range):
    '''
    stores a range-rule which maps one range to another.
    start and stop is for the input range, and anything between those
    will be offset by the offset
    '''
    def __init__(self, start, stop,offset) -> None:
        super().__init__(start, stop)
        self.offset = offset

    def __repr__(self):
        return f'RuleRange {self.start}-{self.stop}:{self.offset} '

class Layers:
    '''
    Holds all the layers, each layer has a set of mapping rules. 
    '''
    def __init__(self) -> None:
        self.layer_names = []
        self.layer_rules = [] #each inx is one layer of list 

    def add_layer(self,layer_rules):
        self.layer_rules.append(layer_rules)
    
    def get_rules(self,layer):
        return self.layer_rules[layer]

class Calculator:
    '''
    Performs propagation of the initial seeds through each mapping layer.
    '''
    def __init__(self,layers) -> None:
        self.layers = layers
        self.min_location = None
    
    def propagate(self,in_range:Range,layer):
        if layer == len(self.layers.layer_rules):
                if self.min_location is None or in_range.start < self.min_location:
                    self.min_location = in_range.start
                return
        has_intersected = False
        for rule in self.layers.get_rules(layer): 
            intersect, remains = in_range.find_intersection_and_remainder(rule)
            if intersect:
                has_intersected=True
                #print(f'layer:{layer} intersect at {intersect.start} -> {intersect.start+rule.offset}')
                intersect.add(rule.offset)
                #print(f'inrange:{in_range}')
                self.propagate(intersect,layer+1)
                for remain in remains:
                    self.propagate(remain,layer)
        # in case none of the rules have applied (thus no other propagate called)
        if not has_intersected: 
            self.propagate(in_range,layer+1)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
seed_ids = []
seed_ranges = []
layers = Layers()
with open('input') as f:
    seedline = f.readline()
    seed_ids = [int(x) for x in seedline.split(":")[1].split()]

    for x in range(1, 1+len(seed_ids), 2):
        seed_ranges.append(Range(seed_ids[x-1], seed_ids[x-1] + seed_ids[x]-1))

    layer_rules=[]
    for line in f.readlines():
        if ':' in line:
            layers.layer_names.append(line.split(':')[0])
            if len(layer_rules)>0:
                layers.add_layer(layer_rules)
                layer_rules=[]
        elif len(line) > 1:
            reg_entry = [int(x) for x in line.split()]
            layer_rules.append(MapRule(reg_entry[1],reg_entry[1]+reg_entry[2]-1,reg_entry[0]-reg_entry[1]))
    
    if len(layer_rules)>0:
        layers.add_layer(layer_rules)


calc = Calculator(layers)

for seed in seed_ids:
    calc.propagate(Range(seed,seed),0)
print(f'min location part1 {calc.min_location}')
calc.min_location=None

for seed in seed_ranges:
    debug_print(f'---- propagating {seed}')
    calc.propagate(seed,0)
print(f'min location part2 {calc.min_location}')