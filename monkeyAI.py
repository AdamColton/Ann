import random
import c4Ai
import Genome
import connectfour
import os

def makeMonkeyMove(game):
  possibleNextMoves = game.getAllMoveIds()
  move = random.choice(possibleNextMoves)
  game.makeMove(move)
  
def gameLoop(genomeString, responses, iterations, display):
  playerToIntMap = ['white', 'black', 'draw']
  for _ in range(iterations):
    ai = c4Ai.C4AI( Genome.GenomeFactory(genomeString) )
    game = connectfour.Game()
    playerMap = ['ai', 'monkey']
    random.shuffle(playerMap)
    playerMap.append('draw')
    current = playerMap[0]
    while not game.gameOver:
      if current == "ai":
        ai.takeTurn(game)
        current = "monkey"
      else:
        makeMonkeyMove(game)
        current = "ai"
    if display == 'end': game.display()
    responses.put(playerMap[ playerToIntMap.index(game.winner) ])
    
def benchmarkLoop(responses):
  playerToIntMap = ['white', 'black', 'draw']
  while True:
    genomeName = random.choice( [f for f in os.listdir(".") if os.path.isfile(f) and f[-4:] == ".gen"] )
    file = open(genomeName, 'r')
    genomeString = file.read()
    file.close()
    ai = c4Ai.C4AI( Genome.GenomeFactory(genomeString) )
    game = connectfour.Game()
    playerMap = ['ai', 'monkey']
    random.shuffle(playerMap)
    playerMap.append('draw')
    current = playerMap[0]
    while not game.gameOver:
      if current == "ai":
        ai.takeTurn(game)
        current = "monkey"
      else:
        makeMonkeyMove(game)
        current = "ai"
    responses.put(playerMap[ playerToIntMap.index(game.winner) ])
    
 