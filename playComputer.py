#!/usr/bin/env python
import connectfour
import c4Ai
import sys
import Genome
import os
import random

print("Who goes first?")
firstPlayer = int( input("0-AI, 1-Person: ") )
aiName = input("Neural Net Name (0 for random): ")
if aiName == "0":
  aiName = random.choice( [f for f in os.listdir(".") if os.path.isfile(f) and f[-4:] == ".gen"] )
  print("Using ", aiName)
else:
  aiName += ".gen"
file = open(aiName, 'r')
genome = Genome.GenomeFactory(file.read())
file.close()
ai = c4Ai.C4AI( genome )
game = connectfour.Game()

if firstPlayer == 0:
  current = "ai"
else:
  current = "player"
  
while not game.gameOver:
  if current == "ai":
    ai.takeTurn(game)
    current = "player"
  else:
    game.display()
    move = input("Next Move: ")
    game.makeMove(int(move))
    current = "ai"
game.display()
print(game.winner)
input()
