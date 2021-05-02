import os

NR_OF_PLAYERS           = 3
ADDED_ARMIES_PER_TURN   = 10

class Manager():
    '''
    Manages the game. Takes turns and communicates with the active player
    '''
    def __init__(self, nrOfPlayers):
        self.nrOfPlayers    = nrOfPlayers
        self.players        = self.init_players(nrOfPlayers)
        self.activePlayer   = self.players[0]

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(
"\n-----------------------------------\n\
         Active player: {}\
\n-----------------------------------\n\
            ".format(self.activePlayer.id))
       
        self.activePlayer.run()
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

    def run(self):
        Finished        = False
        self.ask_info()
        while not Finished:
            option = self.ask_option()
            if option == 1:
                self.ask_reinforce()
                Finished = True
            elif option == 2:  
                self.ask_attack_fromto()
                Finished = True
        self.ask_info()
        input("----- End of turn. Press a key to continue. -----")
    def ask_option(self):
        optionValid = False
        while not optionValid:
            try:
                userInput = int(input(\
"Choose an option:\
\n  1) Reinforce armies\
\n  2) Attack\
\n\t - "))\

                optionValid = True
            except Exception:
                print("no valid number given!")
                pass
        return userInput
    
    def ask_info(self):      
        print("\n")          
        for city in self.owned_cities():
            cityObj = Region.get_vertex(city)
            print("[Info] {} ==> {} armies".format(cityObj.name, cityObj.armies))
        print("\n")

    def ask_city_to_reinforce(self):
        validCity   = False
        while not validCity:
            try:
                inputCity = input("[Q] Which city to reinforce? Choose from: {}\n\t".format(self.owned_cities()))
                if inputCity in self.owned_cities():
                    validCity = True
                else:
                    print("[Error] Given city not owned by player")

            except Exception:
                print("[Error] No valid city given")
                pass
        return inputCity
    
    def ask_how_many_reinforcements(self, city, armiesLeftToAdd):
        validArmies = False
        while not validArmies:
            try:
                armiesToAdd = int(input("[Q] How many armies to add to {}?\n\t".format(city)))
                if armiesToAdd <= armiesLeftToAdd and armiesToAdd >= 0:
                    cityObj = Region.get_vertex(city)
                    cityObj.add_armies(armiesToAdd)
                    print("[Info] Successful. Armies now in {}: ".format(city), cityObj.armies)
                    validArmies = True
                else:
                    print("[Error] Invalid number of armies given. ")
            except Exception:
                print("[Error] Invalid input")
        return armiesToAdd

    def ask_reinforce(self):
        armies_left_to_add  = ADDED_ARMIES_PER_TURN
        while armies_left_to_add != 0:
            print("[Info] Reinforcements left: {}".format(armies_left_to_add))
            city = self.ask_city_to_reinforce()
            armies_left_to_add -= self.ask_how_many_reinforcements(city, armies_left_to_add)
               
        return 0 #

    def ask_attack_fromto(self):
        print("Owned cities: ", self.owned_cities()) 
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

    def owned_cities(self):
        return Region.get_players_vertices(self.id)

class Vertex:
    def __init__(self, name, ownedBy):
        self.name       = name
        self.ownedBy    = ownedBy
        self.adjacent   = {}
        self.armies     = 0
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
    
    def add_armies(self, armiesToAdd):
        self.armies += armiesToAdd


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
Region.add_vertex('Delfzijl', 0)  
Region.add_vertex('Leeuwarden', 1)
Region.add_vertex('Assen',  2)

Region.add_edge('Groningen', 'Delfzijl')
Region.add_edge('Groningen', 'Leeuwarden')
Region.add_edge('Groningen', 'Assen')

#print("vertex list: ", Region.get_vertex_list('Groningen'))
#print(Region.get_vertex('Assen'))
#print(Region.get_vertex_owner('Groningen'))

manager = Manager(NR_OF_PLAYERS)
while True:
    manager.run()
