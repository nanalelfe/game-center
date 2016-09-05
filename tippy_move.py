from move import Move
import pep8


class TippyMove(Move):
    """A move in the game of Tippy."""

    def __init__(self, move):
        """(TippyMove, list of int) -> NoneType

        Initialize a new TippyMove for placing move on board.

        >>> tippymove = TippyMove([1, 1])
        >>> tippymove.move
        [1, 1]
        """
        
        self.move = move

    def __repr__(self):
        """(TippyMove) -> str

        Return a string representation of TippyMove that produces
        an equivalent TippyMove when evaluated in Python.

        >>> tippymove = TippyMove([1, 1])
        >>> tippymove
        TippyMove([1, 1])
        """
        return "TippyMove({})".format(repr(self.move))

    def __str__(self):
        """(TippyMove) -> str

        Return a convenient string representation of TippyMove.

        >>> tippymove = TippyMove([1, 1])
        >>> print(tippymove)
        [1, 1]
        """
        return str(self.move)

    def __eq__(self, other):
        """(TippyMove) -> bool

        Return whether self is equivalent to other.

        >>> tippymove1 = TippyMove([1, 1])
        >>> tippymove2 = TippyMove([2, 2])
        >>> tippymove1 == tippymove2
        False
        """
        return (isinstance(other, TippyMove) and
                self.move == other.move)

if __name__ == '__main__':
    pep8.Checker('tippy_move.py', ignore=('W2', 'W3')).check_all()
    import doctest
    doctest.testmod()