import numpy as np
from collections import defaultdict
galaxies=defaultdict(list)

with open('testinput') as f:
    row = 0
    col = 0
    galaxy_number = 1
    rows = []
    for line in f:
        line=line.strip()
        rows.append(list(line))
        if not '#' in line:
            rows.append(list('.'*(len(line))))
    # list of lines
    map = np.array(rows) 
    a=1
    


    '''if character == '#':
        galaxies[(row,col)]=galaxy_number
        galaxy_number+=1
       '''         


