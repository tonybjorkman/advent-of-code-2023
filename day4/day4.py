import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('input') as f:
    score = 0
    for line in f.readlines():
        values = line.split(":")[1].split("|")
        win_values = [int(x) for x in values[0].split()]
        my_values = [int(x) for x in values[1].split()]
        
        count = 0
        for value in my_values:
            if value in win_values:
                count+=1
        if count>0:
            score+=pow(2,count-1)
    print(f'score is {score}')
