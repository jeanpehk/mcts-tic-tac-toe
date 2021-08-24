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

# TREE NODE

class Node:
  def __init__(self, parent, state, wr):
    self.parent = parent
    self.state = state
    self.wr = wr
    self.nodes = []

  def select(self):
    moves = self.get_new_moves()
    if moves:
      return self
    if check(self.state[0]) is not None:
      return None
    else:
      tried = []
      for i in range(len(self.nodes)):
        while True:
          n = randrange(len(self.nodes))
          if n not in tried:
            tried.append(n)
            break
        leaf = self.nodes[n].select()
        if leaf is not None:
          return leaf
    return None

  def can_expand(self):
    winner = check(self.state[0])
    if winner is not None:
      return False
    moves = self.get_new_moves()
    if not moves:
      return False
    return True

  def expand(self):
    moves = self.get_new_moves()
    if not moves:
      print('error: no moves left')
      return None

    mv = moves[randrange(len(moves))]
    chosen = None
    for m in moves:
      new_state = self.state[0].copy()
      new_state[m] = self.state[1]
      turn = 1 if self.state[1] == 2 else 2
      node = Node(self, [new_state, turn], [0,0,0])
      self.nodes.append(node)
      if m == mv:
        chosen = node

    return chosen

  def get_new_moves(self):
    moves = []
    for i in range(len(self.state[0])):
      done = [n.state for n in self.nodes if n.state[0][i] != 0]
      if self.state[0][i] == 0 and not done:
        moves.append(i)
    return moves

  def rewind(self):
    if self.parent is None:
      return self
    else:
      return self.parent.rewind()

  def update(self, result):
    self.wr[result] += 1
    if self.parent is not None:
      self.parent.update(result)

  def simulate(self):
    w, s = play(self.state[0].copy(), self.state[1])
    self.update(w)

def travel(node, route):
  route.insert(0, node)
  if node.parent is not None:
    travel(node.parent, route)

def mcts(root):
  for i in range(10000):
    leaf = root.select()
    if leaf is None:
#      print('search ended at i: %d' % i)
      break
    child = leaf.expand()
    w, s = play(child.state[0].copy(), child.state[1])
    child.update(w)
  hi = -1
  move = None
  print('\n- MCTS search outcomes:\n')
  for n in root.nodes:
    b = [as_char(x) for x in n.state[0]]
    total = n.wr[0]+n.wr[1]+n.wr[2]
    wr = n.wr[1]/total if total > 0 else 0
    print(n)
    print(str(b[:3]) + ' '*17)
    print('{} {:8.8}'.format(b[3:][:3], wr))
    print(str(b[6:]) + ' '*17)
    if wr > hi:
      hi = wr
      move = n
  return move

def as_char(c):
  if c == 1:
    return 'X'
  elif c == 2:
    return 'O'
  else:
    return ' '

def print_board(s):
  b = [as_char(x) for x in s]
  print(b[:3])
  print(b[3:][:3])
  print(b[6:])

winner = None
state = ([0]*9, 1)
root = Node(None, (state[0],state[1]), [0,0,0])
while winner is None:
  mv = mcts(root)
  state = mv.state[0]
  print('\n- Board state after MCTS move:\n')
  print_board(state)
  winner = check(state)
  if winner is None:
    while True:
      my_move = int(input('\nYour Move: '))
      if state[my_move] == 0:
        state[my_move] = 2
        break
      else:
        print('mv %d unavailable at state %s' % (my_move, state))
    print('\n- Board state after your move:\n')
    print_board(state)
    winner = check(state)
    root = Node(None, (state, 1), [0,0,0])

winner = as_char(winner)
if winner == ' ':
  print('\nTie!')
else:
  print('\nWinner: %s' % winner)

