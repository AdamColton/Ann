import Ann
import connectfour

inputs = 42
outputs = 1
iterations = 50

def compete(ai1, ai2, displayMode = "none"):
  game = connectfour.Game()
  currentAi = ai1
  while not game.gameOver:
    currentAi.makeMove(game)
    if displayMode == "all": game.display()
    if currentAi == ai1:
      currentAi = ai2
    else:
      currentAi = ai1
  if displayMode == "end": game.display()
  return game.winner

class AI(object):
  def __init__(self, genome):
    global guid
    self.genome = genome
  def evaluate(self, inputs):
    neuralNet = self.genome.generate()
    neuralNet.input( inputs )
    neuralNet.calculate(iterations)
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
        print( moves[-1] )
    moves.sort()
    move = moves[-1][1]
    game.makeMove(move)