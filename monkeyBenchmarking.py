#!/usr/bin/env python
from config import Monkey as config
from config import DisplayOptions
import multiprocessing
import monkeyAI
  

if __name__ == '__main__':
  processes = config.cores
  if processes==0:
    processes = multiprocessing.cpu_count()
  elif processes < 0:
    processes += multiprocessing.cpu_count()
    if processes < 0: processes = 1
  responses = multiprocessing.JoinableQueue()
  for _ in range(processes):
    multiprocessing.Process(target=monkeyAI.benchmarkLoop, args=(responses, config.display), daemon=True).start()

  file = open("benchmark.txt", 'w')
  file.write('')
  file.close()
  
  while True:
    wins = {
      'ai': 0,
      'monkey': 0,
      'draw': 0
    }
    for i in range(config.benchmarkResolution):
      wins[responses.get()] += 1
      if config.display == DisplayOptions.dot: print('.', end='', flush=True)
    file = open("benchmark.txt", 'a')
    file.write(str(wins['ai']) + " / " + str(wins['monkey']) + '\n')
    file.close()