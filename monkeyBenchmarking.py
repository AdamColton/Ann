#!/usr/bin/env python
import connectfour
import c4Ai
import Genome
import random
import os
import config
import multiprocessing
import monkeyAI

if __name__ == '__main__':
  
  processes = multiprocessing.cpu_count()
  responses = multiprocessing.JoinableQueue()
  for _ in range(processes):
    multiprocessing.Process(target=monkeyAI.benchmarkLoop, args=(responses,), daemon=True).start()

  file = open("benchmark.txt", 'w')
  file.write('')
  file.close()
  
  while True:
    wins = {
      'ai': 0,
      'monkey': 0,
      'draw': 0
    }
    for i in range(config.monkeyBenchmarkResolution):
      wins[responses.get()] += 1
    file = open("benchmark.txt", 'a')
    file.write(str(wins['ai']) + " / " + str(wins['monkey']) + '\n')
    file.close()