class Enum:
  def __init__(self, *args):
    self._enum = args
  def __getattr__(self,name):
    return self._enum.index(name)

DisplayOptions = Enum('none','dot','brief','verbose')

class Monkey:
  display = DisplayOptions.none
  benchmarkResolution = 300
  
class Genome:
  patternInputInilizeRange = (1,5)
  patternOutputInilizeRange = (1,5)
  patternHiddenInilizeRange = (1,5)
  defaultPatterns = 10
  defaultGenes = 10
  perturbSynapseWeightsMaxDisturbance = 0.01
  perturbSynapseWeightsdisturbanceProbability = 0.01
  perturbInitialValsMaxDisturbance = 0.01
  perturbInitialValsdisturbanceProbability = 0.01
  perturbBiasesMaxDisturbance = 0.01
  perturbBiasesdisturbanceProbability = 0.01
  geneDefaultNumberOfPatternsRange = (1,5)
  
class Evolver:
  display = DisplayOptions.brief
  defaultGenomeCount = 1000
  genomeInitialScore = 5
  
class C4wrapper:
  display = DisplayOptions.none
  genomes = 1000
  
class C4AI:
  iterations = 50