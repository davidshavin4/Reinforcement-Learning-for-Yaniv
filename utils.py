import numpy as np
import random
from collections import Counter
from functools import cmp_to_key
from enum import Enum

class SUITS(Enum):
    HEARTS=1
    SPADES=2
    DIAMOND=3
    CLUBS=4
    
    def __str__(self):
        if self.value == 1:
            return "♥"
        elif self.value == 2:
            return "♠"
        elif self.value == 3:
            return "♦"
        else:
            return "♣"

class MOVE(Enum):
    YANIV=1
    PILE=2
    STACK=3
    
    def __str__(self):
        if self.value == 1:
            return "YANIV"
        elif self.value == 2:
            return "PILE"
        elif self.value == 3:
            return "STACK"
    
class Move:   
    
    def __init__(self, move, input_cards=None):
        """
        move: an enum of MOVE
        input_deck: the deck the player is inserting onto the pile (usually of size 1)
        """
        self.move = move
        self.input_cards = input_cards
        
    def __str__(self):
        return "MOVE: " + str(self.move) + "\nINPUT_CARDS: "+str(Deck(self.input_cards))
    

    
    

def compare(card1, card2):
    """
    compares the number on 2 cards
    NOTE: this compare doesn't care about the suit 
    """
    return card1.number - card2.number
    
class Card:
    """
    Representation of a real card
    """
    
    def __init__(self, number, suit=None):
        """
        number: the number on the card
        suit: the suit on the card
        note: suit=None will be the case for a joker
        """
        self.number = number
        self.suit = suit
        
    def __str__(self):
        if self.suit==None:
            return "🃏"
        return str(self.number)+"_"+str(self.suit)

class Deck:   
    """
    holds a list of cards, contains many useful function to preform on the cards
    """
    
    def __init__(self, cards=None):
        #cards: a list of the cards the deck holds
        if cards==None:
            self.cards = []
        else:
            self.cards = cards
                
    def __str__(self):
        output = ""
        if len(self.cards) == 0:
            return output
        for card in self.cards[:-1]:
            output += str(card) + " | "
        output += str(self.cards[-1])
        return output             
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def join(self, cards):
        """
        joins with another deck, note: it doesn't check if joined deck is valid (might contain 2 of the same card twice)
        """
        self.cards += cards
        
    def pop(self, n=-1):
        """
        n: the index to pop from
        make sure you don't pop from an empty list
        """
        return self.cards.pop(n)
    
    def remove(self, cards):
        """
        takes a list of cards and removes them from the deck
        """
        for card in cards:
            self.cards.remove(card)

    
    def sort_cards(self):
        """
        sorts a list of cards
        NOTE: this function doesn't care about suits, and the suits at each value of the cards might be mixed
        """
        self.cards =  sorted(self.cards,  key=cmp_to_key(compare))        
    
    def most_frequent_number(self):
        """
        returns the most frequent number (as an int) in the deck and the number of times it appeared
        NOTE: if multiple numbers have the same number of instances in the deck, we'll return the 
        maximal number out of these numbers
        """
        players_cards_only_numbers = []
        for card in self.cards:
            players_cards_only_numbers.append(card.number)
        players_cards_only_numbers.sort()
        return Counter(players_cards_only_numbers[::-1]).most_common(1)[0]
                        
    def most_frequent_cards(self):
        """
        returns a list of the most frequent cards in the list (by number) as a list of cards
        """
        most_frequent_number = self.most_frequent_number()[0]        
        most_frequent_cards = []
        for card in self.cards:
            if card.number == most_frequent_number:
                most_frequent_cards.append(card)
        return most_frequent_cards
    
    def size(self):
        return len(self.cards)
    
    def get_numbers_in_deck(self):
        """
        returns a list of all the numbers in the deck (without repetitions)
        """
        numbers_in_deck = set()
        for card in self.cards:
            numbers_in_deck.add(card.number)
        numbers_in_deck = list(numbers_in_deck)
        numbers_in_deck.sort()
        return numbers_in_deck
                
    def print(self):
        for card in self.cards:
            print(card)
            
            
            
class CustomDict(dict):
  """
  A counter keeps track of counts for a set of keys.
  
  The counter class is an extension of the standard python
  dictionary type.  It is specialized to have number values  
  (integers or floats), and includes a handful of additional
  functions to ease the task of counting data.  In particular, 
  all keys are defaulted to have value 0.  Using a dictionary:
  
  a = {}
  print(a['test'])
  
  would give an error, while the Counter class analogue:
    
  >>> a = Counter()
  >>> print(a['test'])
  0

  returns the default 0 value. Note that to reference a key 
  that you know is contained in the counter, 
  you can still use the dictionary syntax:
    
  >>> a = Counter()
  >>> a['test'] = 2
  >>> print(a['test'])
  2
  
  This is very useful for counting things without initializing their counts,
  see for example:
  
  >>> a['blah'] += 1
  >>> print(a['blah'])
  1
  
  The counter also includes additional functionality useful in implementing
  the classifiers for this assignment.  Two counters can be added,
  subtracted or multiplied together.  See below for details.  They can
  also be normalized and their total count and arg max can be extracted.
  """
  def __getitem__(self, idx):
    self.setdefault(idx, 0)
    return dict.__getitem__(self, idx)

  def incrementAll(self, keys, count):
    """
    Increments all elements of keys by the same count.
    
    >>> a = Counter()
    >>> a.incrementAll(['one','two', 'three'], 1)
    >>> a['one']
    1
    >>> a['two']
    1
    """
    for key in keys:
      self[key] += count
  
  def argMax(self):
    """
    Returns the key with the highest value.
    """
    if len(self.keys()) == 0: return None
    all = list(self.items())
    values = [x[1] for x in all]
    maxIndex = values.index(max(values))
    return all[maxIndex][0]
  
  def sortedKeys(self):
    """
    Returns a list of keys sorted by their values.  Keys
    with the highest values will appear first.
    
    >>> a = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> a['third'] = 1
    >>> a.sortedKeys()
    ['second', 'third', 'first']
    """
    sortedItems = list(self.items())    
    sortedItems.sort(key=lambda item: -item[1])
    return [x[0] for x in sortedItems]
  
  def totalCount(self):
    """
    Returns the sum of counts for all keys.
    """
    return sum(self.values())
  
  def normalize(self):
    """
    Edits the counter such that the total count of all
    keys sums to 1.  The ratio of counts for all keys
    will remain the same. Note that normalizing an empty 
    Counter will result in an error.
    """
    total = float(self.totalCount())
    if total == 0: return
    for key in self.keys():
      self[key] = self[key] / total
      
  def divideAll(self, divisor):
    """
    Divides all counts by divisor
    """
    divisor = float(divisor)
    for key in self:
      self[key] /= divisor

  def copy(self):
    """
    Returns a copy of the counter
    """
    return Counter(dict.copy(self))
  
  def __mul__(self, y ):
    """
    Multiplying two counters gives the dot product of their vectors where
    each unique label is a vector element.
    
    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['second'] = 5
    >>> a['third'] = 1.5
    >>> a['fourth'] = 2.5
    >>> a * b
    14
    """
    sum = 0
    x = self
    if len(x) > len(y):
      x,y = y,x
    for key in x:
      if key not in y:
        continue
      sum += x[key] * y[key]      
    return sum
      
  def __radd__(self, y):
    """
    Adding another counter to a counter increments the current counter
    by the values stored in the second counter.
    
    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['third'] = 1
    >>> a += b
    >>> a['first']
    1
    """ 
    for key, value in y.items():
      self[key] += value   
      
  def __add__( self, y ):
    """
    Adding two counters gives a counter with the union of all keys and
    counts of the second added to counts of the first.
    
    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['third'] = 1
    >>> (a + b)['first']
    1
    """
    addend = Counter()
    for key in self:
      if key in y:
        addend[key] = self[key] + y[key]
      else:
        addend[key] = self[key]
    for key in y:
      if key in self:
        continue
      addend[key] = y[key]
    return addend
    
  def __sub__( self, y ):
    """
    Subtracting a counter from another gives a counter with the union of all keys and
    counts of the second subtracted from counts of the first.
    
    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['third'] = 1
    >>> (a - b)['first']
    -5
    """      
    addend = Counter()
    for key in self:
      if key in y:
        addend[key] = self[key] - y[key]
      else:
        addend[key] = self[key]
    for key in y:
      if key in self:
        continue
      addend[key] = -1 * y[key]
    return addend                                           