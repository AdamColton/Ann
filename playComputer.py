#!/usr/bin/env python
import connectfour
import c4Ai
import sys
import Genome
  

print("Who goes first?")
firstPlayer = int( input("0-AI, 1-Person: ") )
aiName = input("AI id: ") + ".gen"
print(aiName)
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
