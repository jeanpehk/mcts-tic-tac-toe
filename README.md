# Monte Carlo Tree Search

A simple [MCTS](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) implementation for tic tac toe.

All moves are chosen randomly, still it seems to perform decently if enough playouts for each position
are given.

Basic outline of the algorithm:
- Search for new playouts i.e. leaf nodes with possible moves (select).
- Expand leaf node by creating child nodes for all possible next moves (expand).
    - This is done because the search space for next move in tic tac toe is so small.
    - Choose the move for playout randomly from created child nodes.
- Simulate the game from chosen node.
- Update the result for the tree (update).

