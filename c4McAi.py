import Ann
import connectfour
import random
from config import C4MCAI as config
from config import DisplayOptions

class C4MCAI(object):
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
    neuralNet.calculate(config.neuralNetIterations)
    return neuralNet.outputs[0].val + random.random()*0.0000000001
  def takeTurn(self, game):
    allPossibleMoves = game.getAllMoves()
    possibleNextMoves = []
    while possibleNextMoves < config.movePool and len(allPossibleMoves) > 0:
      move = random.choice(allPossibleMoves)
      allPossibleMoves.remove(move)
      possibleNextMoves.append({
        "move": move,
        "wins": config.startingWins,
        "losses": config.startingLosses
      })
    
    moves = []
    for i, board in zip( range(len(possibleNextMoves)), possibleNextMoves):
      if board:
        flattenBoard = []
        for row in board:
          flattenBoard.extend(row)
        moves.append( (self.evaluate(flattenBoard), i) )
    moves.sort()
    move = moves[-1][1]
    game.makeMove(move)