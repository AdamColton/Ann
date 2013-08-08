#!/usr/bin/env python
import connectfour
import c4Ai
import sys
import Genome

def makeAiMove(ai, game):
  possibleNextMoves = game.getAllMoves()
  moves = []
  for i, board in zip( range(len(possibleNextMoves)), possibleNextMoves):
    if board:
      flattenBoard = []
      for row in board:
        flattenBoard.extend(row)
      ai.inputFromList(flattenBoard)
      ai.compute()
      moves.append( (ai.getOutput(0), i) )
  moves.sort()
  move = moves[-1][1]
  game.makeMove(move)
  

print("Who goes first?")
firstPlayer = int( input("0-AI, 1-Person: ") )
game = connectfour.Game()
genome = Genome.Genome(c4Ai.inputs, c4Ai.outputs)
genome.perturbSynapseWeights(1,1)
genome.perturbInitialVals(1,1)
genome.perturbBiases(1,1)
ai = c4Ai.AI( genome )

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
