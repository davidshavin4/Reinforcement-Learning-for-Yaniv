import numpy as np
import random
from utils import MOVE, Move, SUITS, Card, Deck, CustomDict
from enum import Enum
from RL_utils import State, Action

SCORE_FOR_YANIV = 7


class PLAYERS(Enum):
    """
    An Enum representing all the possible players in the game
    """
    HAREL_PLAYER = 1
    GREEDY_RANDOM_PLAYER = 2
    SEMI_RANDOM_PLAYER = 3
    REAL_PLAYER = 4
    
    
class RealPlayer:  
    
    def __init__(self, name="real_player_name"):
        """
        name: the player's name
        """
        self.player = PLAYERS.REAL_PLAYER
        self.deck = Deck()
        self.name = name#a name to better keep track of the players in case of multiple players
        
    def __str__(self):
        return "RealPlayer " + self.name + "\ncards: " + str(deck)
    
    def move(self): 
        """
        makes the player's move, updating it's own cards
        and returns a move object
        """
        cards_as_string = ""
        for card in self.deck.cards:
            cards_as_string += " "+str(card)            
        print(self.name, ' cards: ', cards_as_string)               
        
        can_call_yaniv = True if self.get_score() <= SCORE_FOR_YANIV else False


        move = "not_digit"
        valid_in = False
        while not isinstance(move, int) or not valid_in:      
            move = input("Enter your move or Q to quit 1=YANIV | 2=PILE | 3=STACK")
            if not move.isdigit():
                if move == "Q" or move == "q":
                    exit()
                print("ERROR: enter only digits")
            else:
                move = int(move)
                if move not in [1, 2, 3]:
                    print('illegal input, try again')
                elif move==1 and not can_call_yaniv:
                    print("you can't call YANIV, choose different move")
                else:
                    valid_in = True


        if move == 1:
            print('you called YANIV!!')
            return Move(MOVE.YANIV)
        elif move == 2:
            move = MOVE.PILE
        else:
            move = MOVE.STACK
                    
        while True:
            input_is_valid = True
            indicies = []
            numbers = []
            cards_to_drop = []
            user_input = input("enter the INDICIES of the cards you want to put down, from 1 to " + str(self.deck.size()))            
            for index in user_input.split():
                if not index.isdigit():
                    print("ERROR: enter only digits")
                    input_is_valid = False
                    break
                index = int(index)
                if index not in range(1, self.deck.size()+1):
                    print("ERROR: index " + str(index) + " is not in deck's range")
                    input_is_valid = False
                    break        
                indicies.append(index)

            for i in indicies:
                numbers.append(self.deck.cards[i-1].number)
                cards_to_drop.append(self.deck.cards[i-1])
            deck_to_drop = Deck(cards_to_drop)
            deck_to_drop.sort_cards()
            cards_to_drop = deck_to_drop.cards
            cards_are_serie = True#checks if cards are a serie of 3 or more consequitive cards of the same suit
            if len(cards_to_drop) < 3:
                cards_are_serie = False
            else:
                suit = cards_to_drop[0].suit
                current_number = cards_to_drop[0].number
                for card in cards_to_drop[1:]:
                    if card.suit != suit or card.number != current_number+1:
                        cards_are_serie = False
                    current_number += 1
            if (len(set(numbers)) == 1 and input_is_valid) or (cards_are_serie and input_is_valid):
                print('cards to output:')
                for card in cards_to_drop:
                    print(card)
                self.deck.remove(cards_to_drop)                                
                return Move(move, cards_to_drop)
            print("ERROR: This combination of cards can't be layed in the pile")

    
    
    def get_score(self):
        """
        returns the score of the player
        """
        score = 0
        for card in self.deck.cards:
            score+=card.number
        return score    


class SemiRandomPlayer:
    """
    This player will choose randomly which card to drop from its deck
    If it chooses a number which we have multiple instances of cards with 
    that number then we'll put all these instances on the pile.
    It will choose from where to take a card (the pile or the stack) accordingly:
    if the card that is being dumped into the pile has a higher value than what's
    on top of the pile than it will take the card from the pile, else, it will take 
    a card from the stack
    NOTE: The player will call YANIV when it can
    """
    
    def __init__(self, name='srplayer', display=False):
        """
        name: the player's name
        display: do we want to display the player's card during the game        
        """
        self.player = PLAYERS.SEMI_RANDOM_PLAYER#type of player
        self.name = name
        self.display = display
        self.deck = Deck()#will start with an empty deck and the GameManger will give it cards        
        
        
    def __str__(self):
        return "SemiRandomPlayer " + self.name + "\n" + "cards: " + str(self.deck)
        
    def move(self, number_on_pile):   
        """
        number_on_pile: the number on top of the pile
        makes the player's move, updating it's own cards
        and returns a move object
        """
        if self.get_score() <= SCORE_FOR_YANIV:
            return Move(MOVE.YANIV)
        
        if self.display:
            cards_as_string = ""
            for card in self.deck.cards:
                cards_as_string += " "+str(card)
            print(self.name + " cards: ", cards_as_string)
        
        numbers_in_deck = self.deck.get_numbers_in_deck()
        number_to_drop = random.choice(numbers_in_deck)
        cards_to_drop = []
        for card in self.deck.cards:
            if card.number == number_to_drop:
                cards_to_drop.append(card)
                
        move = MOVE.PILE if number_to_drop>number_on_pile else MOVE.STACK
         
        self.deck.remove(cards_to_drop)
        return Move(move, cards_to_drop)
        
                            
            
    def get_score(self):
        """
        returns the score of the player
        """
        score = 0
        for card in self.deck.cards:
            score+=card.number
        return score
                      
    
class GreedyRandomPlayer:
    """
    This player will choose randomly on if to 
    switch it's lowest card with what's on the 
    top of the pile or with what's on top of the deck
    this player is greedy, meaning, if Yaniv is a legal move then he'll call "Yaniv"
    NOTE: If the player can put down multiple cards it will prefer doing that than 
    just putting down the lowest value card
    """
    
    
    def __init__(self, p=0.5, name='grplayer', display=False):
        """
        cards: a list of cards
        p: the probability to take a card from the stack, by default it's 0.5
        name: the player's name
        display: do we want to display the player's card during the game 
        """
        self.player = PLAYERS.GREEDY_RANDOM_PLAYER#type of player
        self.deck = Deck()#will start with an empty deck and the GameManger will give it cards
        self.name = name
        self.display = display
        self.p = p
        
        
    def __str__(self):
        return "GreedyRandomPlayer " + self.name + " with p = " + str(self.p) + "\n" + "cards: " + str(self.deck)
        
    def move(self):
        """        
        makes the player's move, updating it's own cards
        and returns a move object        
        The random player will make a random move, note, it will be responsible of removing its cards from its deck
        legal_moves is a list of MOVES (enum)
        """
        
        if self.display:
            cards_as_string = ""
            for card in self.deck.cards:
                cards_as_string += " "+str(card)
            print(self.name + " cards: ", cards_as_string)
        
        if self.get_score() <= SCORE_FOR_YANIV:
            return Move(MOVE.YANIV)
        #we'll sort the deck here so most_frequent_cards will work properly::
        #self.deck.sort_cards()
        most_frequent_cards = self.deck.most_frequent_cards()
                
        self.deck.remove(most_frequent_cards)
        
        if random.uniform(0, 1) < self.p:   
            return Move(MOVE.STACK, most_frequent_cards)        
        return Move(MOVE.PILE, most_frequent_cards)
                            
            
    def get_score(self):
        """
        returns the score of the player
        """
        score = 0
        for card in self.deck.cards:
            score+=card.number
        return score
        
        

class HarelPlayer:
    
    def __init__(self, lr, p_exploration, discount, name='harel', display=False):
        """
        lr: learning rate
        p_exploration: the probability to explore randomally
        discount: discount
        name: the player's name
        display: do we want to display the player's card during the game 
        """
        self.player = PLAYERS.HAREL_PLAYER
        self.lr = lr
        self.p_exploration = p_exploration
        self.discount = discount        
        self.deck = Deck()#will start with an empty deck and the GameManger will give it cards        
        self.qvalues = CustomDict()
        self.name = name
        self.display = display
        
        
        
    def __str__(self):
        return "HarelPlayer\n" + "cards: " + str(self.deck)    
        
    def move(self, number_on_pile):      
        """
        number_on_pile: the number on top of the pile
        makes the player's move, updating it's own cards
        and returns a move object
        """
        if self.display:
            cards_as_string = ""
            for card in self.deck.cards:
                cards_as_string += " "+str(card)
            print(self.name + " cards: ", cards_as_string)
            
        self.last_state = State(self.deck, number_on_pile)
        ## If this number > greater than epsilon --> exploitation (taking the biggest Q value for this state)
        if random.uniform(0,1) > self.p_exploration:
            action = self.getPolicy(self.last_state) 
        else:
            action = random.choice(self.get_legal_actions(self.last_state))
                    
                  
        #We need the last action when updating the qvalues
        self.last_action = action
        number_to_remove = action.action[1]
        cards_to_pile = []
        for card in self.deck.cards:
            if card.number == number_to_remove:
                cards_to_pile.append(card)             
        self.deck.remove(cards_to_pile)                        

        if action.action[0] == 1:
            #YANIV
            return Move(MOVE(action.action[0]))

        elif action.action[0] == 2:
            #PILE              
            return Move(MOVE(action.action[0]), cards_to_pile)
        elif action.action[0] == 3:
            #STACK                
            return Move(MOVE(action.action[0]), cards_to_pile)
        
        #You shouldn't get here

                           
            
    def update(self, next_state, reward):
        """
        next_state: the agent's next_state
        reward: the agent's reward
        This functions update the qvalues of the player
        """
        state = self.last_state
        action = self.last_action
        self.qvalues[(state, action)] = self.getQValue(state, action) + self.lr*(reward + self.discount*self.getValue(next_state) - self.getQValue(state, action))
    
    
    def getQValue(self, state, action):
        """
        Returns Q(state,action)
        Should return 0.0 if we never seen
        a state or (state,action) tuple
        """    
        return self.qvalues[(state, action)]
    
        
    def getValue(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        action = self.getPolicy(state)
        return self.getQValue(state, action)


        
    def getPolicy(self, state):
        """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
        """    
        if len(self.get_legal_actions(state)) == 0:
            return None    
        max_qvalue = np.max(np.array([self.getQValue(state, action) for action in self.get_legal_actions(state)]))
        best_actions = []
        for action in self.get_legal_actions(state):
            if self.getQValue(state, action) == max_qvalue:
                best_actions.append(action)
        return random.choice(best_actions)

        
    def get_legal_actions(self, state):
        """
        returns a list of the legal actions given the state
        """
        legal_actions = []
        if self.get_score() <= SCORE_FOR_YANIV:
            legal_actions.append(Action(MOVE.YANIV, 0))
        for number_in_deck in self.deck.get_numbers_in_deck():
            legal_actions.append(Action(MOVE.PILE, number_in_deck))
            legal_actions.append(Action(MOVE.STACK, number_in_deck))
        return legal_actions
        

    def get_score(self):
        """
        returns the score of the player
        """
        score = 0
        for card in self.deck.cards:
            score+=card.number
        return score
        
        

        
    