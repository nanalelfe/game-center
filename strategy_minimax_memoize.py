from tippy_game_state import TippyGameState
from tippy_move import TippyMove
from strategy import Strategy


class StrategyMinimaxMemoize(Strategy):
    """ Interface to suggest moves based on the Minimax Memoize algorithm."""
    
    # We believe that it is not appropriate to implement
    # a __str__ method since StrategyMinimaxMemoize has no useful attributes
    # to display.

    def __init__(self, interactive=False, state_holder={}):
        """(StrategyMinimaxMemoize, bool, dict) -> NoneType

        Initialize self to a state holder state_holder,
        which stores all the states that self has encountered so far.

        >>> minimax = StrategyMinimaxMemoize({})
        >>> minimax.state_holder
        {}
        """
        
        self.state_holder = state_holder

    def __repr__(self):
        """(StrategyMinimaxMemoize) -> str

        Return a string representation of self that produces an
        equivalent StrategyMinimaxMemoize when evaluated in Python.

        >>> minimax = StrategyMinimaxMemoize()
        >>> minimax
        StrategyMinimaxMemoize({})
        """
        
        return "StrategyMinimaxMemoize({})".format(self.state_holder)

    def __eq__(self, other):
        """(StrategyMinimaxMemoize, object) -> bool

        Return whether self is equivalent to other.

        >>> minimax1 = StrategyMinimaxMemoize({})
        >>> minimax2 = StrategyMinimaxMemoize({})
        >>> minimax1 == minimax2
        True
        """
        
        return (isinstance(other, StrategyMinimaxMemoize) and
                self.state_holder == other.state_holder)

    def suggest_move(self, state):
        """(StrategyMinimaxMemoize, GameState) -> Move

        Return a move chosen based on the Minimax Memoize
        algorithm from those available for state.

        >>> minimax = StrategyMinimaxMemoize({})
        >>> state = TippyGameState('p1', 3, [['p2', None, None],\
        ['p2', 'p1', None], [None, 'p1', None]], {'p2': [TippyMove([0, 0]),\
        TippyMove([0, 1])], 'p1': [TippyMove([1, 2]), TippyMove([1, 1])]})
        >>> state.all_tippies = state.find_tippies()
        >>> minimax.suggest_move(state)
        TippyMove([2, 1])
        """
        
        return self.best_move(state)[1]
    
    def best_move(self, state):
        """(StrategyMinimaxMemoize, GameState) -> list of float and Move

        Apply minimax algorithm. When a game state is first encountered, 
        it is logged into the dictionary self.state_holder along with its 
        value. If the same state is subsequently encountered, the value
        stored in the  dictionary is return instead.

        >>> minimax = StrategyMinimaxMemoize({})
        >>> state = TippyGameState('p1', 3, [['p2', None, None],\
        ['p2', 'p1', None], [None, 'p1', None]], {'p2': [TippyMove([0, 0]),\
        TippyMove([0, 1])], 'p1': [TippyMove([1, 2]), TippyMove([1, 1])]})
        >>> state.all_tippies = state.find_tippies()
        >>> minimax.best_move(state)
        [1.0, TippyMove([2, 1])]
        """

        move_list = state.possible_next_moves()
     
        if not move_list:
            return [state.outcome(), None]
        else:
            gather = []
            for move in move_list:
                new_state = state.apply_move(move)
                if ((str(new_state), new_state.next_player) not in
                        self.state_holder):
                    score = (self.best_move(new_state)[0] * -1)
                    gather.append([score, move])
                    self.state_holder[(str(new_state),
                                       new_state.next_player)] = (score * -1)

                else:
                    gather.append([self.state_holder[
                        (str(new_state), new_state.next_player)] * -1, move])

        move = gather[0]
        for item in gather:
            if move[0] < item[0]:
                move = item
                
        return move


if __name__ == '__main__':
    import doctest
    doctest.testmod()

