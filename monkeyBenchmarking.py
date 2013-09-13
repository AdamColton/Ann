#!/usr/bin/env python
from config import Monkey as config
from config import DisplayOptions
import multiprocessing
import monkeyAI
import Graph
import datetime

#Requires Pillow
  

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

  filename = datetime.datetime.now().strftime("benchmark.%y%m%d%H%M.txt")
  file = open(filename, 'w')
  file.write('')
  file.close()
  
  data = []
  while True:
    wins = {
      'ai': 0,
      'monkey': 0,
      'draw': 0
    }
    for i in range(config.benchmarkResolution):
      print(i)
      wins[responses.get()] += 1
      if config.display == DisplayOptions.dot: print('.', end='', flush=True)
    data.append(wins['ai']*1.0/config.benchmarkResolution)
    if len(data) > 2 : Graph.new(data).line_graph(datetime.datetime.now().strftime("%y%m%d%H%M"))
    file = open(filename, 'a')
    file.write(str(wins['ai']) + " / " + str(wins['monkey']) + '\n')
    file.close()