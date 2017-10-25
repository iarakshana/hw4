#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
You can use this script to play against your computer's strategy.
"""

from t3 import *

def human_match():
  """
  Get basic input from the command line for a human match.
  """

  play = "Y"
  while play == "Y":

    hmark = ""
    while hmark not in ['X', 'O']:
      hmark = input("Do you want to be 'x' or 'o' [X/o]?  ").upper()
      hmark = hmark or "X"

    g = game(hmark, c1 = computer)
    g.play()

    play = ""
    while play not in ["Y", "N"]:
      play = input("Would you like to play again [Y/n]?  ").upper()
      play = play or "Y"

human_match()
