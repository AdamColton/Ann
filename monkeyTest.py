#!/usr/bin/env python
import random
import os
import config
import multiprocessing
import monkeyAI
from config import Monkey as config
from config import DisplayOptions

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
  iterationsPerProcess = int(config.benchmarkResolution / processes)
  for _ in range(processes):
    multiprocessing.Process(target=monkeyAI.gameLoop, args=(genomeString, responses, iterationsPerProcess, config.display), daemon=True).start()

  wins = {
    'ai': 0,
    'monkey': 0,
    'draw': 0
  }
  
  for i in range(iterationsPerProcess * processes):
    wins[responses.get()] += 1
    if config.display == DisplayOptions.dot : print('.', end="", flush=True)
  print('\n',wins)
  input()
