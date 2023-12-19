import numpy as np
from collections import defaultdict

def apply_offsets(col_offsets,row_offsets,position,expansion_factor):
    col_offsets[col_offsets < position[1]]
    new_col_inx = position[1]+len(col_offsets[col_offsets < position[1]])*(expansion_factor-1) #-1 because replaces one existing distance
    new_row_inx = position[0]+len(row_offsets[row_offsets < position[0]])*(expansion_factor-1)
    return new_row_inx,new_col_inx

def get_galaxy_positions(map,expansion_factor=2):
    galaxies={}
    all_false_columns = np.all(~map,axis=0)
    all_false_rows = np.all(~map,axis=1)
    col_indexes = np.nonzero(all_false_columns)[0]
    row_indexes = np.nonzero(all_false_rows)[0]
    galaxies_arr = np.nonzero(map)

    galaxies_tuples = zip(galaxies_arr[0],galaxies_arr[1])
    for num,galaxy in enumerate(galaxies_tuples):
        galaxies[num]=apply_offsets(col_indexes,row_indexes,galaxy,expansion_factor=expansion_factor)
    return galaxies

def calculate_distance_matrix(galaxies):
    distance_matrix = np.zeros((len(galaxies),len(galaxies)))
    for start in range(distance_matrix.shape[0]):
        for dest in range(distance_matrix.shape[0]):
            if start == dest or dest<start:
                continue
            y_dist=abs(galaxies[start][0]-galaxies[dest][0])
            x_dist=abs(galaxies[start][1]-galaxies[dest][1])

            distance_matrix[start,dest] = y_dist+x_dist
    return distance_matrix

def get_input_map(file):
    with open(file) as f:
        rows = []
        for line in f:
            line=line.strip()
            rows.append([a == '#' for a in line])
        map = np.array(rows)
    return map

map = get_input_map('input')
galaxies = get_galaxy_positions(map,expansion_factor=2)
exp_2_dist = calculate_distance_matrix(galaxies)

print(f'part1 total sum {np.sum(exp_2_dist)}')

galaxies = get_galaxy_positions(map,expansion_factor=1000000)
exp_mil_dist = calculate_distance_matrix(galaxies)
print(f'part2 million total sum {np.sum(exp_mil_dist)}')
