import Ann
import connectfour
import random
from config import C4AI as config
from config import DisplayOptions

class C4AI(object):
  inputs = 42
  outputs = 1
  
  @staticmethod
  def compete(ai1, ai2, display = DisplayOptions.none):
    game = connectfour.Game()
    currentAi = ai1
    while not game.gameOver:
      currentAi.takeTurn(game)
      if currentAi == ai1:
        currentAi = ai2
      else:
        currentAi = ai1
    if display == DisplayOptions.verbose: game.display()
    if display >= DisplayOptions.brief: print(ai1.genome.id, ' vs ', ai2.genome.id, ' winner ', game.winner)
    return game.winner
  def __init__(self, genome):
    self.neuralNet = genome.generate()
  def evaluate(self, inputs):
    neuralNet = Ann.CopyObjectNet( self.neuralNet )
    neuralNet.input( inputs )
    neuralNet.calculate(config.iterations)
    return neuralNet.outputs[0].val + random.random()*0.0000000001
  def takeTurn(self, game):
    possibleNextMoves = game.getAllMoves()
    moves = []
    for i, board in zip( range(len(possibleNextMoves)), possibleNextMoves):
      if board:
        flattenBoard = [i for row in board for i in row]
        moves.append( (self.evaluate(flattenBoard), i) )
    moves.sort()
    move = moves[-1][1]
    game.makeMove(move)