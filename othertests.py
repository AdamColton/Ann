import Genome
import random

def output(outStr):
  file = open("output.txt", 'w')
  file.write(outStr)
  file.close()
  
def view_10_rounds_of_output():
  genome = Genome.Genome(10,10)
  for i in range(100):
    genome.mutate()
  ann = genome.generate()
  for i in range(10):
    for input in ann.inputs:
      input.val = random.random()*2 - 1
    ann.calculate()
    disp = []
    for output in ann.outputs:
      disp.append( output.val )
    print( ", ".join(map(str,disp)) )
    
def view_ann_after_50():
  genome = Genome.Genome(10,10)
  genome.perturbSynapseWeights(2,1)
  ann = genome.generate()
  for input in ann.inputs:
    input.val = random.random()*2 - 1
  ann.calculate(50)
  output( str(ann) )
  
def view_mutations():
  genome = Genome.Genome(10,10)
  for i in range(20):
    print( genome.mutate() )
    
def view_genome_str():
  genome = Genome.Genome(2,3)
  for i in range(1000):
    genome.mutate()
  output(str(genome))
    
view_genome_str()