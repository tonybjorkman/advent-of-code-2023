import re
import os
import cmath
import math

os.chdir(os.path.abspath(os.path.dirname(__file__)))
races=[]
with open('input') as f:
    times = map(int,re.findall(r'\d+',next(f)))
    distance = map(int,re.findall(r'\d+',next(f)))
    races = list(zip(times,distance))

def distance_from_time(distance,max_time):
    a = -1
    b = max_time
    c = -distance

    # calculate the discriminant
    d = (b**2) - (4*a*c)

    # find two solutions
    sol1 = (-b-cmath.sqrt(d))/(2*a)
    sol2 = (-b+cmath.sqrt(d))/(2*a)

    print('The solution are {0} and {1}'.format(sol1,sol2))
    return sol1,sol2
sum=1
for t,d in races:
    result = distance_from_time(d,t) 
    sum*=(math.floor(result[0].real)-math.ceil(result[1].real)+1)

print(f'final: {sum}')