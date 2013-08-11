import Genome
from time import sleep
import multiprocessing
import random

def worker(commands, responses, AIclass):
  genomes = {}
  while True:
    while not commands.empty():
      command = commands.get()
      if command[0] == 'g':
        genome = Genome.GenomeFactory(command[1])
        genomes[genome.id] = genome
    keys = [key for key in genomes.keys() ]
    ai1 = genomes[ random.choice(keys) ]
    keys.remove(ai1.id)
    ai2 = genomes[ random.choice(keys) ]
    
    #run competition
    winner = AIclass.compete(AIclass(ai1), AIclass(ai2))
    #report results
    if winner != "draw":
      if winner == 'white':
        responses.put( (ai1.id, ai2.id) )
      else:
        responses.put( (ai2.id, ai1.id) )

def start(AI, cores = 4, genomeCount = 1000):
  responses = multiprocessing.JoinableQueue()
  commandQueues = []
  processes = []
  for _ in range(4):
    commands = multiprocessing.JoinableQueue()
    commandQueues.append(commands)
    p = multiprocessing.Process(target=worker, args=(commands, responses, AI))
    p.daemon = True
    processes.append(p)
  #try loading from file
  genomes = { genome.id : genome for genome in (Genome.Genome(AI.inputs, AI.outputs) for _ in range(genomeCount)) }
  for genome in (genomes[key] for key in genomes):
    genome.score = 5
    genomeString = str(genome)
    #save to file (try using threads)
    for commandQueue in commandQueues:
      commandQueue.put(('g', genomeString))
  for process in processes:
    process.start()
  #montior results
  while True:
    response = responses.get()
    print(response[0], " beat ", response[1])