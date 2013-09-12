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
      if display == DisplayOptions.verbose: print(game.moveCount)
      currentAi.takeTurn(game)
      if currentAi == ai1:
        currentAi = ai2
      else:
        currentAi = ai1
    if display == DisplayOptions.verbose: game.display()
    if display >= DisplayOptions.brief: print(ai1.id, ' vs ', ai2.id, ' winner ', game.winner)
    return game.winner
  def __init__(self, genome):
    self.neuralNet = genome.generate()
    self.id = genome.id
  def evaluate(self, inputs):
    neuralNet = Ann.CopyObjectNet( self.neuralNet )
    neuralNet.input( inputs )
    neuralNet.calculate(config.neuralNetIterations)
    return neuralNet.outputs[0].val + random.random()*0.0000000001
  def takeTurn(self, game):
    possibleNextMoves = []
    allPossibleMoves = game.getAllMoves()
    for move, board in zip( range(len(allPossibleMoves)), allPossibleMoves):
      if board: possibleNextMoves.append({
        'board': board,
        'move': move,
        'score': config.startingScore,
        'attempts': config.startingAttempts})
    
    for _ in range(config.simulations):
      possibleFirstMoves = [move for move in possibleNextMoves]
      while len(possibleFirstMoves) > config.movePool:
        possibleFirstMoves.remove(random.choice(possibleFirstMoves))
      random.shuffle(possibleFirstMoves)
      bestScore = 0
      bestMove = possibleFirstMoves[0]
      for move in possibleFirstMoves:
        score = move['score']*1.0 / move['attempts']
        score *= self.evaluate([i for row in move['board'] for i in row])
        if score > bestScore:
          bestScore = score
          bestMove = move
      
      monteCarloBoard = game.copy()
      monteCarloBoard.makeMove(bestMove['move'])
      bestMove['attempts'] += 1
      monteCarloWinner =  self.monteCarlo(monteCarloBoard)
      if monteCarloWinner == game.turn:
        bestMove['score'] += 1
      elif monteCarloWinner != "draw":
        bestMove['score'] -= 1
      
    moves = [((move['score']*1.0) / (move['attempts']), move['move']) for move in possibleNextMoves]
    moves.sort()
    move = moves[-1][1]
    game.makeMove(move)
  def monteCarlo(self, game):
    iteration = 0
    while not game.gameOver:
      moves = []
      i=0
      for board in game.getAllMoves():
        if board:
          moves.append({
            'board': board,
            'move': i
          })
        i += 1
      while len(moves) > config.movePool:
        moves.remove(random.choice(moves))
      bestScore = 0
      bestMove = None
      for move in moves:
        if iteration < config.nnMcDepth:
          score = self.evaluate([i for row in move['board'] for i in row])
        else:
          score = random.random()
        if score > bestScore:
          bestMove = move
          bestScore = score
      game.makeMove(bestMove['move'])
    return game.winner