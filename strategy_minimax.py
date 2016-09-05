from tippy_game_state import TippyGameState
from tippy_move import TippyMove
from strategy import Strategy


class StrategyMinimax(Strategy):
    """ Interface to suggest moves based on the Minimax Pruning algorithm. """

    # The special method __init__ is inherited by Strategy
    # and we believe that it is not appropriate to implement
    # a __str__ method since StrategyMinimax has no attributes
    # to display.

    def __repr__(self):
        """(StrategyMinimax) -> str

        Return a string representation of self that produces an
        equivalent StrategyMinimax when evaluated in Python.

        >>> minimax = StrategyMinimax()
        >>> minimax
        StrategyMinimax()
        """
        
        return "StrategyMinimax()"

    def __eq__(self, other):
        """(StrategyMinimax, object) -> bool

        Return whether self is equivalent to other.

        >>> minimax1 = StrategyMinimax()
        >>> minimax2 = StrategyMinimax()
        >>> minimax1 == minimax2
        True
        """
        
        return isinstance(other, StrategyMinimax)
    
    def suggest_move(self, state):
        """(StrategyMinimax, GameState) -> Move

        Return a move chosen based on the Minimax Pruning algorithm from those
        available for state.

        >>> minimax = StrategyMinimax()
        >>> state = TippyGameState('p1', 3, [['p2', None, None],\
        ['p2', 'p1', None], [None, 'p1', None]], {'p2': [TippyMove([0, 0]),\
        TippyMove([0, 1])], 'p1': [TippyMove([1, 2]), TippyMove([1, 1])]})
        >>> state.all_tippies = state.find_tippies()
        >>> minimax.suggest_move(state)
        TippyMove([2, 1])
        """
        
        self.maximizer = state.next_player
        return self.best_move(state)[1]        

    def best_move(self, state, alpha=-1, beta=-1):
        """(StrategyMinimax, GameState, number, number)
                                           -> list of float and Move

        Initialize value representing worst score for current state. Track
        best move available to the next player and opponent in the variables
        alpha and beta respectively. Continue maximizing score for current
        position, but stop search when when it exceeds -1 times the score
        we already know is gauranteed to the opponent.

        >>> minimax = StrategyMinimax()
        >>> state = TippyGameState('p1', 3, [['p2', None, None],\
        ['p2', 'p1', None], [None, 'p1', None]], {'p2': [TippyMove([0, 0]),\
        TippyMove([0, 1])], 'p1': [TippyMove([1, 2]), TippyMove([1, 1])]})
        >>> state.all_tippies = state.find_tippies()
        >>> minimax.maximizer = state.next_player
        >>> minimax.best_move(state)
        [1.0, TippyMove([2, 1])]
        """
        
        # Alpha is the current player's best encountered score on the path to
        # the root.
        # Beta is the opponent's best encoutered score on the path to the
        # root.

        # Initialize value as the worst possible score for this game position.
        value = -1.0
        move_list = state.possible_next_moves()
        
        # Base case
        if not move_list:
            return [state.outcome(), None]
        
        else:
            # Initialize value as the worst possible score for this game
            # position.
            value = -1.0
            gather = []
                
            # Current player's loop
            if state.next_player == self.maximizer:
                i = 0
                while i < len(move_list) and (value < beta * -1.0):
                    move = move_list[i]
                    score = (self.best_move(state.apply_move(move),
                                            alpha, beta)[0] * -1)
                    
                    # Track highest score
                    value = max([score, value])
                    alpha = max([alpha, value])
                        
                    gather.append([score, move])
                    i += 1
                    
            # Opponent's loop 
            else:
                i = 0 
                while i < len(move_list) and (value < alpha * -1.0):
                    move = move_list[i]
                    score = (self.best_move(state.apply_move(move),
                                            alpha, beta)[0] * -1)

                    value = max([score, value])
                    beta = max([beta, value])
                        
                    gather.append([score, move])
                    i += 1
            
            # Pick the highest score in gather along with the corresponding
            # move.
            move = gather[0]
            for item in gather:
                if move[0] < item[0]:
                    move = item
            
            return move


if __name__ == '__main__':
    import doctest
    doctest.testmod()

