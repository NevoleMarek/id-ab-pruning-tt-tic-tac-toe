# AI for TicTacToe(piškvorky) game

## Game description

Piškvorky is a czech version of game called TicTacToe. The difference between the two is just that the board size is slightly bigger at 15x15 tiles and for the win the player has to have 5 marks in a row instead of 3.

## Used algorithms

The AI for this game is based on [negamax](https://en.wikipedia.org/wiki/Negamax)(equivalent to minimax) algorithm. Negamax searches the game tree in DFS fashion. Usually with set depth limit it has to traverse whole game tree to find optimal move.

To reduce the number of traversed nodes [AlphaBeta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) algorithm is used. It prunes the game tree by using alpha and beta variables to cutoff subtrees that won't yield better move.

Ordering of the child nodes is very important to performance, the better moves found earlier then the more subtrees are pruned. I used random ordering, and limited admissible moves to tiles that are within certain radius of already played moves.

Since time spent by the algoritm is exponential with the depth and broadness of the tree, it is a good idea to implement [iterative deepening](https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search). Iterative deepening runs the AlphaBeta algorithm with depth limit initially set to 1 and reruns it with incremented depth limit while within chosen time limit.

Last improvement is in memoization using [transposition table](https://en.wikipedia.org/wiki/Transposition_table). Same nodes are evaluated over and over, especially when iterative deepening is implemented, the implemented evaluation function uses convolutions to score the board and can be expensive when ran on every board combination. The basic method, which I used, uses [zobrist hashing](https://en.wikipedia.org/wiki/Zobrist_hashing) to hash the game board and stores it to hash table of particular size(2^16 is used here).

With time limit set to 5 seconds, the AI is capable to beat average to slightly advanced players. Scoring function is very basic and is a big part of AI game performance.

## How to run

1) Install required packages from `requirements.txt`
2) Run the app with `python main.py`

## TODO

- Use alpha, beta values in transposition table to further prune the game tree.
- Improve scoring function.
- Next better algorithm to implement would be MDT(f) or NegaScout.
- Move ordering e.g. killer heuristic or based on previous iterations of iterative deepening.
