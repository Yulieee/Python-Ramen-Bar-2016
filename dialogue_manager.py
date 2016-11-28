import nltk, re
from menu import *
from kitchen import *
from copy import deepcopy

grammar_filename = 'ramen_grammar.fcfg'
order = Order()
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
    s = re.sub(r'-', ' ', s)
    s = re.sub(r'please', '', s)

    # unify phrases to compound tokens
    for phrase in phrases_to_unify:
        new_phrase = re.sub(r' ', '_', phrase)
        s = re.sub(phrase, new_phrase, s)
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
    return [tree for tree in parser.parse(processed)]

def respond(sentence, parses):
    if len(parses) == 0:
        return "I'm sorry; I don't know what that means."

    else:
        response = 'I heard you say "' + sentence + '"\n'
        for p in parses:
            print('PARSE OF "' + sentence + '" (of ' + str(len(parses)) + '):')
            print(p)
            print()
        parse = parses[0]
        # Get the OIs in the parse.
        order_items = get_OIs(parse)
        # Iterate through the OIs and add the foods they mention to the
        # order.
        for item in order_items:
            # Figure out what kind of item the user requested by looking
            # for keywords.
            leaves = item.leaves()
            word_set = set(leaves)
            item_type = 'none'
            item_word = ''
            if len(word_set & broths) > 0\
               or len(word_set & proteins) > 0:
                item_type = 'ramen_bowl'
            elif len(word_set & set(apps.keys())) > 0:
                item_type = 'app'
                item_word = list(word_set & set(apps.keys()))[0]
            elif len(word_set & set(drinks.keys())) > 0:
                item_type = 'drink'
                item_word = list(word_set & set(drinks.keys()))[0]
            # If the user wants a ramen bowl...
            if item_type == 'ramen_bowl':
                new_ramen = RamenBowl()
                # Check for toppings in the leaves of the tree.
                for leaf in leaves:
                    if leaf in toppings:
                        new_ramen.add_toppings(leaf)
                order.add_item(deepcopy(new_ramen))
                response += "  I've added a ramen bowl to your order."
            # If the user mentioned an app...
            elif item_type == 'app':
                new_app = App(item_word)
                order.add_item(deepcopy(new_app))
                response += "  I've added a " + item_word + " to your order."
            # If the user mentioned a drink...
            elif item_type == 'drink':
                new_drink = Drink(item_word)
                order.add_item(deepcopy(new_drink))
                response += "  I've added a " + item_word + " to your order."
        response += "  Would you like anything else?"
        return response

def get_OIs(parse):
    """Return the subtrees of the parse that are OIs."""
    ois = []
    # iterate over all children until you find OIs (that aren't parents of a
    # conjoined OI)
    for node in parse:
        if not isinstance(node, str):
            if repr(node.label()).startswith('OI') and\
               (not 'CONJ' in node.label() or not node.label()['CONJ']):
                ois.append(node)
                if 'CONJ' in node.label():
                    print(node.label()['CONJ'])
            else:
                more_ois = get_OIs(node)
                ois = ois + more_ois
    return ois
