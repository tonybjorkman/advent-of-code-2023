import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
index_offset = -1
def get_cards(card_id):
    print(f'processing card:{card_id}',end='')
    if card_id > 202:
        return 0
    # return the cards of a single ticket, by index and by reading the value
    sum=1 #this card
    for card in [i+card_id for i in range(1,card_score_db[card_id+index_offset]+1) if i+card_id<=202]:
        sum+=get_cards(card)
        #print(f'-> Draws card:{card}')
    
    #print(f'No more cards to draw for {card_id}. Sum:{sum}')
    print(f'sum:{sum}')
    return sum


card_score_db = []
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
        card_score_db.append(count)
        if count>0:
            score+=pow(2,count-1)
    print(f'score is {score}')

sum=0
for card in range(1,len(card_score_db)+1):
    sum+=get_cards(card)
print(f'Solution for Part2:{sum}')
