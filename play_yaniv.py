from game_manager import GameManager
from players import PLAYERS, GreedyRandomPlayer, HarelPlayer, SemiRandomPlayer, RealPlayer
import pickle as pkl




if __name__ == "__main__":
    ###LOADING tTHE RL PLAYER:
    pickel_in =  open("harel.pickle", "rb")
    harel = pkl.load(pickel_in)
    ######################
    
    grplayer = GreedyRandomPlayer(0.5, 'grplayer_name')
    smplayer = SemiRandomPlayer('srplayer_name')
    rplayer = RealPlayer("Assaf")#the user will play this player
    
    #If you want to see harel's card, uncomment the line below
    #harel.display=True
    
    players = [grplayer, smplayer, rplayer, harel]


    gm = GameManager(players, True)
    while gm.running==True:
        for player in players:
            gm.step(player)
            if gm.running == False:            
                print("The game has ended, winner is: ", gm.get_game_leader().name)
                break

