import nltk, re

grammar_filename = 'ramen_grammar.fcfg'
parser = nltk.parse.load_parser(grammar_filename)

# for converting spelled numbers to arabic numerals
num_conversion_dict = {
    'zero' : 0,
    'one' : 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    }

phrases_to_unify = ['with no', 'let me', 'as well as', 'in addition to'

                    'diet coke', 'diet cola', 'coka cola', 'minute maid', 'minute made', 'minute maid lemonade', 'sencha tea', 'jasmine tea', 'bancha tea'

                    'spring roll', 'egg roll', 'squid ball', 'chili oil', 'soy sauce', 'gyoza sauce', 'sriracha sauce', 'fish cake']


def preprocess(sentence):
    s = sentence.lower()
    s = re.sub(r'[\.,;?!"]', '', s)
    s = re.sub(r'please', '', s)
    s = re.sub(r'with no', 'with_no', s)
    s = re.sub(r'let me', 'let_me', s)
    s = s.split()
    #convert worded numbers to numerals
    for word in s:
        if word in num_conversion_dict.keys():
            numeral = num_conversion_dict[word]
            replace_at_index = s.index(word)
            s[replace_at_index] = numeral
    return s

def parse_sentence(sentence):
    processed = preprocess(sentence)
    for tree in parser.parse(processed):
        print(tree)
