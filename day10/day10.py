from array import array
from operator import index
import os
from tkinter import Y
from turtle import pos
import numpy as np
from PIL import Image

os.chdir(os.path.abspath(os.path.dirname(__file__)))

'''right = {'J':'up','-':'right','7':'down'}
left = {'F':'down','L':'up','-':'left'}
up = {'|':'up','7':'left','F':'right'}
down = {'L':'right','|':'down','J':'left'}
'''

def draw_map(y_3d):

    # Create a sample 2D NumPy array
    array_2d = y_3d[:,:,1]
    '''
    width, height = 512, 512
    gradient = np.zeros((height // 3, width // 3), dtype=np.uint8)

    for i in range(width // 3):
        for j in range(height // 3):
            gradient[j, i] = (i * 3 + j * 3) % 256

    # Step 2: Create a Pillow Image object from the NumPy array
    image_data = np.repeat(np.repeat(gradient, 3, axis=1), 3, axis=0)
    image = Image.fromarray(image_data.astype('uint8'), 'L')
    # Step 3: Display the image using the default viewer
    image.show('title')
    # Step 1: Create a 2D NumPy array
    # For demonstration purposes, you can create a simple array or load an existing image as a NumPy array.
    # In this example, let's create a gradient array.
    '''
    color_map = {'X':140,'1':70,'0':210,'':255}

    tiles = {'J':[[140,0,140],[0,0,140],[140,140,140]],
    'L':[[140,0,140],[140,0,0],[140,140,140]],
    '7':[[140,140,140],[0,0,140],[140,0,140]],
    'F':[[140,140,140],[140,0,0],[140,0,140]],
    '-':[[140,140,140],[0,0,0],[140,140,140]],
    '|':[[140,0,140],[140,0,140],[140,0,140]],
    'S':[[140,0,140],[0,0,0],[140,0,140]]}
    heighty, widthy =  array_2d.shape
    width, height = widthy*3, heighty*3
    gradient = np.zeros((height, width), dtype=np.uint8)

    for i in range(width):
        for j in range(height):
            gradient[i, j] = color_map[array_2d[i//3,j//3]]

    for i in range(heighty):
        for j in range(widthy):
            if array_2d[i,j] == 'X':
                gradient[i*3:i*3+3,j*3:j*3+3] = np.array(tiles[y_3d[i,j,0]])

    # Step 2: Create a Pillow Image object from the NumPy array
    image_data = np.repeat(np.repeat(gradient, 3, axis=1), 3, axis=0)
    image = Image.fromarray(image_data, mode='L')  # 'L' mode is for grayscale

    # Step 3: Display or save the image
    image.show('title')  # Display the image using the default viewer
    a=input()
    if a == 'exit':
        exit()




# in = 1 = mörk färg
right = {'J':{'go':'up','in':[],'out':['right','down']},
         '-':{'go':'right','in':['up'],'out':['down']},
         '7':{'go':'down','in':['up','right'],'out':[]}}
left = {'F':{'go':'down','in':[],'out':['left','up']},
        'L':{'go':'up','in':['left','down'],'out':[]},
        '-':{'go':'left','in':['down'],'out':['up']}}
up = {'|':{'go':'up','in':['left'],'out':['right']},
      '7':{'go':'left','in':[],'out':['right','up']},
      'F':{'go':'right','in':['left','up'],'out':[]}}
down = {'L':{'go':'right','in':[],'out':['left','down']},
        '|':{'go':'down','in':['right'],'out':['left']},
        'J':{'go':'left','in':['right','down'],'out':[]}}

directions = {'right':right,'left':left,'up':up,'down':down}
#    1     1       
#    >  >   >    
# 1 ^   0    V 1    
# 1 ^0  0  0 V 1    
#    <  <   <    
#      1  1       
# number denotes the index in dir_side_border value
dir_to_cartesian = {'right':(1,0),'left':(-1,0),'up':(0,-1),'down':(0,1)}

counter=0

def add_position(pos1,pos2):
    return [pos1[0]+pos2[0],pos1[1]+pos2[1]]

def traverse(map, position, direction):
    ''' follow the char at position when entering from direction'''
    ''' builds a mask, first run marks pipes with X '''
    ''' second run marks sides of pipe with 0 and 1 '''
    global counter
    counter+=1
    char = map[position[1],position[0],0]
    mask = map[position[1],position[0],1]
    if counter % 8 == 0 and mask == 'X':
        pass
        #draw_map(map)
    map[position[1],position[0],1]='X'
    if char == 'S':
        print(counter)
        return
    # find which ways this char can travel
    text_dir = directions[direction][char]['go']
    cartesian_dir = dir_to_cartesian[text_dir]
    if mask == 'X':
        #this is second run of traverse, time to mask sides:
        # tag tile unless tile is already tagged as something
        for rel_pos in [dir_to_cartesian[d] for d in directions[direction][char]['in']]:
            inner_position = add_position(position,rel_pos)
            try:
                if map[inner_position[1],inner_position[0],1] == '':
                    print(f'set 0 at {inner_position}')
                    map[inner_position[1],inner_position[0],1] = '0'
            except IndexError:
                print(f'index error for inner:{inner_position}')
        for rel_pos in [dir_to_cartesian[d] for d in directions[direction][char]['out']]:
            outer_position = add_position(position,rel_pos)
            try:
                if map[outer_position[1],outer_position[0],1] == '':
                    map[outer_position[1],outer_position[0],1] = '1'
            except IndexError:
                print(f'index error for outer:{outer_position}')


    #get next position and direction based on character encountered 
    print(f'entering {direction} to {position},{char} following it',end=' ')
    position[0]+=cartesian_dir[0]
    position[1]+=cartesian_dir[1]
    print(f'{text_dir} to {position}')
    
    return position, text_dir

# Read the file as a 1D array of characters
with open('input', 'r') as file:
    lines = file.readlines()
    char_matrix = [list(line.strip()) for line in lines]
# Reshape the 1D array into a 2D array
# You need to specify the shape based on the size of your data
# For example, if your file has 100 characters and you want a 10x10 array, use (10, 10)
# Make sure the size of the array matches the size of your data
    
test_map=np.array(char_matrix)
y_3d = test_map[:,:,np.newaxis]
y_3d = np.dstack((y_3d,np.full((140,140,1),'',dtype=str)))
print(y_3d[:,:,0])
position=[73,82]
text_dir = 'left'
result=1
while(True):
    result = traverse(y_3d,position,text_dir)
    if result is None:
        break
    position , text_dir = result

print('-- Setting masks of 0 and 1 --')
position=[73,82]
text_dir = 'left'
counter=0
while(True):
    result = traverse(y_3d,position,text_dir)
    if result is None:
        break
    position , text_dir = result

print(counter/2)
draw_map(y_3d)
# solution1:
# find the path tile next to S 
# move_next_neighbour(map,position)->new_position
# ' checks tiletype to see valid moves and moves'
# cuts a 3*3 and searches for matching.

# destroys the map as it passes

# follow path with 'navigation'+prev as | can mean both up and down.
# count number of steps
# walk path until reaching back to S again. 
