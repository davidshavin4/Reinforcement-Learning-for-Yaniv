import numpy as np
import random
from utils import MOVE, Move, SUITS, Card, Deck, CustomDict
from players import PLAYERS, GreedyRandomPlayer, HarelPlayer
from enum import Enum

CARDS_PER_PLAYER = 5

class GameManager:
    """
    The game manager will be responsible of giving a deck for each player in the list
    in addition, it will be used to run the game, we'll call the step method for each turn we'll want to make
    """
    
    def __init__(self, players, display=False):
        self.display = display
        cards = [Card(0), Card(0)]
        for i in range(1, 13):
            for suit in SUITS:
                cards.append(Card(i,suit))
        self.stack = Deck(cards)
        self.stack.shuffle()
        self.pile = Deck([self.stack.pop()])
        self.players = players
        self.display = display#if display is true then we'll display the card on top of the pile in each turn
        self.running = True#game status (running or finished)        
        
        
        for player in players:
            current_player_cards = []
            for i in range(CARDS_PER_PLAYER):#we'll initialize to each player 5 cards
                current_player_cards.append(self.stack.pop())                                         
            player.deck = Deck(current_player_cards)
 
        
    def step(self, player):  
        """
        player: the current player
        This method will excute a turn for the player given as a parameter
        """
        if self.display:
            print('Top of pile in ', player.name, ' turn: ', self.pile.cards[-1])
        if player.player == PLAYERS.HAREL_PLAYER:            
            move = player.move(self.pile.cards[-1].number)#this move takes number_on_pile
            
        elif player.player == PLAYERS.GREEDY_RANDOM_PLAYER:
            move = player.move()
            
        elif player.player == PLAYERS.SEMI_RANDOM_PLAYER:
            move = player.move(self.pile.cards[-1].number)
        
        elif player.player == PLAYERS.REAL_PLAYER:
            move = player.move()
            
        if move.move == MOVE.YANIV:
            self.running = False
            
        #we'll find the card to output to the player, either from the stack or the pile, according to his move
        elif move.move == MOVE.PILE:               
            player.deck.join([self.pile.pop()])                                       
            self.pile.join(move.input_cards)
            
        elif move.move == MOVE.STACK:            
            player.deck.join([self.stack.pop()])                    
            self.pile.join(move.input_cards) 
            
        #we'll keep the pile at size 1 by poping from the pile and inserting to the beggining of the stack
        while self.pile.size() > 1:
            self.stack.cards.insert(0, self.pile.pop(0))
            
        
    def get_game_leader(self):  
        """
        checks the leader of the game and returns him.
        """
        leader = self.players[0]
        for player in self.players[1:]:
            if player.get_score() < leader.get_score():
                leader = player
        return leader
        
    def print_full_game_status(self):
        """
        prints the full status of the game (the cards in the stack, pile and the cards in each player's hand)
        """
        print('stack cards: ')        
        print(self.stack)
        print('pile cards: ')
        print(self.pile)
        for player in self.players:
            print(player)
            
    def print_players_status(self):
        """
        prints the current player
        """
        for i,player in enumerate(self.players):
            print('player ', i)
            print(player)
   