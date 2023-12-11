from collections import Counter
class Hand:
    def __init__(self, cards) -> None:
        self.original = cards.copy()
        self.cards = Counter(cards)
        self.num_jokers = self.cards.pop(11,0)

    def __eq__(self, __o: object) -> bool:
        pass

    def __repr__(self) -> str:
        return str(self.cards)

    def get_most_common(self,inx,count_jokers=False):
        result=0
        try:
            result = self.cards.most_common(inx+1)[inx][1]
        except Exception:
            result = 0
        if count_jokers:
            result+=self.num_jokers
        return result

    def __lt__(self, other) -> bool:
        if self.get_most_common(0,count_jokers=True) == other.get_most_common(0,count_jokers=True):
            if self.get_most_common(1)== other.get_most_common(1):
                for s_c, o_c in zip(self.original,other.original):
                    if s_c == o_c:
                        continue
                    else:
                        return (s_c < o_c or s_c == 11) and ( o_c != 11)
                return False 
            return self.get_most_common(1) < other.get_most_common(1)
        return self.get_most_common(0,count_jokers=True) < other.get_most_common(0,count_jokers=True)

class Rank:
    def __init__(self) -> None:
        pass

def translate_cards_to_digit(cards):
    card_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    translation = []
    for card in cards:
        if card in card_dict:
            translation.append(card_dict[card])
        else:
            translation.append(int(card))
    return translation

hands = []
with open('input') as f:
    for inx, line in enumerate(f):
        hands.append((Hand(translate_cards_to_digit(line.split()[0])),int(line.split()[1])))
hands.sort()

print('---')
high = '99999'
low = 'JJJJJ'
low_hand = Hand(translate_cards_to_digit(low))
high_hand = Hand(translate_cards_to_digit(high))
print(low_hand)
print(high_hand)
print(low_hand.__lt__(high_hand))

total=0
for rank,(hand,bid) in enumerate(hands):
    print(f'{rank+1} hand {hand} - {hand.original} bid {bid} total={bid*(rank+1)}')
    total+=(rank+1)*bid
print(f'total={total}')