# Monte Carlo Tree Search

A simple [MCTS](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) implementation for tic tac toe.

All moves are chosen randomly, still it seems to perform decently if enough playouts for each position
are given.

For each move made the program prints all next moves and their associated winrates.

## How It Works
- Search for new playouts i.e. leaf nodes with possible moves (select).
- Expand leaf node by creating child nodes for all possible next moves (expand).
    - Choose the move for playout randomly from created child nodes.
- Simulate the game from chosen node.
- Update the result for the tree (update).
