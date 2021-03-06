import Genome
import random
import os

def output(outStr):
  file = open("output.txt", 'w')
  file.write(outStr)
  file.close()
  
def view_10_rounds_of_output():
  genome = Genome.Genome(42,1)
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
  for i in range(100):
    genome.mutate()
    output(str(genome))

def load_save_loop():
  genome = Genome.Genome(4,4)
  for i in range(100):
    genome.mutate()
  outStr = str(genome)
  genome = Genome.GenomeFactory(outStr)
  outStr += "----\n" + str(genome)
  output( outStr )
  
def print_all_gen_filenames():
  print( [f for f in os.listdir(".") if os.path.isfile(f) and f[-4:] == ".gen"] )

def count_all_gen_files():
  print( len( [f for f in os.listdir(".") if os.path.isfile(f) and f[-4:] == ".gen"]) )
  
count_all_gen_files()