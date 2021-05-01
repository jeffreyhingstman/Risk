
NR_OF_PLAYERS   = 4

class Manager():
    '''
    Manages the game. Takes turns and communicates with the active player
    '''
    def __init__(self, nrOfPlayers):
        self.nrOfPlayers    = nrOfPlayers
        self.players        = self.init_players(nrOfPlayers)
        self.activePlayer   = self.players[0]

    def run(self):
        print(
"\n-----------------------------------\n\
         Active player: {}\
\n-----------------------------------\n\
            ".format(self.activePlayer.id))
       
        self.activePlayer.run()
        if self.activePlayer.Finished == True:
            self.next_player()

    def next_player(self):
        playerNr = self.activePlayer.id
        if self.activePlayer.id >= len(self.players) - 1:
            self.activePlayer = self.players[0]
        else:
            self.activePlayer = self.players[playerNr + 1]

    @classmethod
    def init_players(self, NrOfPlayers):
        Players = []
        for idx in range(NrOfPlayers):
            Players.append(Player(idx))
        return Players

class Player():
    '''
    Keeps track of a player's info, and what it should do in a turn
    '''
    def __init__(self, id):
        self.armies     = 10
        self.id         = id
        self.Finished   = False

    def run(self):
        self.Finished = False
        strategy = self.ask_strategy()
        print("Player {} chose strategy: {}".format(self.id, strategy))

        if strategy == 1:   # attack strategy
            self.ask_attack_fromto()

        self.Finished = True

    def ask_strategy(self):
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
    
    def ask_attack_fromto(self):
        print("Owned cities: ", Region.get_players_vertices(self.id)) 
        validFrom   = False
        validTo     = False
        validFromTo = False
        try:
            while not validFrom:
                frm = input("From which city do you want to attack: \n\t--> ")
                if Region.get_vertex_owner(frm) != self.id:
                    print("Attempting to attack from city that is not owned by you!") 
                else:
                    validFrom = True
            while not (validTo and validFromTo):
                print("Attackable cities from {}: ".format(frm), Region.get_vertex_list(frm))
                to = input("Which city do you want to attack: \n\t--> ")
                if Region.get_vertex_owner(to) == self.id:
                    print("Attempting to attack city that is not adjacent")
                else:
                    validTo = True
                if to not in Region.get_vertex_list(frm):
                    print("Attempting to attack city that is not adjacent")
                else:
                    validFromTo = True
            print("Player {} attacks {} from {}".format(self.id, to, frm))

        except Exception:
            print("no valid city given!")
            pass
        return frm, to


    def check_attack_combi(self, frm, to):
        if to not in Region.get_vertex_list(frm):
            print("Attempting to attack city that is not adjacent")
            return False
        else:
            return True

class Vertex:
    def __init__(self, name, ownedBy):
        self.name = name
        self.ownedBy = ownedBy
        self.adjacent = {}
    def __str__(self):
        return str(self.name) + ' adjacent: ' + str([x.name for x in self.adjacent])

    def add_neighbor(self, neighbor):
        self.adjacent[neighbor] = True

    def get_connections(self):
        return self.adjacent.keys()  

    def get_name(self):
        return self.name

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node, ownedBy):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node, ownedBy)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, name):
        if name in self.vert_dict:
            return self.vert_dict[name]
        else:
            return None
    
    def get_vertex_list(self, name):
        if name in self.vert_dict:
            return [x.name for x in self.vert_dict[name].adjacent]

    def get_vertex_owner(self, name):
        if name in self.vert_dict:
            return self.vert_dict[name].ownedBy 
        else:
            return None
    
    def get_players_vertices(self, player):
        playersVertices = []
        for name in self.vert_dict:
            vertex = self.vert_dict[name]
            if vertex.ownedBy == player:
                playersVertices.append(name)
        return playersVertices

    def add_edge(self, frm, to):
        self.vert_dict[frm].add_neighbor(self.vert_dict[to])
        self.vert_dict[to].add_neighbor(self.vert_dict[frm])

    def get_vertices(self):
        return self.vert_dict.keys()

Region = Graph()

Region.add_vertex('Groningen', 0)  
Region.add_vertex('Leeuwarden', 1)
Region.add_vertex('Assen',  2)

Region.add_edge('Groningen', 'Leeuwarden')
Region.add_edge('Groningen', 'Assen')

print("vertex list: ", Region.get_vertex_list('Groningen'))
print(Region.get_vertex('Assen'))
print(Region.get_vertex_owner('Groningen'))

manager = Manager(NR_OF_PLAYERS)
while True:
    manager.run()
