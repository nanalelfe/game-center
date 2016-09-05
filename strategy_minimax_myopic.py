from tippy_game_state import TippyGameState
from tippy_move import TippyMove
from strategy import Strategy


class StrategyMinimaxMyopic(Strategy):
    """ Interface to suggest moves based on the Minimax Myopic algorithm. """

    # We believe that it is not appropriate to implement
    # a __str__ method since StrategyMinimaxMyopic has no
    # useful attributes to display.

    def __init__(self, n=3, interactive=False):
        """(StrategyMinimaxMyopic, int, bool) -> NoneType

        Initialize self to have a number of moves to look ahead n.
        
        >>> minimax = StrategyMinimaxMyopic()
        >>> minimax.n
        3
        """
        
        self.n = n
        
        if interactive:
            num = ''
            while not num.isdigit():
                num = input("Please enter a number of moves that you " +
                            "would like your opponent to look ahead: ")
            self.n = int(num)
 
    def __repr__(self):
        """(StrategyMinimaxMyopic) -> str

        Return a string representation of self that produces an
        equivalent StrategyMinimaxMyopic when evaluated in Python.

        >>> minimax = StrategyMinimaxMyopic()
        >>> minimax
        StrategyMinimaxMyopic(3)
        """
        
        return "StrategyMinimaxMyopic({})".format(repr(self.n))

    def __eq__(self, other):
        """(StrategyMinimaxMyopic, object) -> bool

        Return whether self is equivalent to other.

        >>> minimax1 = StrategyMinimaxMyopic(n=3)
        >>> minimax2 = StrategyMinimaxMyopic(n=4)
        >>> minimax1 == minimax2
        False
        """
        
        return (isinstance(other, StrategyMinimaxMyopic) and
                self.n == other.n)
    
    def suggest_move(self, state):
        """(StrategyMinimaxMyopic, GameState) -> Move

        Return a move chosen based on the Minimax Myopic algorithm from those
        available for state.

        >>> minimax = StrategyMinimaxMyopic(3)
        >>> state = TippyGameState('p1', 3, [['p2', None, None],\
        ['p2', 'p1', None], [None, 'p1', None]], {'p2': [TippyMove([0, 0]),\
        TippyMove([0, 1])], 'p1': [TippyMove([1, 2]), TippyMove([1, 1])]})
        >>> state.all_tippies = state.find_tippies()
        >>> minimax.suggest_move(state)
        TippyMove([2, 1])
        """
        
        return self.best_move(state, self.n)[1]

    def best_move(self, state, n):
        """(StrategyMinimaxMyopic, GameState, int) -> list of float and Move

        Look ahead n moves and if game state has not ended, then best move
        should evaluate rough outcome to provide a score for that game
        state. If the game has ended, evaluate actual outcome.
        
        >>> minimax = StrategyMinimaxMyopic(3)
        >>> state = TippyGameState('p1', 3, [['p2', None, None],\
        ['p2', 'p1', None], [None, 'p1', None]], {'p2': [TippyMove([0, 0]),\
        TippyMove([0, 1])], 'p1': [TippyMove([1, 2]), TippyMove([1, 1])]})
        >>> state.all_tippies = state.find_tippies()
        >>> minimax.best_move(state, 3)
        [1.0, TippyMove([2, 1])]
        """
        
        move_list = state.possible_next_moves()

        if not move_list:
            return [state.outcome(), None]
        elif n == 0:
            return [state.rough_outcome(), None]
        else:
            gather = []
            for move in move_list:
                score = (self.best_move(state.apply_move(move), n - 1)[0] * -1)
                gather.append([score, move])                   
            
            move = gather[0]              
            for item in gather:
                if move[0] < item[0]:
                    move = item
                    
            return move
            
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
 

