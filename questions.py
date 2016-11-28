
####################
###questions_menu###
####################

from menu import *

questions_grammar_filename = 'questions_runtime_grammar.fcfg'

def compile_questions():
    """Dynamically create a grammar file for questions."""
    
    questions_grammar_file = open(questions_grammar_filename, 'w')

    # Add phrase-structure rules from a text file.
    questions_grammar_file.write('##########################\n' +\
                                 '# Phrase-Structure Rules #\n' +\
                                 '##########################\n\n')

    questions_ps_file = open('questions_ps_rules.txt', 'r')
    for line in questions_ps_file:
        questions_grammar_file.write(line)
    questions_grammar_file.write('\n')
    
    # Add lexical entries based on information in text files.  Also add these
    # words to our personal wordlist (for use in spell-checking).
    questions_grammar_file.write('###################\n' +\
                                 '# Lexical Entries #\n' +\
                                 '###################\n\n')

    # Compile information about pizzas.
    pizza_file = open('pizzas.txt', 'r')
    for line in pizza_file:
        # Read in a line from the pizza info file and split it into fields.
        info = re.split(r'\t', line[:-1])
        info = [i for i in info if len(i) > 0]
        pizza = info[0]
        pizza_price = float(info[1])
        pizza_names = set(re.split(r', ', ''.join(info[2])))
        pizza_toppings = set(re.split(r', ', ''.join(info[3:])))
        # Add the pizza's information to the `pizzas` dictionary.
        pizzas[pizza] = {'names': pizza_names,
                         'price': pizza_price,
                         'toppings': pizza_toppings}
        # Add a lexical entry with all alternate names of the pizza.
        pizza_lexinfo = {'ID': pizza,
                         'FOODTYPE': 'pizza'}
        questions_grammar_file.write(lexical_entry('N', pizza_lexinfo, pizza_names))
        # Add all the pizza names to our personal wordlist.
        wordlist_entry(list(pizza_names))
        # Add appropriate mappings for alternate names (for preprocessing).
        for standard_name in pizzas:
            for alt_name in pizzas[standard_name]['names']:
                name_mapping[alt_name] = standard_name
    questions_grammar_file.write('\n')

    # Compile information about toppings.
    topping_file = open('toppings.txt', 'r')
    for line in topping_file:
        # Read in a line from the topping info file and split it into fields.
        info = re.split(r'\t', line[:-1])
        info = [i for i in info if len(i) > 0]
        topping = info[0]
        topping_type = info[1]
        topping_price = float(info[2])
        topping_names = set(re.split(r', ', ''.join(info[3:])))
        # Add the topping's information to the `toppings` dictionary.
        toppings[topping] = {'names': topping_names,
                             'type': topping_type,
                             'price': topping_price}
        # Add a lexical entry with all alternate names of the topping.
        topping_lexinfo = {'ID': topping,
                           'FOODTYPE': 'topping',
                           'TOPPINGTYPE': topping_type}
        cat = 'N'
        questions_grammar_file.write(lexical_entry(cat, topping_lexinfo, topping_names))
        if topping_lexinfo['TOPPINGTYPE'] == 'crust':
            questions_grammar_file.write(lexical_entry('A', topping_lexinfo,
                                             topping_names))
        # Add all the topping names to our personal wordlist.
        wordlist_entry(list(topping_names))
        # Add appropriate mappings for alternate names (for preprocessing).
        for alt_name in topping_names:
            name_mapping[alt_name] = topping
    questions_grammar_file.write('\n')
    
    # Compile information about sides.
    side_file = open('sides.txt', 'r')
    for line in side_file:
        # Read in a line from the sides info file and split it into fields.
        info = re.split(r'\t', line[:-1])
        info = [i for i in info if len(i) > 0]
        side = info[0]
        side_price = float(info[1])
        side_names = set(re.split(r', ', ''.join(info[2:])))
        # Add the side's information to the `sides` dictionary.
        sides[side] = {'names': side_names,
                       'price': side_price}
        # Add a lexical entry with all alternate names of the side.
        side_lexinfo = {'ID': side,
                        'FOODTYPE': 'side'}
        questions_grammar_file.write(lexical_entry('N', side_lexinfo, side_names))
        # Add all the side names to our personal wordlist.
        wordlist_entry(list(side_names))
        # Add appropriate mappings for alternate names (for preprocessing).
        for standard_name in sides:
            for alt_name in sides[standard_name]['names']:
                name_mapping[alt_name] = standard_name
    questions_grammar_file.write('\n')
    
    # Compile information about drinks.
    drink_file = open('drinks.txt', 'r')
    for line in drink_file:
        # Read in a line from the drink info file and split it into fields.
        info = re.split(r'\t', line[:-1])
        info = [i for i in info if len(i) > 0]
        drink = info[0]
        drink_price = float(info[1])
        drink_names = set(re.split(r', ', ''.join(info[2:])))
        # Add the drink's information to the `drinks` dictionary.
        drinks[drink] = {'names': drink_names,
                         'price': drink_price}
        # Add a lexical entry with all alternate names of the drink.
        drink_lexinfo = {'ID': drink,
                         'FOODTYPE': 'drink'}
        questions_grammar_file.write(lexical_entry('N', drink_lexinfo, drink_names))
        # Add all the drink names to our personal wordlist.
        wordlist_entry(list(drink_names))
        # Add appropriate mappings for alternate names (for preprocessing).
        for standard_name in drinks:
            for alt_name in drinks[standard_name]['names']:
                name_mapping[alt_name] = standard_name
    questions_grammar_file.write('\n')
    
    # Compile information about sizes.
    size_file = open('sizes.txt', 'r')
    for line in size_file:
        # Read in a line from the size info file and split it into fields.
        info = re.split(r'\t', line[:-1])
        info = [i for i in info if len(i) > 0]
        size = info[0]
        size_type = info[1]
        size_price = float(info[2])
        size_names = set(re.split(r', ', ''.join(info[3:])))
        # Add the size's information to the `sizes` dictionary.
        sizes[size] = {'names': size_names,
                       'type': size_type,
                       'price': size_price}
        # Add a lexical entry with all alternate names of the size.
        size_lexinfo = {'ID': size,
                        'FOODTYPE': size_type}
        questions_grammar_file.write(lexical_entry('A', size_lexinfo, size_names))
        # Add all the size names to our personal wordlist.
        wordlist_entry(list(size_names))
        # Add appropriate mappings for alternate names (for preprocessing).
        for standard_name in sizes:
            for alt_name in sizes[standard_name]:
                name_mapping[alt_name] = standard_name
    questions_grammar_file.write('\n')

    # Get question lexical entries.
    questions_lex_file = open('questions_lex_entries.txt', 'r')
    for line in questions_lex_file:
        questions_grammar_file.write(line)
        wordlist_entry(re.findall(r'(?:")(\S+)(?:")', line))
    
    # Deal with words for stripping.
    for line in open(bad_word_filename, 'r'):
        wordlist_entry([line[:-1]])
        bad_words.add(line[:-1])

    questions_grammar_file.close()



#######################
###questions_kitchen###
#######################

class Questions_Order:
    
    items = []
    
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        if isinstance(item, (Pizza, Side, Drink)):
            self.items.append(item)
    
    def price(self):
        return sum([item.price() for item in self.items])
    
    def __str__(self):
        string = ''
        if len(self.items) > 0:
            string = '\n'.join(str(item) for item in self.items)
        return string



################################
###questions_dialogue_manager###
################################

from dialogue_manager import *

compile_questions()
questions_order = Questions_Order()
questions_parser = nltk.parse.load_parser(questions_grammar_filename)

def questions_parse_sentence(sentence):
    processed = preprocess(sentence)
    return [tree for tree in questions_parser.parse(processed)]

def questions_respond(sentence, parses):
    if len(parses) == 0:
        return "Uh-oh! I don't know what that means."
    else:
        response = 'I heard you ask "' + sentence + '"  '
        filtered_parses = [p for p in parses if acceptable_parse(p)]
        if len(filtered_parses) > 0:
            parses = filtered_parses
        for p in parses:
            print('PARSE OF "' + sentence + '" (of ' + str(len(parses)) + '):')
            print(p)
            print()
        parse = parses[0]
        # Get the `maximal NPs` in the parse - NPs that aren't dominated by
        # other NPs.  If we've done things right, each maximal NP should
        # correspond to a single item that we want to add to the order.
        item_nps = maximal_NPs(parse)
        # Iterate through the maximal NPs and add the foods they mention to the
        # order.
        for np in item_nps:
            # Look for determiners, which might specify an amount.  Use the top-
            # level NP unless this is an "order" NP, in which case look deeper
            # into the tree if no amount is specified at a higher level.
            amount_np = np
            amount = get_amount(np)
            if amount == 1 and 'order' in amount_np.leaves():
                for i in range(len(amount_np)):
                    if repr(amount_np[i].label()).startswith('N')\
                       and amount_np[i].label()['FOODTYPE'] != 'topping':
                        amount_np = amount_np[i][2]
                        amount = get_amount(amount_np)
            # Figure out what kind of item the user requested.
            leaves = np.leaves()
            word_set = set(leaves)
            item_type = 'none'
            item_word = ''
            if len(word_set & set(pizzas.keys())) > 0:
                item_type = 'pizza'
            elif len(word_set & set(sides.keys())) > 0:
                item_type = 'side'
                item_word = list(word_set & set(sides.keys()))[0]
            elif len(word_set & set(drinks.keys())) > 0:
                item_type = 'drink'
                item_word = list(word_set & set(drinks.keys()))[0]
            else:
                last_item = questions_order.items[-1]
                if isinstance(last_item, Pizza):
                    item_type = 'pizza'
                elif isinstance(last_item, (Drink, Side)):
                    for i in range(amount):
                        questions_order.add_item(deepcopy(last_item))
            # If the user wants a pizza...
            if item_type == 'pizza':
                new_pizza = Pizza()
                # Check whether the user mentioned a specialty pizza.
                for leaf in leaves:
                    if leaf in pizzas:
                        for topping in pizzas[leaf]['toppings']:
                            new_pizza.add_topping(topping)
                # Check for toppings in the leaves of the tree.
                for leaf in leaves:
                    if leaf in toppings:
                        if toppings[leaf]['type'] == 'crust':
                            new_pizza.crust = leaf
                        elif not leaf in new_pizza.toppings:
                            new_pizza.add_topping(leaf)
                    elif leaf + '_pizza' in sizes:
                        new_pizza.size = leaf + '_pizza'
                # Remove items
                for leaf in leaves:
                    if leaf in {'minus','without'}:
                        next_leaf = leaves[leaves.index(leaf)+1]
                        if next_leaf in toppings:
                            new_pizza.remove_topping(next_leaf)
                for i in range(amount):
                    questions_order.add_item(deepcopy(new_pizza))
            # If the user mentioned a side...
            elif item_type == 'side':
                new_side = Side(item_word)
                for i in range(amount):
                    questions_order.add_item(deepcopy(new_side))
            # If the user mentioned a drink...
            elif item_type == 'drink':
                new_drink = Drink(item_word)
                for leaf in leaves:
                    if leaf + '_drink' in sizes:
                        new_drink.size = leaf + '_drink'
                for i in range(amount):
                    questions_order.add_item(deepcopy(new_drink))

        questions_np = str(questions_order)
        questions_order_string = '${:.2f}'.format(questions_order.price())
        price_question = False
        for i in range(len(parse)):
            if repr(parse[i].label()).startswith('WH')\
               and parse[i].label()['QUESTIONTYPE'] == 'price':
                price_question = True
        if price_question:
            questions_response = response + questions_np + " will cost " + questions_order_string + "."
        else:
            questions_response = response + "Yes, we have " + questions_np + "."
        questions_order.items = []
        return questions_response
