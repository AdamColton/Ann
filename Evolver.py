import Genome
from time import sleep
import multiprocessing
import random
import os

def Pawn(commands, responses, AIclass):
  genomes = {}
  while True:
    while not commands.empty():
      command = commands.get()
      if command[0] == 'g':
        genome = Genome.GenomeFactory(command[1])
        genomes[genome.id] = genome
      elif command[0] == 'd':
        del genomes[ command[1] ]
    keys = [key for key in genomes.keys() ]
    ai1 = genomes[ random.choice(keys) ]
    keys.remove(ai1.id)
    ai2 = genomes[ random.choice(keys) ]
    
    #run competition
    winner = AIclass.compete(AIclass(ai1), AIclass(ai2), 'end')
    #report results
    if winner != "draw":
      if winner == 'white':
        print( ai1.id, " beat ", ai2.id)
        responses.put( (ai1.id, ai2.id) )
      else:
        print( ai2.id, " beat ", ai1.id)
        responses.put( (ai2.id, ai1.id) )
    else:
      print( ai1.id, " drew with ", ai2.id)

class Queen(object):
  def __init__(self, AI, cores = 4, genomeCount = 1000):
    self._populateProcesses(cores, AI)
    self._populateGenomes(genomeCount, AI)
    self._sendGenomesToProcesses()
    self._startProcesses()
    
    #montior results
    while True:
      response = self.responses.get()
      if response[0] in self.genomes:
        self.genomes[ response[0] ].score += 1
        if self.genomes[ response[0] ].score >= 10: self.reproduceGenome(response[0])
      if response[1] in self.genomes:
        self.genomes[ response[1] ].score -= 1
        if self.genomes[ response[1] ].score <= 0: self.killGenome(response[1])
  def _populateProcesses(self, cores, AI):
    self.responses = multiprocessing.JoinableQueue()
    self.commandQueues = []
    self.processes = []
    for _ in range(cores):
      commands = multiprocessing.JoinableQueue()
      p = multiprocessing.Process(target=Pawn, args=(commands, self.responses, AI))
      p.daemon = True
      self.commandQueues.append(commands)
      self.processes.append(p)
  def _populateGenomes(self, genomeCount, AI):
    self.genomes = {}
    genomeFilenames = [f for f in os.listdir(".") if os.path.isfile(f) and f[-4:] == ".gen"][:genomeCount]
    for filename in genomeFilenames:
      file = open(filename, 'r')
      genome = Genome.GenomeFactory( file.read() )
      file.close()
      self.genomes[genome.id] = genome
    while len(self.genomes) < genomeCount:
      genome = Genome.Genome(AI.inputs, AI.outputs)
      genome.perturbInitialVals(1,1)
      genome.perturbSynapseWeights(1,1)
      genome.perturbBiases(1,1)
      file = open(genome.id+".gen", 'w')
      file.write(str(genome))
      file.close()
      self.genomes[genome.id] = genome
  def _sendGenomesToProcesses(self):
    for genome in (self.genomes[key] for key in self.genomes):
      genome.score = 5
      command = ('g', str(genome))
      self._sendCommandToAllProcesses( command )
  def _sendCommandToAllProcesses(self, command):
    for commandQueue in self.commandQueues:
      commandQueue.put(command)
  def _startProcesses(self):
    for process in self.processes:
      process.start()
  def reproduceGenome(self, id):
    print(id, " is reproducing")
    genome = Genome.CopyGenome( self.genomes[id] )
    genome.mutate()
    self.genomes[genome.id] = genome
    command = ('g', str(genome))
    self._sendCommandToAllProcesses( command )
    file = open(genome.id+".gen", 'w')
    file.write(str(genome))
    file.close()
    self.genomes[id].score -= 5
    genome.score = 5
  def killGenome(self, id):
    print(id, " has died")
    del self.genomes[id]
    os.remove(id+".gen")
    command = ('d', id)
    self._sendCommandToAllProcesses( command )
    