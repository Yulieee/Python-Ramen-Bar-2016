import nltk, re

grammar_filename = 'ramen_grammar.fcfg'
parser = nltk.parse.load_parser(grammar_filename)

def preprocess(sentence):
    s = sentence.lower()
    s = re.sub(r'[\.,;?!"]', '', s)
    s = re.sub(r'please', '', s)
    s = re.sub(r'with no', 'with_no', s)
    s = re.sub(r'let me', 'let_me', s)
    s = s.split()
    return s

def parse_sentence(sentence):
    processed = preprocess(sentence)
    for tree in parser.parse(processed):
        print(tree)

