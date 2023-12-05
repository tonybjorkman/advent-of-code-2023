import numpy as np
import os
from enum import Enum

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Read the file as a 1D array of characters
with open('input', 'r') as file:
    content = file.read()
    file.seek(0)
    schematic_width = len(file.readline())-1
    char_array_1d = np.frombuffer(content.encode(), dtype=np.uint8)

# Reshape the 1D array into a 2D array
array_shape = (schematic_width, len(char_array_1d) // schematic_width)
char_array_2d = char_array_1d[:np.prod(array_shape)].reshape(array_shape)


class State(Enum):
    SEARCHING = 0
    ON_NUMBER = 1

def search_special(line,x_start,x_stop):
    ''' 
    Returns
    boolean - if symbol was found
    list of tuples - tuple contains coordinates of bordering *'s if any'''
    start_line = 0
    if line > 1:
        start_line = line-1
    x_start = abs(x_start-1)
    if x_stop < char_array_2d.shape[1]:
        x_stop = x_stop+1
    search_area = char_array_2d[start_line:line+2,x_start:x_stop]
    print(search_area)
    #check for element
    found_special = False
    star_coordinates = []
    for row_index, row in enumerate(search_area):
        for col_index, element in enumerate(row):
            if chr(element) != "." and not chr(element).isdigit() and chr(element) != '\n':
                print(f"Condition met:({chr(element)}:[{row_index}, {col_index}])")
                found_special = True
                if chr(element) == "*":
                    star_coordinates.append((start_line+row_index,col_index+x_start))
    return found_special, star_coordinates

current_number = ""
number_start_x = 0
number_stop_x = 0
state = State.SEARCHING
total_sum = 0
gear_dict = {}
for y in range(char_array_2d.shape[0]):
    for x in range(char_array_2d.shape[1]):
        #skip ahead until end of number if number has been found
        if y == char_array_2d.shape[0]-1:
            a=1
        if x > number_stop_x or x == 0:
            print(chr(char_array_2d[y,x]))
            if chr(char_array_2d[y,x]).isdigit():
                if state == State.SEARCHING:
                    number_start_x = x
                state = State.ON_NUMBER
                current_number+=chr(char_array_2d[y,x])
            elif not chr(char_array_2d[y,x]).isdigit() and state == State.ON_NUMBER:
                # last digit in number passed
                has_symbol, star_coordinates = search_special(y,number_start_x,x)
                if has_symbol:
                    print(f'add {current_number}')
                    total_sum+=int(current_number)
                    for coord in star_coordinates:
                        try:
                            gear_dict[coord].append(int(current_number))
                        except:
                            gear_dict[coord] = [int(current_number)]

                current_number = ""
                number_stop_x = x
                state = State.SEARCHING
    number_stop_x = 0
# calculate Part2 gear ratio sum.
gear_sum = 0
for k,v in gear_dict.items():
    if len(v) == 2:
        gear_sum+=v[0]*v[1]

print(f'symbol number total is:{total_sum} and gear total is:{gear_sum}')
