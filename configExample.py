class Enum:
  def __init__(self, *args):
    self._enum = args
  def __getattr__(self,name):
    return self._enum.index(name)

DisplayOptions = Enum('none','dot','brief','verbose')
AiLibraries = Enum('c4Ai','c4McAi')

class Monkey:
  display = DisplayOptions.none
  benchmarkResolution = 300
  aiLibrary = AiLibraries.c4McAi
  cores = 0
  # cores = 0 will use all available cores
  # cores = 2 will run 2 processes (even if only 1 core is available)
  # cores = -3 will use all but one three cores (so 5 cores on an 8 core machine), but will always use at lease one core.
  
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
  
class C4wrapper:
  genomeInitialScore = 5
  display = DisplayOptions.none
  genomes = 1000
  cores = -1
  
class C4AI:
  iterations = 50
  
class C4MCAI:
  simulations = 1000
  neuralNetIterations = 20
  movePool = 2
  startingScore = 3
  startingAttempts = 1
  nnMcDepth = 7