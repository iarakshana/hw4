#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a simple set of classes for playing Tic-Tac-Toe
according to the strategies laid out by Newell & Simon:
https://en.wikipedia.org/wiki/Tic-tac-toe

Note that this strategy is not necessarily optimal
since player 1 plays in the center instead of the corner.
With a game start with X0 O8, X could play at X1 and lose.

However, since the game begins with X4, it's self-consistent.
"""
__author__    = "Adriana Rakshana, Julia Karon"
__copyright__ = "Copyright 2017 Rakshana and Karon"
__email__     = "iarakshana@uchicago.edu and jkaron@uchicago.edu"

import sys
import random
from copy import deepcopy as dc


class player():
  """
  The player class contains its mark and a strategy for "moves."
  That strategy is specialized for human (input) and computer (N&S)
  classes, while the monkey class uses the player's random move.
  """

  def __init__(self, mark):
    """
    :param mark: the class simply knows its marker (X or O).
    """

    assert(mark in "XO")

    self.mark = mark
    self.other_mark = "XO"[mark == "X"]

  def move(self, match):
    """
    :param match: is an instance of the game class, for which to generate a move.
    """

    return random.choice([i for i in range(9) if not match.board[i]])


class monkey(player):
  """
  The monkey class is just a "cute" renaming of the player with random strategy.
  """

  def __init__(self, mark):
    """
    :param mark: the class simply knows its marker (X or O).
    """

    assert(mark in "XO")

    self.mark = mark
    self.other_mark = "XO"[mark == "X"]

  pass


class human(player):
  """
  The human player specializes the move for command-line input.
  """

  def move(self, match):
    """
    Method displays the game board and handles input for a human player.
    """

    m = -1
    while m not in range(9):
      try:
        print(match)
        m = int(input("Your move, {} [0-8]: ".format(self.mark)))
      except ValueError: continue

    return m


class computer(player):
  """
  This is the class to be specialized by students.
  """
  def __init__(self, mark):
    """
    :param mark: the class simply knows its marker (X or O).
    """

    assert(mark in "XO")

    self.mark = mark
    self.other_mark = "XO"[mark == "X"]

  def move(self, match):
    """
    This is your specialization.
    I would suggest that you follow the strategy of N&S (wiki)
    https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
    but so long as you don't lose to monkeys, you can do what you want.
    """

    #1# Win if possible.
    self_wins = match.check_for_wins(self.mark)

    if self_wins != None:
        return self_wins
#selfwins checks for number of wins for the player mark
#and so if there is a way to win we play it


    #2# Block wins, if possible.
    other_wins = match.check_for_wins(self.other_mark)

    if other_wins != None:
        return other_wins
#if there is a way for the other player to win we play in that spot
#to block their win

    #3# Fork.
    fork_twos = match.check_for_twos(self.mark)

    for i in fork_twos:
        if fork_twos[i] ==2:
            return i
#if there are two ways to win for the player we play there

    #4# Fork Defense.
    # Get posible squares to play for a "two"
    self_twos = match.check_for_twos(self.mark)

# We'll now consider hypothetical games,
# where we play in each of the "two" positions.
    for i in self_twos:                 # For each of these
        hypo_match = dc(match)          # create a copy of the game -- dc is deepcopy
        hypo_match.board[i] = self.mark # try playing there.

    # Now look for the win implied by your "two".
    # Your opponent would have to play here.
        w = hypo_match.check_for_wins(self.mark)

    # For your OPPPONENT, get any potential twos.
        hypo_twos = hypo_match.check_for_twos(self.other_mark)

    # If your potential win is not just a two for them,
    # but in fact a DOUBLE two -- a fork -- don't move here!
        if w in hypo_twos and hypo_twos[w] > 1: continue

    # Otherwise, it meets the condition.  Do it!!
        return i

    #5# Block a fork.
    opponent_fork = match.check_for_twos(self.other_mark)

    for i in opponent_fork:
        if opponent_fork[i] == 2:
            return i
#if other player is trying to play to create a fork, i.e. ==2 then we play there

    #6# Center.

    if not match.board[4]:
        return 4
#4 is the centre of the board

    #7# Opposite corner.

    for i in [0, 2, 6, 8]:
        if match.board[i] == self.other_mark:
            if not match.board[8 - i]:
                return (8 - i)
#we play in the 8-i location as that will be the opposite corner

    #8# Empty corner.

    for i in [0, 2, 6, 8]:
        if not match.board[i]:
            return i

    #9# Side
    for i in [1, 3, 5, 7]:
        if not match.board[i]:
            return i


    return random.choice([i for i in range(9) if not match.board[i]])


class game():
  """
  game contains two players -- humans, monkeys, or computers --
  who then play in a loop.
  """

  mini_num = "012345678"

  threes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # columns
            [0, 4, 8], [2, 4, 6]]            # diagonals

  def __init__(self, hmark = None, c1 = monkey, c2 = monkey):
    """
    Create a new game.

    :parame hmark: the marker for the human player
    :parame c1:    the class of computer 1, by default a monkey (random)
    :parame c2:    the class of computer 2, by default a monkey (random)
    """

    if hmark:

      if hmark.upper() not in ["X", "O"]:
        print("Human must play either X or O.  Quitting.")
        sys.exit()

      self.cmatch  = False
      self.vmark   = hmark
      self.players = [human(hmark), c1("XO"[hmark == "X"])]

    else:
      self.cmatch  = True
      self.vmark   = "XO"[random.randint(0, 1)]
      self.players = [c1("XO"[self.vmark == "X"]), c2(self.vmark)]

    self.players.sort(key = lambda x: x.mark, reverse = True)

    self.board = [None for x in range(9)]

    self.moves = 9 - self.board.count(None) # for debugging, can set moves...


  def __str__(self):

    s = ""
    for n in range(9):

      if not (n%3): s += "\n"

      if self.board[n]:
        s += self.board[n]
      else: s += game.mini_num[n]
      s += " "

    s += "\n"

    return s


  def play(self):
    """
    play is just a (max) 9 iteration loop
    between the two players defined,
    which returns the winning player (or None).
    """

    winner = ""
    while self.moves < 9 and not winner:

      m = self.players[self.moves % 2].move(self)
      while not self.check_move(m):
        m = self.players[self.moves % 2].move(self)

      self.board[m] = ["X", "O"][self.moves % 2]
      self.moves += 1

      winner = self.winner()

    if not self.cmatch:
      print(self)
      print("Alas, our game is at an end!")
      if self.moves < 9:
        print("Congratulations, player {}!!".format(winner))
      if self.moves == 9: print("It is a draw.")

    return winner


  def check_move(self, move):
    """
    Method verifies that the proposed move m is
    (a) legal -- that is, an integer from 0-8 and
    (b) not already taken.
    :param move: proposed move
    :return: boolean True if move is legal, otherwise False.
    """

    if type(move) != int or \
       move > 8 or move < 0:
      print("I require an integer, 0-8!")
      return False

    if self.board[move]:
      print("Players cannot play where there is already a mark!")
      print(self)
      return False

    return True



  def winner(self):
    """
    Method verifies that the proposed move m is
    (a) legal -- that is, an integer from 0-8 and
    (b) not already taken.
    :param move: proposed move
    :return: the winner (or "").
    """

    for m in ["X", "O"]:

      for three in game.threes:
        if all(self.board[sq] == m for sq in three):
          return m

    # Return the winner.  Game will end.
    return ""

  def check_for_wins(self, mark):
    """
    Look for any winning moves for player.
    :param mark: player to search for wins, for.
    :return: location of the first winning move, or None.
    """

    for three in game.threes:
      if sum(self.board[cell] == mark for cell in three) == 2:
        for cell in three:
          if self.board[cell] == None:
            return cell

    return None

  def check_for_twos(self, mark):
    """
    Search for twos
    :param mark: player to search for
    :return: dictionary of with multiplicity of twos created by playing at a location.
    """

    twos = {}
    for three in game.threes:
      diag = [self.board[cell] for cell in three]
      if mark in diag and diag.count(None) == 2:
        for cell in three:
          if not self.board[cell]:
            if cell in twos: twos[cell] += 1
            else: twos[cell] = 1

    return twos
