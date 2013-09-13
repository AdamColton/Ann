#!/usr/bin/env python
import connectfour
import sys
import Genome
import os
import random

print("Choose Your Opponent?")
opponent = int( input("0-Monkey, 1-Monte Carlo 2-Neural Net 3-MC NN: ") )
if opponent > 3 or  opponent < 0 : opponent = 0

print("Who goes first?")
firstPlayer = int( input("0-AI, 1-Person: ") )

ai = None
if opponent == 2 or opponent == 3 :
  aiName = input("Neural Net Name (0 for random): ")
  if aiName == "0":
    aiName = random.choice( [f for f in os.listdir(".") if os.path.isfile(f) and f[-4:] == ".gen"] )
    print("Using ", aiName)
  else:
    aiName += ".gen"
  file = open(aiName, 'r')
  genome = Genome.GenomeFactory(file.read())
  file.close()
  if opponent == 2:
    import c4Ai
    ai = c4Ai.C4AI( genome )
  elif opponent == 3:
    import c4McAi
    ai = c4McAi.C4MCAI( genome )
else:
  import monkeyAI
  if opponent == 0:
    ai = monkeyAI.Monkey()
  if opponent == 1:
    ai = monkeyAI.MonteCarlo()
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
