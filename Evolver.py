import Genome
from time import sleep
import multiprocessing
import random
import os
from config import Evolver as config
from config import DisplayOptions

def Pawn(commands, responses, AIclass, display):
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
    if len(keys) < 1: continue
    ai2 = genomes[ random.choice(keys) ]
    
    #run competition
    winner = AIclass.compete(AIclass(ai1), AIclass(ai2), display)
    #report results
    if winner != "draw":
      if winner == 'white':
        if display == DisplayOptions.verbose: print( ai1.id, " beat ", ai2.id)
        responses.put( (ai1.id, ai2.id) )
      else:
        if display == DisplayOptions.verbose: print( ai2.id, " beat ", ai1.id)
        responses.put( (ai2.id, ai1.id) )
    else:
      if display == DisplayOptions.verbose: print( ai1.id, " drew with ", ai2.id)

class Queen(object):
  def __init__(self, AI, display = config.display, pawns = 0, genomeCount = config.defaultGenomeCount):
    if pawns == 0: pawns = multiprocessing.cpu_count()
    self._populateProcesses(pawns, AI, display)
    self._populateGenomes(genomeCount, AI)
    self._sendGenomesToProcesses()
    self._startProcesses()
    self.display = display
    
    #montior results
    while True:
      response = self.responses.get()
      if self.display == DisplayOptions.dot: print('.', end='', flush=True)
      if response[0] in self.genomes:
        self.genomes[ response[0] ].score += 1
        if self.genomes[ response[0] ].score >= 2*config.genomeInitialScore: self.reproduceGenome(response[0])
      if response[1] in self.genomes:
        self.genomes[ response[1] ].score -= 1
        if self.genomes[ response[1] ].score <= 0: self.killGenome(response[1])
  def _populateProcesses(self, pawns, AI, display):
    self.responses = multiprocessing.JoinableQueue()
    self.commandQueues = []
    self.processes = []
    for _ in range(pawns):
      commands = multiprocessing.JoinableQueue()
      p = multiprocessing.Process(target=Pawn, args=(commands, self.responses, AI, display))
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
      genome.score = config.genomeInitialScore
      command = ('g', str(genome))
      self._sendCommandToAllProcesses( command )
  def _sendCommandToAllProcesses(self, command):
    for commandQueue in self.commandQueues:
      commandQueue.put(command)
  def _startProcesses(self):
    for process in self.processes:
      process.start()
  def reproduceGenome(self, id):
    if self.display >= DisplayOptions.brief: print(id, " is reproducing")
    genome = Genome.CopyGenome( self.genomes[id] )
    genome.mutate()
    self.genomes[genome.id] = genome
    command = ('g', str(genome))
    self._sendCommandToAllProcesses( command )
    file = open(genome.id+".gen", 'w')
    file.write(str(genome))
    file.close()
    self.genomes[id].score -= config.genomeInitialScore
    genome.score = config.genomeInitialScore
  def killGenome(self, id):
    if self.display >= DisplayOptions.brief: print(id, " has died")
    del self.genomes[id]
    os.remove(id+".gen")
    command = ('d', id)
    self._sendCommandToAllProcesses( command )
    