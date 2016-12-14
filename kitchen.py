from menu import *

class RamenBowl:
    
    def __init__(self, broth = None, size = None,
                 spiciness = None, protein = None):
        self.broth = broth
        self.size = size
        if self.size is None:
            self.size = 'full'
        self.spiciness = spiciness
        self.protein = protein
        self.toppings = []
        self.sauces = []
    def update_broth(self, broth_new):
        if broth_new in broths:
            self.broth = broth_new
    def update_protein(self,new_protein):
        if new_protein in proteins:
            self.protein = new_protein
    def update_size(self, size_to_add):
        if size_to_add in sizes:
            self.size = size_to_add
    def update_spice(self, spice_to_add):
        if spice_to_add in spiciness:
            self.spiciness = spice_to_add
    def add_toppings(self, toppings_to_add):
        if isinstance(toppings_to_add, list):
            for topping in toppings_to_add:
                self.add_toppings(topping)
        else:
            if toppings_to_add in toppings:
                self.toppings.append(toppings_to_add)

    def remove_toppings(self, toppings_to_remove):
        if isinstance(toppings_to_remove, list):
            for topping in toppings_to_remove:
                self.remove_toppings(topping)
        else:
            self.toppings.remove(toppings_to_remove)
    
    def price(self):
        price = sizes[self.size]['price']
        if len(self.sauces) > 0:
            price += sum([sauces[s]['price'] for s in self.sauces])
        return price
    
    def __str__(self):
        string = ''
        if self.spiciness is None:
            string += '(spiciness)'
        else:
            string += self.spiciness + ' '
        string += self.size
        if self.broth is None:
            string += ' (broth)'
        else:
            string += ' ' + self.broth
        if self.protein is None:
            string += ' (protein)'
        else:
            string += ' ' + self.protein
        if len(self.toppings) > 0:
            for topping in self.toppings:
                string += ', ' + topping
        return string

class App:
    
    def __init__(self, app = None):
        if not (app is None or app not in apps):
            self.app = app
    
    def price(self):
        return apps[self.app]['price']
    
    def __str__(self):
        if self.app is None:
            return 'NA'
        else:
            return self.app

class Drink:
    
    def __init__(self, drink = None):
        if not (drink is None or drink not in drinks):
            self.drink = drink
    
    def price(self):
        price = drinks[self.drink]['price']
        return price
    
    def __str__(self):
        if self.drink is None:
            return 'NA'
        else:
            return self.drink

class Sauce:
    
    def __init__(self, sauce = None):
        if not (sauce is None or sauce not in sauces):
            self.sauce = sauce
    
    def price(self):
        price = sauces[self.sauce]['price']
        return price
    
    def __str__(self):
        if self.sauce is None:
            return 'NA'
        else:
            return self.sauce

class Order:
    
    items = []
    
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        if isinstance(item, (RamenBowl, App, Drink, Sauce)):
            self.items.append(item)
    
    def price(self):
        return sum([item.price() for item in self.items])
    
    def __str__(self):
        string = ''
        if len(self.items) > 0:
            string = '\n'.join(str(item) for item in self.items)
        return string
    
    def reset(self):
        items = []        
