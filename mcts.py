#!/usr/bin/env python3

from random import randrange

# TIC TAC TOE

TIE = 0
wins = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [6,4,2]]

# check for winner
def check(s):
  winner = None
  for w in wins:
    if s[w[0]] == s[w[1]] == s[w[2]] and s[w[0]] != 0:
      return s[w[0]]
  if 0 not in s:
    return TIE
  return None

def move(state, turn):
  moves = []
  for i in range(len(state)):
    if state[i] == 0:
      moves.append(i)
  assert(len(moves) > 0) # need to have moves left to call this
  mv = randrange(len(moves))
  state[moves[mv]] = turn
  return state

def play(s, turn):
  winner = check(s)
  while winner is None:
    s = move(s, turn)
    turn = 1 if turn == 2 else 2
    winner = check(s)
  return winner, s

# MCTS

class Node:
  def __init__(self, parent, state, wr):
    self.parent = parent
    self.state = state
    self.wr = wr
    self.nodes = []

  def select(self):
    if check(self.state[0]) is not None:
#      print('no moves left for node with state: %s' % self.state[0])
#      print('returning None')
      return None
    if not self.nodes and check(self.state[0]) is None:
      return self
    # no new playouts left for this node
    for i in range(len(self.nodes)):
      n = randrange(len(self.nodes))
      leaf = self.nodes[n].select()
      if leaf is not None:
        return leaf
      else:
        # None returned -> no moves left for child
        assert(check(self.state[0]) is None)
        return self
    raise Exception('All possible paths taken?')

  def expand(self):
    winner = check(self.state[0])
    if check(self.state[0]) is not None:
      self.wr[winner] += 1
      self.update(winner)
      return None

    # no winner so expand
    moves = self.get_valid_moves()
    new_state = self.state[0].copy()
    mv = moves[randrange(len(moves))] # choose move at random
    new_state[mv] = self.state[1]
    turn = 1 if self.state[1] == 2 else 2
    node = Node(self, (new_state, turn), [0,0,0])
    self.nodes.append(node)
    return node

  def rewind(self):
    if self.parent is None:
      return self
    else:
      return self.parent.rewind()

  def update(self, result):
    self.wr[result] += 1
    if self.parent is not None:
      self.parent.update(result)

  def get_valid_moves(self):
    moves = []
    for i in range(len(self.state[0])):
      if self.state[0][i] == 0:
        moves.append(i)
    return moves

class Smart:
  def __init__(self, tree):
    self.tree = tree


node = Node(None, ([0]*9, 1), [0,0,0])
for i in range(100000):
  root = node.rewind()
  leaf = root.select()
  child = leaf.expand()
  if child is not None:
    w, s = play(child.state[0].copy(), child.state[1])
    child.update(w)
  else:
    print('what now')
    break

