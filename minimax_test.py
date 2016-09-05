import subtract_square_state as sss
import subtract_square_move as ssm
import strategy_minimax as sm
import strategy_minimax_prune as mp
import strategy_minimax_memoize as mm
import strategy_minimax_myopic as my
import unittest as ut

# winning moves for given totals
WINNERS = {25:[ssm.SubtractSquareMove(25)],
           27:[ssm.SubtractSquareMove(25)],
           28:[ssm.SubtractSquareMove(16)],
           29:[ssm.SubtractSquareMove(9)]}


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
        #self.strat = sm.StrategyMinimax()
        self.strat = mp.StrategyMinimaxPrune()
        #self.strat = mm.StrategyMinimaxMemoize()
        #self.strat = my.StrategyMinimaxMyopic()
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

if __name__ == '__main__':
    ut.main(exit=False)

        
        
