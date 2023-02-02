from Board import Board
from Minimax_AlphaBeta import  back_to_start_state
from math import log

class Node:
    
    def __init__(self, board):
        self.board = board
        self.wins = 0
        self.draws = 0
        self.visits = 0
        self.parents = set()
        
    def add_parent(self, parent):
        if isinstance(parent, Board):
            parent_representation = parent.get_representation()
            self.parents.add(parent_representation)
        else:
            self.parents.add(parent)
            
    def update(self, player, winner):
        if player == winner:
            self.wins += 1
        elif winner == 0:
            self.draws += 1
        
        self.visits += 1
            
    def calculate_parents_visits(self):
        total_parents_visits = 0
        for parent in self.parents:
            total_parents_visits += parent.visits
        return total_parents_visits
<<<<<<< HEAD
    
    def calculate_winrate(self):
        if self.visits == 0:
            return 0
        
        return (self.wins + self.draws) / self.visits
            
    def calculate_uct(self, c):
        if self.visits == 0:
            return float('inf')
        
        winrate = (self.wins + self.draws) / self.visits #we count a draw as a win because, under best play, a draw is the best result one can get
        
        parents_visits = self.calculate_parents_visits()
        exploration = c * (log(parents_visits) / self.visits)**(1/2)
        
        return winrate + exploration

def choose_node_uct(board, player, dic_nodes_visited, c):
=======
            
    def calculate_uct(self, c = 2**(1/2)):
        if self.visits == 0:
            return 0
        
        winrate = (self.wins + self.draws) / self.visits #we count a draw as a win because, under best play, a draw is the best result one can get
        
        parents_visits = self.calculate_parents_visits
        exploration = c * (log(parents_visits) / self.visits)**(1/2)
        
        return winrate + exploration
    

def choose_node(board, player, dic_nodes_visited, c = 2**(1/2)):
>>>>>>> bd65c89a41f5b09a69863097e39f0d821492124a
    #dic has the board representation as key and the node as value
    
    if board.isGameOver():
        return None
    
    nb_moves_beginning = len(board.moves)
    best_uct = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            try:
                board.play(i, j, player)
                
<<<<<<< HEAD
                if dic_nodes_visited.get(board.get_representation()) != None: #the node has already been visited and exists in the dictionary
                    node = dic_nodes_visited.get(board.get_representation())
=======
                node = dic_nodes_visited.get(board.get_representation())
                if node != None: #the node has already been visited and exists in the dictionary
>>>>>>> bd65c89a41f5b09a69863097e39f0d821492124a
                    uct = node.calculate_uct(c)
                else:
                    node = Node(board.copy())
                    dic_nodes_visited[node.board.get_representation()] = node
                    uct = node.calculate_uct(c)
                    
                if uct >= best_uct:
                    best_uct = uct
                    best_move = (i, j, node)
                
                back_to_start_state(board, nb_moves_beginning)
            except:
                back_to_start_state(board, nb_moves_beginning)
    
    back_to_start_state(board, nb_moves_beginning)      
    return best_move

<<<<<<< HEAD
def choose_node_winrate(board, player, dic_nodes_visited):    
    if board.isGameOver():
        return None
    
    nb_moves_beginning = len(board.moves)
    best_winrate = -1
    best_move = None
    for i in range(3):
        for j in range(3):
            try:
                board.play(i, j, player)
                
                if dic_nodes_visited.get(board.get_representation()) != None: #the node has already been visited and exists in the dictionary
                    node = dic_nodes_visited.get(board.get_representation())
                    winrate = node.calculate_winrate()
                else:
                    winrate = 0
                    
                if winrate >= best_winrate:
                    best_winrate = winrate
                    best_move = (i, j, node)
                
                back_to_start_state(board, nb_moves_beginning)
            except:
                back_to_start_state(board, nb_moves_beginning)
    
    back_to_start_state(board, nb_moves_beginning)      
    return best_move

def play_move_in_simulation(board, player, dic_nodes_visited, path, c):
    
    try:
        parent = dic_nodes_visited[board.get_representation()]
    except:
        parent = Node(board.copy())
    
    try:
        (i, j, best_node) = choose_node_uct(board, player, dic_nodes_visited, c)
        try:
            board.play(i, j, player)
            path.append((best_node, player))
                
            best_node.add_parent(parent)
            
        except:
            pass
    except:
        pass

'''
def play_move_in_simulation(board, player, dic_nodes_visited, path, c):
    
    try:
        (i, j, best_node) = choose_node_uct(board, player, dic_nodes_visited, c)
=======
def play_move_in_simulation(board, player, dic_nodes_visited, path, c = 2**(1/2)):
    
    try:
        (i, j, best_node) = choose_node(board, player, dic_nodes_visited, c)
>>>>>>> bd65c89a41f5b09a69863097e39f0d821492124a
        try:
            board.play(i, j, player)
            path.append((best_node, player))
            
            try:
                parent = dic_nodes_visited[board.get_representation()]
            except:
                parent = Node(board.copy())
                
            best_node.add_parent(parent)
            
        except:
            pass
    except:
        pass
<<<<<<< HEAD
'''  
=======
    
>>>>>>> bd65c89a41f5b09a69863097e39f0d821492124a

def backpropagation(path, winner):
    for i in range(len(path)-1, -1, -1):
        node, player = path[i]
        node.update(player, winner)
            
    
<<<<<<< HEAD
def make_complete_simulation(board, player, dic_nodes_visited, c):
=======
def make_complete_simulation(board, player, dic_nodes_visited, c = 2**(1/2)):
>>>>>>> bd65c89a41f5b09a69863097e39f0d821492124a
    path = []
    
    while not board.isGameOver():
        play_move_in_simulation(board, player, dic_nodes_visited, path, c)
        if player == -1:
            player = 1
        else:
            player = -1
    
    winner = board.gameState
    backpropagation(path, winner)
 
def play_mcts(board, player, nb_simulations, c = 2**(1/2)):
    dic_nodes_visited = {}
    
<<<<<<< HEAD
    for i in range(nb_simulations):
        copy_board = board.copy()
        make_complete_simulation(copy_board, player, dic_nodes_visited, c)
        copy_board = None
        #print(f"Simulation {i} ended -> len(dic) = {len(dic_nodes_visited)}")
        
    #print('len dic = ' + str(len(dic_nodes_visited)))
    #print('len moves = ' + str(len(board.moves)))
    
    (i, j, _) = choose_node_winrate(board, player, dic_nodes_visited)
    board.play(i, j, player)
    return dic_nodes_visited
    


=======
    for _ in range(nb_simulations):
        copy_board = board.copy()
        make_complete_simulation(copy_board, player, dic_nodes_visited, c)
    
    #print('len dic = ' + str(len(dic_nodes_visited)))
    #print('len moves = ' + str(len(board.moves)))
    
    (i, j, _) = choose_node(board, player, dic_nodes_visited, c)
    board.play(i, j, player)
    
>>>>>>> bd65c89a41f5b09a69863097e39f0d821492124a
b = Board()
b.play(0, 0, 1)
b.play(1, 1, -1)

<<<<<<< HEAD
d = play_mcts(b, 1, 9, c = 4)
print('done')
import pickle

with open('./Code/d.pickle', 'wb') as handle:
    pickle.dump(d, handle)
=======
dic_nodes_visited = {}
choose_node(b, 1, dic_nodes_visited)
make_complete_simulation(b, 1, dic_nodes_visited)  
b.display()
print(dic_nodes_visited)
>>>>>>> bd65c89a41f5b09a69863097e39f0d821492124a
