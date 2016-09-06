#Game Center: Tippy Game, Subtract Square and Minimax AI

A game center containing 2 zero-sum games; Tippy Game, a variation of Tic-Tac-Toe, and Subtract Square, a game consisting of subtracting a number until it becomes 0. The human player has the choice to face an AI based on the Minimax Algorithm.

##Tippy Game 
Tippy is a variation of tic-tac-toe. Players take turns placing either an X or an O on an nxn grid (where n is at least 3, and is specified by the player before game-start). 
Tippies correspond to the Z and S tetrominos (aka tetriminos) from tetris. On a 3 x 3 grid there are 8 possible tippies, and more on a larger grid. 

Unlike Tic-tac-toe there is a winning tippy strategy for whichever player moves first. In other words, if the first player always chooses the **best move**, her or she will always win the game of tippy. Compare this to the situation in tic-tac-toe where if both players choose the best possible move, the result is always a tie. 

##Subtract a Square Game 
Subtract a Square is a game which is played via the terminal. It is a two-player, turn-based game. A positive whole number is randomly chosen as the starting value by the program. The player whose turn it is chooses some square of a positive whole number (such as 1, 4, 9, 16,...) to subtract from the value, provided the chosen square is not larger. After subtracting, we have a new value and the next player chooses a square to subtract from it. 

The game play continues to alternate between the two players until no moves are possible. Whoever is about to play at that point loses!

##AI-Strategies

###Random Strategy: 
The AI picks moves randomly.
###Minimax Strategy: 
The AI evaluates all of the possible moves, and chooses the strongest possible move by picking one that returns the highest score. The algorithm does not contain any optimization techniques.
###Minimax Memoize: 
The AI performs the same operations as the regular Minimax Strategy. However, it uses the method of memoization, an optimization technique that avoids redundancy by storing the positions it has come across in a dictionary, where the position and its corresponding "score" are stored. Hence, when the algorithm comes across a position it has already seen, it does not have to make another expensive recursive call.
###Minimax Pruning (Alpha-Beta Pruning): 
Minimax is presented with a huge tree of game state (position) sequences. However, some careful consideration shows that, in many situations, Minimax may ignore huge portions of the tree, since the position sequences in those portions won't change the outcome of the game. Hence, in this technique, minimax is optimized by keeping track of the score already guaranteed to each opponent, and abandoning further search whenever the score guaranteed for itself is greater than the score guaranteed to its opponent.
###Minimax Myopia: 
In this technique, minimax looks ahead of the game by only some n moves. If minimax looks ahead n moves and the game has not ended, then it should use its best guess to provide a score for that game position. This is not as accurate as looking all the way ahead, but saves computational resources.


##Usage 
Use Python 3.4 and terminal for optimal results.

Type the following in terminal to run the python file:

<code>$python game_view.py</code>




#Authors 

* Nana Nosirova
* Humair Khan

