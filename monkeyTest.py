#!/usr/bin/env python
import connectfour
import c4Ai
import Genome
import random
import os
import config
import multiprocessing

#todo : make this multiproc

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

if __name__ == '__main__':
  genomeName = input("Neural Net Name (0 for random): ")
  responses = multiprocessing.JoinableQueue()
  if genomeName == "0":
    genomeName = random.choice( [f for f in os.listdir(".") if os.path.isfile(f) and f[-4:] == ".gen"] )
    print("Using ", genomeName)
  else:
    genomeName += ".gen"
    
  file = open(genomeName, 'r')
  genomeString = file.read()
  file.close()
  
  processes = multiprocessing.cpu_count()
  iterationsPerProcess = int(config.monkeyTestIterations / processes)
  for _ in range(processes):
    multiprocessing.Process(target=gameLoop, args=(genomeString, responses, iterationsPerProcess, config.monkeyDisplay), daemon=True).start()

  wins = {
    'ai': 0,
    'monkey': 0,
    'draw': 0
  }
  
  for i in range(iterationsPerProcess * processes):
    wins[responses.get()] += 1
    print('.', end="", flush=True)
  print('\n',wins)
  input()
