import numpy as np
from collections import defaultdict
galaxies={}

with open('testinput') as f:
    row = 0
    col = 0
    galaxy_number = 1
    rows = []
    for line in f:
        line=line.strip()
        rows.append([a == '#' for a in line])
        if not '#' in line:
            rows.append([False for a in range(len(line))])
    # list of lines
    map = np.array(rows)
    test = np.all(~map,axis=0)
    indexes = np.nonzero(test)[0]
    map = np.insert(map,indexes+1,False,axis=1)

    galaxies_arr = np.nonzero(map)
    galaxies_tuples = zip(galaxies_arr[0],galaxies_arr[1])
    for num,galaxy in enumerate(galaxies_tuples):
        galaxies[num]=galaxy
    
    distance_matrix = np.zeros((len(galaxies),len(galaxies)))

    for start in range(distance_matrix.shape[0]):
        for dest in range(distance_matrix.shape[0]):
            if start == dest or dest[1]<start[1]:
                continue
            y_dist=abs(galaxies[start][0]-galaxies[dest][0])
            x_dist=abs(galaxies[start][1]-galaxies[dest][1])

            distance_matrix[start,dest] = y_dist+x_dist
    print(f'total sum {np.sum(distance_matrix)}')


