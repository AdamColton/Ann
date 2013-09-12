import random
import Genome
import connectfour
import os
from config import Monkey as config
from config import DisplayOptions
from config import AiLibraries

if config.aiLibrary == AiLibraries.c4Ai:
  import c4Ai
  aiLibrary = c4Ai.C4AI
elif config.aiLibrary == AiLibraries.c4McAi:
  import c4McAi
  aiLibrary = c4McAi.C4MCAI

def makeMonkeyMove(game):
  possibleNextMoves = game.getAllMoveIds()
  move = random.choice(possibleNextMoves)
  game.makeMove(move)
  
def gameLoop(genomeString, responses, iterations, display):
  playerToIntMap = ['white', 'black', 'draw']
  for _ in range(iterations):
    ai = aiLibrary( Genome.GenomeFactory(genomeString) )
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
    if display == DisplayOptions.verbose: game.display()
    if display >= DisplayOptions.brief: print('Winner: ', playerMap[ playerToIntMap.index(game.winner) ])
    responses.put(playerMap[ playerToIntMap.index(game.winner) ])
    
def benchmarkLoop(responses, display):
  playerToIntMap = ['white', 'black', 'draw']
  while True:
    genomeName = random.choice( [f for f in os.listdir(".") if os.path.isfile(f) and f[-4:] == ".gen"] )
    file = open(genomeName, 'r')
    genomeString = file.read()
    file.close()
    ai = aiLibrary( Genome.GenomeFactory(genomeString) )
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
    if display == DisplayOptions.verbose:game.display()
    if display >= DisplayOptions.brief: print(genomeName[:-4], ' Winner: ', playerMap[ playerToIntMap.index(game.winner) ])
    responses.put(playerMap[ playerToIntMap.index(game.winner) ])