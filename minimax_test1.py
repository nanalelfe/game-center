import subtract_square_state as sss
import subtract_square_move as ssm
import strategy_minimax as sm
import strategy_minimax_memoize as mm
import strategy_minimax_prune as mp
import tippy_game_state as tgs
import tippy_move as tm
import unittest as ut

# Subtract Square winning moves for given totals
WINNERS = {25:[ssm.SubtractSquareMove(25)],
           27:[ssm.SubtractSquareMove(25)],
           28:[ssm.SubtractSquareMove(16)],
           29:[ssm.SubtractSquareMove(9)],
           33:[ssm.SubtractSquareMove(16)],
           41:[ssm.SubtractSquareMove(36)],}


class MinimaxSubtractSquare(ut.TestCase):
    ''' tests of minimax on subtract square 

    Each test verifies that some winning move is returned
    from a winning position, with a correct choice being
    awarded the odds that it would succeed randomly.

    The product of all the odds is 0.0016 for each player, or
    a probability of less than 1% that all tests 
    could randomly succeed.
    '''

    def setUp(self, p='p1', total=8):
        ''' Set up some tools. '''
        self.strat = sm.StrategyMinimax()
#        self.strat = sm.StrategyMinimaxMemoize()
#        self.strat = sm.StrategyMinimaxPrune()
        self.sub = sss.SubtractSquareState(p, current_total=total)
        self.mv = self.strat.suggest_move(self.sub)
        self.total = total
        self.error = ('Wrong move: {},  for SubtractSquare({})'.
                      format(str(self.mv), self.total))
    
    def tearDown(self):
        ''' Clean up.'''
        self.sub, self.strat, self.mv = None, None, None
        self.total, self.error = None, None

    def testTwentyFiveP1(self):
        ''' Winning start on 25, p1: 0.2 '''
        self.setUp('p1', 25)
        assert self.mv in WINNERS[25], self.error

    def testTwentyFiveP2(self):
        ''' Winning start on 25, p2: 0.2 '''
        self.setUp('p2', 25)
        assert self.mv in WINNERS[25], self.error

    def testTwentySevenP1(self):
        ''' Winning start on 27, p1: 0.2 '''
        self.setUp('p1', 27)
        assert self.mv in WINNERS[27], self.error

    def testTwentySevenP2(self):
        ''' Winning start on 27, p2: 0.2 '''
        self.setUp('p2', 27)
        assert self.mv in WINNERS[27], self.error

    def testTwentyEightP1(self):
        ''' Winning start on 28, p1: 0.2 '''
        self.setUp('p1', 28)
        assert self.mv in WINNERS[28], self.error

    def testTwentyEightP2(self):
        ''' Winning start on 28, p2: 0.2 '''
        self.setUp('p2', 28)
        assert self.mv in WINNERS[28], self.error

    def testTwentyNineP1(self):
        ''' Winning start on 29, p1: 0.2 '''
        self.setUp('p1', 29)
        assert self.mv in WINNERS[29], self.error
        
    def testTwentyNineP2(self):
        ''' Winning start on 29, p2: 0.2 '''
        self.setUp('p2', 29)
        assert self.mv in WINNERS[29], self.error

    def testThirtyThreeP1(self):
        ''' Winning start on 33, p1: 0.2 '''
        self.setUp('p1', 33)
        assert self.mv in WINNERS[33], self.error

    def testThirtyThreeP2(self):
        ''' Winning start on 33, p2: 0.2 '''
        self.setUp('p2', 33)
        assert self.mv in WINNERS[33], self.error

# These tests take *really* long without optimization
#
    def testFortyOneP1(self):
        ''' Winning start on 41, p1: 0.16 '''
        self.setUp('p1', 41)
        assert self.mv in WINNERS[41], self.error
#
    def testFortyOneP2(self):
        ''' Winning start on 41, p2: 0.16 '''
        self.setUp('p2', 41)
        assert self.mv in WINNERS[41], self.error

class testMinimaxTippyWin(ut.TestCase):
    ''' tests of winning move for minimax on tippy
    '''

    def setUp(self, p='p1', n=3):
        ''' set up some tools '''
        self.strat = mm.StrategyMinimaxMemoize()
        self.tip = tgs.TippyGameState(p)
        self.mv = self.strat.suggest_move(self.tip)
        self.error = ('Wrong move: {}, for tippy: {}'.format(self.mv, self.tip))

    def tearDown(self):
        ''' prepare a blank slate '''
        self.strat, self.tip, self.mv = None, None, None
        self.error = None

    def testTippy3P1(self):
        ''' Winning start on 3x3 tippy, p1: 0.11 '''
        self.setUp('p1', 3)
        assert self.mv == tm.TippyMove([1, 1]), self.error
    


if __name__ == '__main__':
    ut.main(exit=False)

        
        
