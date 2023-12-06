import os
from itertools import chain
import logging
import tqdm

# Set the logging level to DEBUG when you want to enable debug debug_prints
logging.basicConfig(level=logging.INFO)

def debug_print(message,end='\n'):
    logging.debug(message,end=end)

# Example usage

class Register:
    def __init__(self, name) -> None:
        self.name = name
        self.ranges = []
        self.linked_register = None
        self.reverse_link_register = None

    def add_link(self, other):
        self.linked_register = other
        other.reverse_link_register = self

    def get_destination(self, source_id):
        debug_print(f'{self.name}:{source_id} -> ', end='')
        for dest, source, length in self.ranges:
            if source_id >= source and source_id < source+length:
                debug_print(dest+source_id-source)
                return dest+source_id-source
        # if not in a range, dest=source
        debug_print(source_id)
        return source_id

    def get_source(self, dest_id):
        debug_print(f'{self.name}:{dest_id} -> ', end='')
        for dest, source, length in self.ranges:
            if dest_id >= dest and dest_id < dest+length:
                debug_print(source+dest_id-dest)
                return source+dest_id-dest
        # if not in a range, source=dest
        debug_print(dest_id)
        return dest_id

    def add_range(self, dest_start, source_start, length):
        self.ranges.append((dest_start, source_start, length))

    def get_final_destination(self, source_id):
        if self.linked_register is None:
            return self.get_destination(source_id)

        return self.linked_register.get_final_destination(self.get_destination(source_id))

    def get_final_source(self, dest_id):
        if self.reverse_link_register is None:
            return self.get_source(dest_id)

        return self.reverse_link_register.get_final_source(self.get_source(dest_id))


os.chdir(os.path.dirname(os.path.abspath(__file__)))
registers = []
seed_ids = []
seed_ranges = []
with open('input') as f:
    seedline = f.readline()
    seed_ids = [int(x) for x in seedline.split(":")[1].split()]

    for x in range(1, 1+len(seed_ids), 2):
        seed_ranges.append(range(seed_ids[x-1], seed_ids[x-1] + seed_ids[x]))
    a = 1
    for line in f.readlines():
        if ':' in line:
            reg = Register(line[:-2])
            if len(registers) > 0:
                registers[-1].add_link(reg)
            registers.append(reg)
        elif len(line) > 1:
            reg_entry = [int(x) for x in line.split()]
            registers[-1].add_range(*reg_entry)

def trace_source(location):
    end_seed = registers[-1].get_final_source(location)
    print(location)
    if end_seed in chain(seed_ranges):
        print(f'Found seed at location {location}')
        exit()

locations = []
for seed in seed_ids:
    debug_print('----')
    locations.append(registers[0].get_final_destination(seed))
from joblib import Parallel, delayed
Parallel(n_jobs=-1)(delayed(trace_source)(location) for location in tqdm.tqdm(range(857589555), desc="Processing", unit="item"))

#print(f'min location: {min(locations)}')