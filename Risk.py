
NR_OF_PLAYERS   = 4

class Manager():
    '''
    Manages the game. Takes turns and communicates with the active player
    '''
    def __init__(self, nrOfPlayers):
        self.nrOfPlayers  = nrOfPlayers
        self.players = self.init_players(nrOfPlayers)
        self.activePlayer = self.players[0]

    def run(self):
        print(
"\n-------------------------\n\
    Active player: {}\
\n--------------------------\n\
            ".format(self.activePlayer.Number))
       
        self.activePlayer.run()
        if self.activePlayer.Finished == True:
            self.next_player()

    def next_player(self):
        playerNr = self.activePlayer.Number
        if self.activePlayer.Number >= len(self.players) - 1:
            self.activePlayer = self.players[0]
        else:
            self.activePlayer = self.players[playerNr + 1]

    @classmethod
    def init_players(self, NrOfPlayers):
        Players = []
        for number in range(NrOfPlayers):
            Players.append(Player(number))
        return Players

class Player():
    '''
    Keeps track of a player's info, and what it should do in a turn
    '''
    def __init__(self, number):
        self.armies     = 10
        self.Number     = number
        self.Finished   = False

    def run(self):
        self.Finished = False
        strategy = self.read_input()
        print("Player {} chose strategy: {}".format(self.Number, strategy))
        self.Finished = True

    def read_input(self):
        strategyValid = False
        while strategyValid == False:
            try:
                userInput = int(input(\
"Choose a strategy:\
\n1) attack\
\n2) add troops\n\t--> "))  # 1=attack, 2=add troops

                strategyValid = True
            except Exception:
                print("no valid number given!")
                pass
        return userInput

class territory():
    def __init__(self, name):
        self.name = name


manager = Manager(NR_OF_PLAYERS)
while True:
    manager.run()
