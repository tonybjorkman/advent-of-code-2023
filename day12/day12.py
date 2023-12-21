import re
import numpy as np

def read_data(file):
    '''
    returns list of tuples
    (row,answer)
    '''
    data = []
    with open(file) as f:
        for line in f:
            data.append((line.split()[0],line.split()[1]))
    return data

def decimal_to_binary_array(decimal_number, min_len):
    binary_string = bin(decimal_number)[2:]  # Convert to binary and remove the '0b' prefix
    binary_array = [bit=='1' for bit in binary_string]
    while len(binary_array) < min_len:
        binary_array.insert(0,False)
    return binary_array

def get_interpret(row):
    '''
    returns the groups of # of a row in format
    [firstgroup-len,secondgroup-len, ...]
    '''
    spring_counter=0
    out_list=[]
    for num in row:
        if num:
            spring_counter+=1
        if not num and spring_counter>0:
            out_list.append(spring_counter)
            spring_counter=0
    if spring_counter>0:
        out_list.append(spring_counter)
    return out_list

def generate_and_evaluate_candidates(row_str,answer):
    '''
    generates all candidates and compares against answer and returns
    number of valid candidates.
    '''
    row = np.array([i=='#' for i in row_str])
    #number of groups
    inxes = [inx for inx,char in enumerate(row_str) if char == '?']
    binary_max = 2**len(inxes)
    count=0
    for i in range(binary_max):
        binary_candidate = decimal_to_binary_array(i,len(inxes))
        for num,(inx, binary) in enumerate(zip(inxes,binary_candidate)):
            row[inx]=binary
        result=get_interpret(row)
        if result == answer:
            print(['#' if x else '.' for x in row], end=' ')
            print('is match')
            count+=1
    return count

data = read_data('input')

counts = []
for row, answer in data:
    print(f'{row}:{answer}')
    count = generate_and_evaluate_candidates(row, list(map(lambda x: int(x) ,answer.split(','))))
    counts.append(count)
    print(f'{row} has {count} solutions')
    print(f'--------------------')
print(f' total num variation is: {sum(counts)}')
a=1
#number of variations per group
