import Ann
import connectfour

class C4AI(object):
  inputs = 42
  outputs = 1
  iterations = 50
  
  @staticmethod
  def compete(ai1, ai2, displayMode = "none"):
    game = connectfour.Game()
    currentAi = ai1
    while not game.gameOver:
      currentAi.takeTurn(game)
      if displayMode == "all": game.display()
      if currentAi == ai1:
        currentAi = ai2
      else:
        currentAi = ai1
    if displayMode == "end": game.display()
    return game.winner
  def __init__(self, genome):
    global guid
    self.genome = genome
  def evaluate(self, inputs):
    neuralNet = self.genome.generate()
    neuralNet.input( inputs )
    neuralNet.calculate(self.iterations)
    return neuralNet.outputs[0].val
  def takeTurn(self, game):
    possibleNextMoves = game.getAllMoves()
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