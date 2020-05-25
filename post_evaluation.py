import pprint
import re
from sys import argv

import key_words


'''Second part of the project. The saved review is evaluated in order to decide
if I should bother with part 3 of the project.'''

script, book_data = argv
positive_words_dict = {}
negative_words_dict = {}

reccomend_phrase = ''

with open(book_data, 'r') as file:
    data = file.read()
    data = re.sub('[?!]', '.', data)
    data_replaced = data.replace('\n', '').strip()
    lines = data_replaced.split('. ')

    for line in lines:
        if not reccomend_phrase and 'polecam' in line:
            reccomend_phrase = line
            continue

        line_split = line.split()

        for word in line_split:
            if len(word) > 2:
                word_lower = word.lower()
                if word_lower in key_words.positive_words:
                    if word_lower not in positive_words_dict:
                        positive_words_dict[word_lower] = 0
                    positive_words_dict[word_lower] += 1
                elif word_lower in key_words.negative_words:
                    if word_lower not in negative_words_dict:
                        negative_words_dict[word_lower] = 0
                    negative_words_dict[word_lower] += 1


last_line = lines[len(lines)-1]
good_book_ratio = f'{len(positive_words_dict)} : {len(negative_words_dict)}'

print(f'Recommending words to bad words ratio - {good_book_ratio}')
print(f'Recommend phrase - "{reccomend_phrase}"')
print('Last line: ', last_line)
