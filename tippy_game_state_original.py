from game_state import GameState
from tippy_move import TippyMove
from strategy_minimax_memoize import StrategyMinimaxMemoize
from strategy_minimax import StrategyMinimax
from copy import deepcopy
import time


class TippyGameState(GameState):
    """ The state of the Tippy game. """

    def __init__(self, p, n=3, board=[], player_to_move={'p1': [], 'p2': []},
                 all_tippies=None, interactive=False):
        """(TippyGameState, str, int, list of list of object, dict of {str:
            list of Tippy Moves}, list of list of TippyMove, bool) -> NoneType

        Initialize self to have a next_player p, a board of size n, a board, a
        player_to_move which stores all the moves of the players,
        the list of all possible tippy moves all_tippies and the instructions
        of the game. 

        >>> tippygame = TippyGameState('p1')
        >>> tippygame.next_player
        'p1'
        >>> tippygame.n
        3
        >>> tippygame.board
        [[None, None, None], [None, None, None], [None, None, None]]
        >>> tippygame.player_to_move == {'p1': [], 'p2': []}
        True
        """
 
        GameState.__init__(self, p, interactive=False)

        if interactive:
            n = input('Enter the size n of an nxn grid of' +
                      ' your choice: ')
            while not n.isdigit() or int(n) < 3:
                n = input('Please enter a valid n greater than 2: ')
            n = int(n)
            
        self.n = n
          
        self.instructions = """
        Tippy is a variation of tic-tac-toe. Players take turns
        placing either an X or an O on an n x n grid (where n is
        at least 3), with the goal of forming a tippy. In this
        example below, in a 3x3 grid, X has won by forming a tippy:
        
                  0   1   2 
                -------------
            0	| X | X | O |
                -------------
            1	| O | X | X |
                -------------
            2	| O |   |   |
                -------------

        """
        
        self.board = deepcopy(board)

        # If the board is empty (the game just started), then
        # create a new board and generate all the possible tippies
        # available to board depending on size n:
        
        if self.board == []:
            self.create_new_board()
            all_tippies = self.find_tippies()

        self.all_tippies = all_tippies
        
        self.player_to_move = player_to_move
        
        if self.all_tippies is not None:
            if not self.possible_next_moves():
                self.over = True
        
    def __repr__(self):
        """(TippyGameState) -> str

        Return a string representation of self that also produces an
        equivalent TippyGameState when evaluated in Python.

        >>> tippygame = TippyGameState('p1')
        >>> tippygame.all_tippies = None
        >>> eval(repr(tippygame)) == TippyGameState('p1', 3, \
        [[None, None, None],[None, None, None], [None, None, None]],\
        {'p2': [], 'p1': []}, None)
        True
        """
        # The output of this method is really long!
        
        return "TippyGameState({}, {}, {}, {}, {})".\
               format(repr(self.next_player),
                      repr(self.n),
                      repr(self.board),
                      repr(self.player_to_move),
                      repr(self.all_tippies))

    def __str__(self):
        r"""(TippyGameState) -> str
    
        Return a convenient string representation of self.
    
        >>> tippygame = TippyGameState('p1')
        >>> y = '\n\t  0   1   2 \n\t-------------\n    0\t|   |   |   '
        >>> y += '|\n\t-------------\n    1\t|   |   |   |\n\t-------------'
        >>> y += '\n    2\t|   |   |   |\n\t-------------\n'
        >>> y == str(tippygame) 
        True
        """
        # Comparing the print output is not feasable. 
        
        display = '\n\t'
        for j in range(self.n): 
            display += ('  {0} '.format(j))
    
        display += '\n\t-' + '----' * self.n + '\n'
        i = 0 
        for x in self.board:
            display += ('    ' + str(i) + '\t')
            for y in x:
                if y is None:
                    piece = '   '
                elif y == 'p2':
                    piece = ' O '
                else: 
                    piece = ' X '
                display += ('|' + piece)
            display += '|\n\t-' + '----' * self.n + '\n'
            i += 1
            
        return display  

    def __eq__(self, other):
        """(TippyGameState, object) -> bool

        Return whether self is equivalent to other.

        >>> tippygame = TippyGameState('p1')
        >>> other1 = TippyGameState('p2')
        >>> tippygame == other1
        False
        >>> other2 = TippyGameState('p1')
        >>> tippygame == other2
        True
        """
        
        return (isinstance(other, TippyGameState) and
                self.next_player == other.next_player and
                self.n == other.n and
                self.board == other.board and
                self.player_to_move == other.player_to_move and
                self.all_tippies == other.all_tippies)
    
    def create_new_board(self): 
        """(TippyGameState) -> Nonetype
        
        Create board of size n x n for self at initialization.
        """
        
        for y in range(self.n):
            coord_list = []
            for x in range(self.n):
                coord_list.append(None)
            self.board.append(deepcopy(coord_list))
            
    def get_move(self):
        """(TippyGameState) -> TippyMove

        Prompt user and return move.
        """

        # Cannot provide docstring examples for get_move because this method
        # requires input from the user.
        
        x = input('Pick the x coordinate of a move: ')
        y = input('Pick the y coordinate of a move: ')

        return TippyMove([int(x), int(y)])
    
    def apply_move(self, tp_move):
        """(TippyGameState, TippyMove) -> TippyGameState

        Return the new TippyGameState reached by applying move to self.

        >>> tippy = TippyGameState('p1')
        >>> tippy1 = tippy.apply_move(TippyMove([1,1]))
        >>> tippy2 = TippyGameState('p2', n=3)
        >>> tippy2.board = [[None, None, None],\
        [None, 'p1', None], [None, None, None]]
        >>> tippy2.player_to_move = {'p2': [],\
        'p1': [TippyMove([1, 1])]}
        >>> tippy1 == tippy2
        True
        """

        if tp_move in self.possible_next_moves():
            
            board_copy = deepcopy(self.board)
            # Adds players move onto board as player's name (ie 'p1' or 'p2')
            board_copy[tp_move.move[1]][tp_move.move[0]] = self.next_player  
            
            player_to_move_copy = deepcopy(self.player_to_move)
            # Keep track of move played
            player_to_move_copy[self.next_player].append(tp_move)
            
            # Pass all pertinent information onto new state
            # This includes board size, board data, moves played 
            # Also switches next_player to opponent
            
            return TippyGameState(self.opponent(), n=self.n,
                                  board=board_copy, 
                                  player_to_move=player_to_move_copy,
                                  all_tippies=self.all_tippies)
        else:
            return None            
            
    def winner(self, player):
        """(TippyGameState, str) -> bool

        Return True iff the game is over and player has won. 

        >>> tippygame1 = TippyGameState('p1')
        >>> tippygame1.winner('p1')
        False
        >>> tippygame2 = TippyGameState('p2')
        >>> tippygame2.board = [['p1', 'p1', None],\
        ['p2', 'p1', 'p1'], ['p2', 'p2', None]]
        >>> tippygame2.player_to_move = {'p1': [TippyMove([1, 1]),\
        TippyMove([0, 0]), TippyMove([1, 0]), TippyMove([2, 1])],\
        'p2': [TippyMove([0, 2]), TippyMove([0, 1]), TippyMove([1, 2])]}
        >>> tippygame2.winner('p1')
        True
        >>> tippygame2.winner('p2')
        False
        """
        
        lst = []

        for route in self.all_tippies:
            lst.append(all([coord in self.player_to_move[player] 
                            for coord in route]))
        return any(lst)

    def possible_next_moves(self):
        """(TippyGameState) -> list of TippyMove

        Return a (possibly empty) list of moves that are legal
        from the present state.

        >>> tippygame = TippyGameState('p1')
        >>> tippygame.possible_next_moves() == [TippyMove([0, 0]),\
        TippyMove([1, 0]), TippyMove([2, 0]), TippyMove([0, 1]),\
        TippyMove([1, 1]), TippyMove([2, 1]), TippyMove([0, 2]),\
        TippyMove([1, 2]), TippyMove([2, 2])]
        True
        """
        
        possible_moves = []

        if self.winner('p1') or self.winner('p2'):
            return []
        else:
            for x in range(self.n):
                for y in range(self.n):
                    if self.board[x][y] is None:
                        possible_moves.append(TippyMove([y, x]))
            return possible_moves

    def rough_outcome(self):
        """(TippyGameState) -> float

        Return an estimate in internal [LOSE, WIN, DRAW] of best outcome
        next_player can guarantee from state self.

        >>> tippygame1 = TippyGameState('p1')
        >>> tippygame1.rough_outcome()
        0.0
        >>> tippygame2 = TippyGameState('p2', 3)
        >>> tippygame2.board = [['p1', 'p1', None], ['p2', 'p1', 'p1'], \
        ['p2', 'p2', None]] 
        >>> tippygame2.player_to_move = {'p1': [TippyMove([1, 1]), \
        TippyMove([0, 0]), TippyMove([1, 0]), TippyMove([2, 1])], \
        'p2': [TippyMove([0, 2]), TippyMove([0, 1]), TippyMove([1, 2])]}
        >>> tippygame2.all_tippies = tippygame2.find_tippies()
        >>> tippygame2.rough_outcome()
        -1.0
        """

        current_player_moves = self.player_to_move[self.next_player]
        opponent_moves = self.player_to_move[self.opponent()]
        
        # list of possible tippy routes available to the current player:
        current_player_routes = []
        # list of possible tippy routes available to the opponent:
        opponent_routes = []

        # Loop over all the possible tippy routes. If at least
        # one route is being completed by the current player and
        # the route isn't blocked by the opponent, append the route to
        # the current player's route list.
        # Complete similar task for the opponent.

        for route in self.all_tippies:
            if (any([x in route for x in current_player_moves]) and 
                    all([item not in opponent_moves for item in route])):
                current_player_routes.append(route)
            elif (any([x in route for x in opponent_moves]) and
                  all([item not in current_player_moves for item in route])):
                opponent_routes.append(route)

        # Check which player has more tippy routes, and return a
        # score accordingly. 

        if len(current_player_routes) > len(opponent_routes):
            return TippyGameState.WIN
        elif len(opponent_routes) > len(current_player_routes):
            return TippyGameState.LOSE
        else:
            return TippyGameState.DRAW

    def find_tippies(self):
            """(FindTippy) -> Nonetype
            
            Go through all tippy routes on every single coord in self.board. 
            Search for all possible tippy combinations, append them to 
            self.all_tippies. Exclude any duplicate tippies. """

            tippies = []
            

            for x in range(len(self.board)):
                for y in range(len(self.board[x])):
                    coords = [x,y]
                    
                    tippy_route = [[self.up, self.right, self.up],
                                    [self.up, self.left, self.up],
                                    [self.down, self.right, self.down],
                                    [self.down, self.left, self.down],
                                    [self.right, self.up, self.right],
                                    [self.right, self.down, self.right],
                                    [self.left, self.up, self.left],
                                    [self.left, self.down, self.left]]
                    
                    all_routes = [] 
                     
                    for route in tippy_route:
                        m = coords.copy()
                        get_route = ([coords] +
                                     [c(m).copy() for c in route]).copy()
                        if not ([] in get_route):
                            get_route.sort()
                            new_route = []
                            for i in range(len(get_route)):
                                new_route.append(TippyMove(get_route[i]))
                            all_routes += [new_route]
                            
                    possible_routes = all_routes

                    for routes in possible_routes:
                        if not routes in tippies:
                            tippies +=  [routes]
            return tippies

    
    def left(self, coord):
        """(TippyGameState, list of int) -> list of int

        Move the coordinate coord one move to the left.

        >>> tippygame = TippyGameState('p1')
        >>> tippygame.left([1, 1])
        [0, 1]
        """
        
        if 0 <= (coord[0] - 1) < self.n:
            coord[0] -= 1
            return coord
        return []
    
    def right(self, coord):
        """(TippyGameState, list of int) -> list of int

        Move the coordinate coord one move to the right.

        >>> tippygame = TippyGameState('p1')
        >>> tippygame.right([1, 1])
        [2, 1]
        """

        if 0 <= (coord[0] + 1) < self.n:
            coord[0] += 1
            return coord
        return []    
    
    def down(self, coord): 
        """(TippyGameState, list of int) -> list of int

        Move the coordinate coord one move down.

        >>> tippygame = TippyGameState('p1')
        >>> tippygame.down([1, 1])
        [1, 2]
        """
 
        if 0 <= (coord[1] + 1) < self.n:
            coord[1] += 1
            return coord
        return []        
    
    def up(self, coord):
        """(TippyGameState, list of int) -> list of int

        Move the coordinate coord one move up.

        >>> tippygame = TippyGameState('p1')
        >>> tippygame.up([1, 1])
        [1, 0]
        """

        if 0 <= (coord[1] - 1) < self.n:
            coord[1] -= 1
            return coord
        return []
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
# Pruning test    
    print()
    t = TippyGameState('p1', n=4) 
    track = time.time()
    print ("STARTING MINIMAX TEST 1:")
    
    s = StrategyMinimax()
    x = s.suggest_move(t)
    
    print('Suggested Move: ', x)
    
    print ("The process took: " + str(time.time() - track) + " seconds")
    
# Memoization test

    #print()
    #t = TippyGameState('p1', n=3) 
    #track = time.time()
    #print ("STARTING MINIMAX TEST 1:")
    
    #s = StrategyMinimaxMemoize()
    #x = s.suggest_move(t)
    
    #print('Suggested Move: ', x)
    
    #print ("The process took: " + str(time.time() - track) + " seconds")
    
