import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def parse(text):
    game = text.split(':')[0].split(' ')[1]
    rounds = text.split(':')[1].split(';')
    max_drawn = {'game':int(game),'red':0,'blue':0,'green':0}

    for round in rounds:
        items = round.split(',')
        for item in items:
            pattern = re.compile(r'\s(\d+) (green|red|blue)')
            matches = pattern.findall(item)
            if int(matches[0][0]) > max_drawn[matches[0][1]]:
                max_drawn[matches[0][1]] = int(matches[0][0])
    
    return max_drawn


#Part One & Two
text = "Game 1: 20 green, 3 red, 2 blue; 9 red, 16 blue, 18 green; 6 blue, 19 red, 10 green; 12 red, 19 green, 11 blue"
max_red = 12
max_green = 13
max_blue = 14
sum_ID_possible_games = 0
total_power = 0
with open('input') as f:
    for line in f.readlines():
        result = parse(line)
        if result['green'] <= max_green and result['blue'] <= max_blue and result['red'] <= max_red:
            sum_ID_possible_games+=result['game']
        total_power += result['green']*result['blue']*result['red']
print(f'Possible games:{sum_ID_possible_games} Power of games:{total_power}') 

