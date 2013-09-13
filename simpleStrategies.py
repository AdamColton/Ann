#!/usr/bin/env python
import connectfour
import c4Ai
import Genome
import random
import os
  
nnName = input("Neural Net Name (0 for random): ")
if nnName == "0":
  nnName = random.choice( [f for f in os.listdir(".") if os.path.isfile(f) and f[-4:] == ".gen"] )
else:
  nnName += ".gen"
print("Who goes first?")
firstPlayer = input("0-AI, 1-SimpleStrat: ")

file = open(nnName)
genome = Genome.GenomeFactory(file.read())
file.close()
ai = c4Ai.C4AI(genome)

strategies = [
    [0,0,0,0],
    [1,1,1,1],
    [2,2,2,2],
    [3,3,3,3],
    [4,4,4,4],
    [5,5,5,5],
    [6,6,6,6],
    [0,1,2,3,4,5,6,0,1,2,3,4,5,6,0,1,2,3,4,5,6,0,1,2,3,4,5,6]
    ]
    
wins = {'white':0, 'black':0, None:0, 'draw':0}

for strategy in strategies:
  game = connectfour.Game()
  current = "player"
  if firstPlayer == 0: current = "ai"
  while not game.gameOver and len(strategy) > 0:
    if current == "ai":
      ai.takeTurn(game)
      current = "player"
    else:
      move = strategy.pop(0)
      game.makeMove(int(move))
      current = "ai"
  game.display()
  print(game.winner)
  wins[game.winner] += 1
print(wins)
input()