import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Specify the file path
file_path = 'input'

# Read the file as a 1D array of characters
with open(file_path, 'r') as file:
    content = file.read()
    file.seek(0)
    schematic_width = len(file.readline())-1
    char_array_1d = np.frombuffer(content.encode(), dtype=np.uint8)

# Reshape the 1D array into a 2D array
# You need to specify the shape based on the size of your data
# For example, if your file has 100 characters and you want a 10x10 array, use (10, 10)
# Make sure the size of the array matches the size of your data
array_shape = (schematic_width, len(char_array_1d) // schematic_width)
char_array_2d = char_array_1d[:np.prod(array_shape)].reshape(array_shape)

# Print the resulting 2D array
print(char_array_2d)

# walk through each line in the array using indexes and check the border around each number,
# if symbol found, then add.

def search_special(line,x_start,x_stop):
    start_line = 0
    if line > 1:
        start_line = line-1
    x_start = abs(x_start-1)
    if x_stop < char_array_2d.shape[1]:
        x_stop = x_stop+1
    search_area = char_array_2d[start_line:line+2,x_start:x_stop]
    print(search_area)
    #check for element
    for row_index, row in enumerate(search_area):
        for col_index, element in enumerate(row):
            if chr(element) != "." and not chr(element).isdigit() and chr(element) != '\n':
                print(f"Condition met:({chr(element)}:[{row_index}, {col_index}])")
                return True
    return False

pointer_x = 0
pointer_y = 0
current_number = ""
number_start_x = 0
number_stop_x = 0
state = "searching"
total_sum = 0
for y in range(char_array_2d.shape[0]):
    for x in range(char_array_2d.shape[1]):
        #skip ahead until end of number if number has been found
        if y == char_array_2d.shape[0]-1:
            a=1
        if x > number_stop_x or x == 0:
            print(chr(char_array_2d[y,x]))
            if chr(char_array_2d[y,x]).isdigit():
                if state == "searching":
                    number_start_x = x
                state = "on number"
                current_number+=chr(char_array_2d[y,x])
            elif not chr(char_array_2d[y,x]).isdigit() and state == "on number":
                if search_special(y,number_start_x,x):
                    print(f'add {current_number}')
                    total_sum+=int(current_number)
                current_number = ""
                number_stop_x = x
                state = "searching"
    number_stop_x = 0

print(f'total is:{total_sum}')


        



