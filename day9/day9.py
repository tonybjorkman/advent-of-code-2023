import os
import re

os.chdir(os.path.abspath(os.path.dirname(__file__)))


def get_element_diff(input_list):
    new_list = []
    for i in range(len(input_list)-1):
        new_list.append(input_list[i+1] - input_list[i])
    return new_list


def get_extrapolated_scalar(input_list):
    ''' input the start list from which the diffs will be taken'''
    ''' the last diff-value for each input list is added to the last element in the input.'''
    if not sum([num != 0 for num in input_list]):
        return 0
    
    diff = get_element_diff(input_list)
    return get_extrapolated_scalar(diff)+input_list[-1]


with open('input') as f:
    totals = 0
    totals2 = 0
    for line in f:
        nums = [int(a) for a in line.strip().split()]
        answer = get_extrapolated_scalar(nums)
        answer2 = get_extrapolated_scalar(nums[::-1])
        print(f'scalar1: {answer}')
        print(f'scalar2: {answer2}')

        totals += answer
        totals2 += answer2
    print(f'sum part1 is {totals}')
    print(f'sum part2 is {totals2}')
