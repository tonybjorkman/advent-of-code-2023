from collections import Counter
# översätt bokstäverna till siffror
from functools import cmp_to_key

filename = "input"
lines=[]
with open(filename, 'r') as file:
    lines = file.readlines()


# Define a mapping function
def transform_element(element):
    mapping = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}

    # Apply the mapping function
    return int(mapping.get(element, element))  # Use the element itself if not found in the mapping

def hand_to_list_of_int(hand):

    hand_list = list(hand)
    transformed_list = [transform_element(item) for item in hand_list]

    return transformed_list

def get_score(hand):

    hand_list = hand_to_list_of_int(hand)

    result = Counter(hand_list)

    counts_most_common = result.most_common(1)[0][1]
    value_most_common = result.most_common(1)[0][0]

    # print("counts_most_common", counts_most_common)
    # print("value_most_common", value_most_common)

    # hand score
    is_five_of_a_kind = len(set(hand_list)) == 1

    if is_five_of_a_kind:
        # print("Five of a kind")
        # score = 1000 + hand_list[0]
        return 1000

    counts_second_most_common = result.most_common(2)[1][1]
    # print("counts_second_most_common", counts_most_common)

    is_four_of_a_kind = counts_most_common == 4

    if is_four_of_a_kind:
        # print("Four of a kind")
        # score = 900 + value_most_common
        return 900

    is_full_house = len(set(hand_list)) == 2 and not is_four_of_a_kind
    if is_full_house:
        # print("Full house")
        return 800

    is_three_of_a_kind = len(set(hand_list)) == 3 and counts_most_common == 3
    if is_three_of_a_kind:
        # print("Three of a kind")
        return 700

    is_two_pair = len(set(hand_list)) == 3 and not is_three_of_a_kind
    if is_two_pair:
        # print("Two pair")
        return 600

    is_one_pair = len(set(hand_list)) == 4
    if is_one_pair:
        # print("One pair")
        return 500

    is_high_card = len(set(hand_list)) == 5
    if is_high_card:
        # print("High card")
        return 400

    return 0

def get_second_score(hand):

    score = 0
    hand_list = hand_to_list_of_int(hand)
    for i, number in enumerate(hand_list):
        score += (10**(12-2*i)) * number

    return score

# Define a custom comparison function
def custom_compare(hand_x, hand_y):

    # Compare elements based on their custom order
    hand_x_score = get_score(hand_x)
    hand_y_score = get_score(hand_y)

    if hand_x_score == hand_y_score:
        hand_x_score = get_second_score(hand_x)
        hand_y_score = get_second_score(hand_y)

    return (hand_x_score > hand_y_score) - (hand_x_score < hand_y_score)


hand_str_list = []
dict_machine = {}

for id, line in enumerate(lines):
    hand_str = line.split()[0]
    bid = int(line.split()[1])
    # print(hand_str, bid)
    hand_str_list.append(hand_str)
    dict_machine[hand_str] = bid

# Sort the list based on the custom comparison function
sorted_hands = sorted(hand_str_list, key=cmp_to_key(custom_compare))
# print(sorted_hands)


# final stuff
sum = 0
for i, hand in enumerate(sorted_hands):

    rank = i + 1
    bid = dict_machine[hand]
    sum += bid * rank

print(sum)
print('')
# compare
class Type:
    '''
    Contains the rules which classify a type
    '''
    def __init__(self) -> None:
        pass

class Hand:
    def __init__(self, cards) -> None:
        card_dict = Counter(cards)
        self.cards = dict(sorted(card_dict.items(), key=lambda item: (-item[1], -item[0])))
        a=1

    def __eq__(self, __o: object) -> bool:
        pass

    def __repr__(self) -> str:
        return str(self.cards)

    def __lt__(self, other) -> bool:
        other_high_suite=None
        for s, o in zip(self.cards.items(), other.cards.items()):
            # same num occurrence(five of a kind etc)
            if s[1] == o[1]:
                # same 'value of card' (A,K etc)
                if s[0] == o[0]:
                    # go to next counter if any.
                    continue
                else:
                    #may still be a second pair. save first highest
                    if other_high_suite is None:
                        other_high_suite=s[0] < o[0]
                    continue
            else:
                return s[1] < o[1]
        # if it comes here, the hands are the same. maybe start with
        # check for equalness?
        # if equal, return as if greater
        if other_high_suite is None:
            other_high_suite=False
        return other_high_suite 

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
    translation.sort()
    return translation

hands = []
with open('input') as f:
    for inx, line in enumerate(f):
        hands.append((Hand(translate_cards_to_digit(line.split()[0])),int(line.split()[1])))
hands.sort()

print('---')
'''high = '99643'
low = 'AKQ98'
low_hand = Hand(translate_cards_to_digit(low))
high_hand = Hand(translate_cards_to_digit(high))

print(low_hand)
print(high_hand)
print(low_hand.__lt__(high_hand))
'''
total=0
for rank,(hand,bid) in enumerate(hands):
    print(f'{rank+1} hand {hand} bid {bid} total={bid*(rank+1)}')
    total+=(rank+1)*bid
print(f'total={total}')



