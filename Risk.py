
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

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor):
        self.adjacent[neighbor] = True

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to])
        self.vert_dict[to].add_neighbor(self.vert_dict[frm])

    def get_vertices(self):
        return self.vert_dict.keys()

Region = Graph()

Region.add_vertex('Groningen')  
Region.add_vertex('Leeuwarden')
Region.add_vertex('Assen')

Region.add_edge('Groningen', 'Leeuwarden')
Region.add_edge('Groningen', 'Assen')

print(Region.get_vertex('Assen'))

manager = Manager(NR_OF_PLAYERS)
while False:
    manager.run()
