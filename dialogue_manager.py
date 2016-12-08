import nltk, re
from nltk import word_tokenize
from menu import *
from kitchen import *
from copy import deepcopy


grammar_filename = 'ramen_grammar.fcfg'
order = Order()
termlimit = False
item_rank = 0
parser = nltk.parse.load_parser(grammar_filename)

# for converting spelled numbers to arabic numerals
num_conversion_dict = {
    'zero' : '0',
    'one' : '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'ten': '10',
    'eleven': '11',
    'twelve': '12',
    'thirteen': '13',
    'fourteen': '14',
    'fifteen': '15',
    'sixteen': '16',
    'seventeen': '17',
    'eighteen': '18',
    'nineteen': '19',
    'twenty': '20',
    }

phrases_to_unify = ['with no', 'let me', 'as well as', 'in addition to',
            
                    'lot of', 'lots of', 'on top of', 'some more',
                    
                    'diet coca cola' , 'diet coke', 'diet cola', 'coca cola',

                    'minute maid lemonade', 'minute made lemonade', \
                    'minute maid', 'minute made', 'jasmine pearl'

                    'spring roll', 'egg roll', 'squid ball', 'chili oil', 'chili sauce',
                    'soy sauce', 'gyoza sauce',
                    'sriracha sauce', 'fish cake', 'bok choy', 'sea weed', 'bean sprout',

                    'diet coca colas' , 'diet cokes', 'diet colas', 'coca colas',

                    'minute maid lemonades', 'minute made lemonades', \
                    'minute maids', 'minute mades', 'jasmine pearls'

                    'spring rolls', 'egg rolls', 'squid balls', 'chili oils', 'chili sauces',
                    'soy sauces', 'gyoza sauces',
                    'sriracha sauces', 'fish cakes', 'bok choys', 'sea weeds', 'bean sprouts',

                    'not spicy', 'somewhat spicy', 'real spicy', 'very spicy', 'extremely spicy',

                    'at all'
                    ]


phrases_to_eliminate = ['please', 'thanks', 'thank you', 'to order', 'to get', 'to have',
                        'to buy', 'to eat', 'to add', 'extra', 'tea', 'size', 'sized','spring rolls',
                        'egg rolls', 'squid balls', 'chili oils', 'chili sauces','soy sauces',
                        'gyoza sauces','sriracha sauces', 'fish cakes', 'bok choys', 'sea weeds',
                        'bean sprouts','at all']

phrases_to_eliminate = ['please', 'thanks', 'thank you', 'to order', 'to get', 'to have',
                        'to buy', 'to eat', 'to add', 'extra', 'tea','size']

phrases_with_s = ["let's","plus", "as", "has", "lots", "yes", "glass" ,"is"]

def preprocess(sentence):
    s = sentence.lower()
    s = re.sub(r'[\.,;?!"]', '', s)
    s = re.sub(r'-', ' ', s)

    # get rid of non-important phrases
    for phrase in phrases_to_eliminate:
        s = re.sub(phrase, '', s)

    # unify phrases to compound tokens
    for phrase in phrases_to_unify:
        new_phrase = re.sub(r' ', '_', phrase)
        s = re.sub(phrase, new_phrase, s)
    s = s.split()

    #get rid of plurals
    i = 0
    while i<len(s):
        if s[i] not in phrases_with_s:
            s[i] = re.sub(r's$','',s[i])
        i+=1

    for word in s:
        # make sure that all the words are in the grammar; if not, ask to repeat
        try:
            parser.chart_parse([word])
        except ValueError:
            s = ''
            return s
        #convert worded numbers to numerals
        if word in num_conversion_dict.keys():
            numeral = num_conversion_dict[word]
            replace_at_index = s.index(word)
            s[replace_at_index] = numeral
        # unify veggies 
        elif word == 'veggie' or word == 'veg':
            s[s.index(word)] = 'vegetable'
        # unify teas
        if word == 'jasmine_pearl' or word == 'pearl':
            s[s.index(word)] = 'jasmine'
        # unify sodas
        elif word == 'coke' or word == 'cola' or word == 'coca_cola':
            s[s.index(word)] = 'coke'
        elif word == 'diet_coke' or word == 'diet_coca_cola':
            s[s.index(word)] = 'diet_coke'
        # unify lemonades:
        elif word == 'minute_maid' or word == 'minute_made' or \
             word == 'minute_maid_lemonade' or word == 'minute_made_lemonade':
            s[s.index(word)] = 'lemonade'
        # unify sizes:
        elif word == 'small' or word == 'tiny' or word == 'baby':
            s[s.index(word)] = 'half'
        elif word == 'large' or word == 'big' or word == 'jumbo' or word =='whole' or word == 'regular':
            s[s.index(word)] = 'full'
        elif word == 'not_spicy':
            s[s.index(word)] = 'mild'
        elif word == 'somewhat_spicy':
            s[s.index(word)] = 'medium'
        elif word == 'very_spicy' or word == 'extremely_spicy' or word == 'real_spicy':
            s[s.index(word)] = 'hot'
           
    return s

def parse_sentence(sentence):
    processed = preprocess(sentence)
    return [tree for tree in parser.parse(processed)]

def respond(sentence, parses):
    global termlimit, item_rank
    if len(parses) == 0:
        return "I'm sorry; I don't know what that means."
    #user response to "would you like anything else?"
    elif parses[0].leaves() == ['yes']:
        return "What else can I get for you?"
    elif parses[0].leaves() == ['no']:
        termlimit = True
        # check ramen bowls for missing information here...
        for item in order.items:
            item_rank = order.items.index(item)
            if isinstance(item, RamenBowl):
                if item.broth == None:
                    response = "What broth would you like for your ramen?\n'shio', 'shoyu', 'miso', 'tontaksu', 'vegan'"
                    return response
                if item.spiciness == None:
                    response = "How spicy would you like your ramen?\n mild, medium, or hot"
                    return response
                if item.protein == None:
                    response = "Which protein would you like in your ramen?\n'tofu', 'beef', 'pork', 'chicken', 'vegetable'"
                    return response
                if item.toppings == None:
                    response = "Would you like any toppings in your ramen?\nfishcake, naruto, mushroom, bean sprouts, kimchi, bok choy, seaweed (nori)"
                    return response                
        return "Your total is $" + str(order.price()) + ".00"
        order.reset()
    #cyute
    elif parses[0].leaves() == ['summon', 'mama']:
        try:
            import antigravity
            return "Now what do you want?"
        except ImportError:
            return "Eat ramen or go away."        
    else:
        response = 'I heard you say "' + sentence + '"\n'
        for p in parses:
            print('PARSE OF "' + sentence + '" (of ' + str(len(parses)) + '):')
            print(p)
            print()
        parse = parses[0]
        
        # Get the OIs in the parse.
        order_items = get_OIs(parse)

        # if they're not done ordering, add new items
        if termlimit == False:
            # Iterate through the OIs and add the foods they mention to the
            # order.
            for item in order_items:
                # Figure out what kind of item the user requested by looking
                # for keywords.
                leaves = item.leaves()
                word_set = set(leaves)
                item_type = 'none'
                item_word = ''
                multiple = 1
                n = 1
                if len(word_set & set(num_conversion_dict.values())) > 0:
                    multiple = int(list(set(word_set) & \
                                    set(num_conversion_dict.values()))[0])
                #broths (and ramen for now)
                if len(word_set & broths) > 0\
                   or len(word_set & proteins) > 0\
                    or len(word_set & cont_nouns) > 0:
                            item_type = 'ramen_bowl'
                #apps
                elif len(word_set & set(apps.keys())) > 0:
                    item_type = 'app'
                    item_word = list(word_set & set(apps.keys()))[0]

                #drinks
                elif len(word_set & set(drinks.keys())) > 0:
                    item_type = 'drink'
                    item_word = list(word_set & set(drinks.keys()))[0]

                elif len(word_set & set(sauces.keys())):
                    item_type = 'sauce'
                    item_word = list(word_set & set(sauces.keys()))[0]
                    
                # If the user wants a ramen bowl...
                if item_type == 'ramen_bowl':
                    new_ramen = RamenBowl()
                    # Check for toppings in the leaves of the tree.
                    for leaf in leaves:
                        if leaf in toppings:
                            new_ramen.add_toppings(leaf)
                        elif leaf in broths:
                            new_ramen.update_broth(leaf)
                        elif leaf in sizes:
                            new_ramen.update_size(leaf)
                        elif leaf in proteins:
                            new_ramen.update_protein(leaf)
                            
                    if multiple == 1:
                        order.add_item(deepcopy(new_ramen))
                        response += "  I've added a ramen bowl to your order."
                    else:
                        while n <= multiple:
                            order.add_item(deepcopy(new_ramen))
                            n+=1
                        response += "  I've added " + str(multiple) + " ramen bowls to your order."
                    
                # If the user mentioned an app...
                elif item_type == 'app':
                    new_app = App(item_word)
                    if multiple == 1:
                        order.add_item(deepcopy(new_app))
                        response += "  I've added a " + item_word + " to your order."
                    else:
                        while n <= multiple:
                            order.add_item(deepcopy(new_app))
                            n+=1
                        response += "  I've added " + str(multiple)+ " " + item_word + "s " + " to your order."
                    
                # If the user mentioned a drink...
                elif item_type == 'drink':
                    new_drink = Drink(item_word)
                    if multiple == 1:
                        order.add_item(deepcopy(new_drink))
                        response += "  I've added a " + item_word + " to your order."
                    else:
                        while n <= multiple:
                            order.add_item(deepcopy(new_drink))
                            n+=1                    
                        response += "  I've added " + str(multiple) + " "+ item_word + "s " + " to your order."

                # If the user mentioned a sauce...
                elif item_type == 'sauce':
                    new_sauce = Sauce(item_word)
                    if multiple == 1:
                        order.add_item(deepcopy(new_sauce))
                        response += "  I've added a " + item_word + " to your order."
                    else:
                        while n <= multiple:
                            order.add_item(deepcopy(new_sauce))
                            n+=1
                        response += "  I've added " + str(multiple) + " " + item_word + "s " + " to your order."

            response += "  Would you like anything else?"
            return response
        else:
            for item in order_items:
                leaves = item.leaves()
                for leaf in leaves:
                    if leaf in toppings:
                        order.items[item_rank].add_toppings(leaf)                    
                    elif leaf in spiciness:
                        order.items[item_rank].update_spice(leaf)
                    elif leaf in broths:
                        order.items[item_rank].update_broth(leaf)
                    elif leaf in sizes:
                        order.items[item_rank].update_size(leaf)
                    elif leaf in proteins:
                        order.items[item_rank].update_protein(leaf)
                        
    respond('no',parse_sentence('no'))
                    

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

