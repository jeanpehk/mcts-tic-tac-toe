# Monte Carlo Tree Search

A simple [MCTS](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) implementation for tic tac toe.

You can play vs it by running the program.
For each move made the program prints all next moves and their associated winrates.

Since playouts are done as random moves and the deciding factor for choosing next move is winrate,
it loses some obvious positions because it is not assuming that the opponent is always going to take a winning move
(and instead chooses a move that could lead to a victory if the opponent was not rational). On the other hand it
seems to play well "agressively" taking advantage of blunders.

## How It Works

- Search for new playouts i.e. leaf nodes with possible moves (select).
- Expand leaf node by creating child nodes for all possible next moves (expand).
    - Choose the move for playout randomly from created child nodes.
- Simulate the game from chosen node.
- Update the result for the tree (update).

## Exploration and Exploitation

This is "solved" by selecting child nodes randomly. Still it seems to perform decently if enough playouts for each position
are given since the search space for TTT is so small.
