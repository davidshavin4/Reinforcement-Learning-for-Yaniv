import numpy as np
import random
from utils import Card, Deck, CustomDict


class Action:
    """
    NOTE: an action for Harel will consist of picking a card from either the pile or the stack
    in addition, we'll lay down cards on the pile. 
    NOTE: If we lay down a number which we have multiple instances of, then we'll lay down all
    instances (there'll be no possibility to lay down 1 card with the number n if we have multiple
    card of with the number n, instead we'll have to lay down all instances of cards with the number n), this will simplify 
    things and make the training easier due to the reduction in the action space        
    """
    action_dims = 2
    
    def __init__(self, move, number_to_pile):
        """
        move: MOVE object (enum)
        number_on_pile: the number on top of the pile
        first number: 0->3: 1=YANIV | 2=PILE | 3=STACK
        second number: number to put on pile (if we call Yaniv, this will be 0)        
        """
        self.action = np.zeros(Action.action_dims, dtype=np.int8)        
        self.action[0] = move.value
        self.action[1] = number_to_pile
        
    def __eq__(self, other):
        if np.sum(self.action != other.action)>0:
            return False
        return True
    
    def __hash__(self):
        return hash(tuple(self.action))
    
    def __str__(self):
        return str(self.action)
    
            

class State:
    """
    The state will be represented by a vector with 6 dimensions, the first 5 dimensions
    will represent the cards the player has in his hand (if the player has less than 5
    cards in his hand then the corresponding dimension of the missing cards will be 
    represented by 0 (in terms of the game having no card and a card with the number 
    of 0 (joker) is equivalent.
    The 6th dimension will represent the number on top of the pile, if Yaniv is called it will be -1
    """
    
    state_dims = 6
    
    def __init__(self, deck, number_on_pile): 
        """
        dims 1to5 is represent the numbers in the player's deck, dimension 6 represents the number on top of the pile      
        """
        self.state = np.zeros(State.state_dims, dtype=np.int8)                       
        deck.sort_cards()        
        for i, card in enumerate(deck.cards):
            self.state[i] = card.number     
        
        self.state[-1] = number_on_pile
            
    def __eq__(self, other):
        if np.sum(self.state != other.state)>0:
            return False
        return True
    
    def __hash__(self):
        return hash(tuple(self.state))
    
    def __str__(self):
        return str(self.state)
    
        