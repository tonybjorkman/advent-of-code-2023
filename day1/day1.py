import os
import copy

class WordCandidate:

    def __init__(self,text,value):
        self.index = 0 
        self.text = text
        self.value = value
        self.length = len(text)

    def is_match(self):
        return self.index == self.length

    def match(self,char):
        result = self.text[self.index] == char
        if result:
            self.index+=1
        return result

class TokenSearch:

    def __init__(self):
        number_map = {
            "zero":0,
            "one":1,
            "two":2,
            "three":3,
            "four":4,
            "five":5,
            "six":6,
            "seven":7,
            "eight":8,
            "nine":9}
        self.reversed_candidates = list([WordCandidate("".join(reversed(k)),v) for k,v in number_map.items()])
        self.forward_candidates = list([WordCandidate(k,v) for k,v in number_map.items()])
        self.candidates = self.forward_candidates
        self.clear()

    def clear(self):
        self.current_candidates = []

    def get_new_candidates(self,char):
        copy_list = copy.deepcopy(self.candidates)
        new = list([c for c in copy_list if c.match(char)]) 
        return new      

    def prune_existing_candidates(self,char): 
        self.current_candidates = list([c for c in self.current_candidates if c.match(char)])

    def next_char(self,char):
        #if we reach a non-letter, stop matching.
        if char.isalpha():
            self.prune_existing_candidates(char)
            for c in self.current_candidates:
                if c.is_match():
                    return c
            #assuming that no candidate is 1 in length, need only check existing
            self.current_candidates += self.get_new_candidates(char)
        else:
            self.current_candidates = []
        return None
    
    def search(self,word,reverse=False):
        if reverse:
            word="".join(reversed(word))
            self.candidates = self.reversed_candidates
        else:
            self.candidates = self.forward_candidates

        index=0
        self.clear()
        print(f'Searching in {word}')
        for char in word:
            if char.isdigit():
                print(f'Found digit:{char} at inx:{index}')
                return int(char)
            word_node = t.next_char(char)
            if word_node is not None:
                print(f'Found a word:{word_node.text}:{word_node.value} at inx:{index}')
                return int(word_node.value)
            index+=1

def find_digit_occurance(text,first=True):
    length=len(text)
    for i in range(length): 
        if first and text[i].isdigit():
            return int(text[i])
        elif not first and text[length-1-i].isdigit():
            return int(text[length-1-i])
    raise Exception('No digit in text')

def process_file(file):
    calibration_values = []
    with open(file) as f:
        for text_row in [repr(line) for line in f.readlines()]:
            print(f'Processing {text_row} into ',end='')
            first = find_digit_occurance(text_row,True)
            last = find_digit_occurance(text_row,False)
            print(f'{first}{last}')
            calibration_values.append(first*10+last)
        
        total_sum = 0
        for num in calibration_values:
            total_sum += num
        
        return total_sum


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #part One
    total_digits = process_file('input') 
    #part Two
    t = TokenSearch()
    #debug
    words = ["one3rrbseven3sevenpnnrnrz6\n"]
    total = 0
    with open('input') as f:
        for line in f.readlines():
        #for line in words:
            word = repr(line)
            print('--Start--')
            first_digit = t.search(word,False)
            print("Reverse Search")
            second_digit = t.search(word,True)
            value = first_digit*10+second_digit
            total += value
            print(f'{word}={value}')
            print('--End--')
        print(f'Total value with words:{total}, without words:{total_digits}')


