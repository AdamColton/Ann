import random
import Ann
from config import Genome as config

"""
I would like a mechanism where a gene expression passes data into a gene at the time that it is expressed.
Think of fingers and toes. Toes are different than fingers and they all have different lengths, but they
could all be expressed with the same gene. They just need a finger/toe switch and a size parameter.
"""

def getId():
  return str( random.randint(1000, 2**30) )

class Genome(object):
  def __init__(self, inputs, outputs, patterns = config.defaultPatterns, genes = config.defaultGenes):
    self.inputs = inputs
    self.outputs = outputs
    self.patterns = [Pattern(random.randint(*config.patternInputInilizeRange),random.randint(*config.patternOutputInilizeRange),random.randint(*config.patternHiddenInilizeRange)) for i in range(patterns)]
    self.genes = [Gene(self) for i in range(genes)]
    self.id = getId()
  def generate(self):
    ann = Ann.ObjectNet(self.inputs, self.outputs)
    for gene in self.genes:
      self._applyGene(gene, ann)
    return ann
  def _applyGene(self, gene, network):
    mapping = {}
    
    for i in range(len(gene.patterns[0].inputs)):
      mapping['0_' + gene.patterns[0].inputs[i].id] = network.inputs[ gene.inputMap[i] ]
    
    for i in range(len(gene.patterns[-1].outputs)):
      mapping[str(len(gene.patterns)-1) + '_' + gene.patterns[-1].outputs[i].id] = network.outputs[ gene.outputMap[i] ]
    
    self._mapHiddenNodes(gene.patterns, network, mapping)
    self._mapIOnodes(gene.patterns, network, mapping)
    self._mapSynapses(gene.patterns, mapping)
  def _mapHiddenNodes(self, patterns, network, mapping):
    for i in range(len(patterns)):
      for hidden in patterns[i].hidden:
        mapping[str(i) + "_" + hidden.id] = network.addNeuron()
  def _mapIOnodes(self, patterns, network, mapping):
    for i in range(len(patterns)-1):
      outputs = patterns[i].outputs
      inputs = patterns[i+1].inputs
      numberOfNeurons = min(len(outputs), len(inputs))
      neurons = [network.addNeuron() for i in range(numberOfNeurons)]
      for j in range(len(outputs)):
        mapping[str(i) + "_" + outputs[j].id] = neurons[j%numberOfNeurons]
      for j in range(len(inputs)):
        mapping[str(i+1) + "_" + inputs[j].id] = neurons[j%numberOfNeurons]
  def _mapSynapses(self, patterns, mapping):
    for i in range(len(patterns)):
      for neuron in patterns[i].neurons:
        for otherNeuron in neuron.synapses:
          synapseNeuron = mapping[str(i) +  '_' + otherNeuron.id]
          mapping[str(i) +  '_' + neuron.id].addSynapse(synapseNeuron, neuron.synapses[otherNeuron])
  def mutate(self):
    return random.choice([
      self.newGene,
      self.newPattern,
      self.perturbInitialVals,
      self.perturbSynapseWeights,
      self.perturbBiases,
      self.addNeuron,
      self.removeNeuron,
      self.remapGene,
      self.copyGene,
      self.addPatternToGene,
      self.removePatternFromGene,
      self.removeUnusedPattern
    ])()
  def perturbSynapseWeights(self, maxDisturbance = config.perturbSynapseWeightsMaxDisturbance, disturbanceProbability = config.perturbSynapseWeightsdisturbanceProbability):
    for pattern in self.patterns:
      pattern.perturbSynapseWeights(maxDisturbance, disturbanceProbability)
    return "Perturbed Synapse Weights with a maximum disturbance of " + str(maxDisturbance) + " and a probability of " + str(disturbanceProbability)
  def perturbInitialVals(self, maxDisturbance = config.perturbInitialValsMaxDisturbance, disturbanceProbability = config.perturbInitialValsdisturbanceProbability):
    for pattern in self.patterns:
      pattern.perturbInitialVals(maxDisturbance, disturbanceProbability)
    return "Perturbed Intilial Values with a maximum disturbance of " + str(maxDisturbance) + " and a probability of " + str(disturbanceProbability)
  def perturbBiases(self, maxDisturbance = config.perturbBiasesMaxDisturbance, disturbanceProbability = config.perturbBiasesdisturbanceProbability):
    for pattern in self.patterns:
      pattern.perturbBiases(maxDisturbance, disturbanceProbability)
    return "Perturbed Biases with a maximum disturbance of " + str(maxDisturbance) + " and a probability of " + str(disturbanceProbability)
  def newGene(self):
    self.genes.append(Gene(self))
    return "Added a new gene"
  def newPattern(self):
    self.patterns.append( Pattern(random.randint(1,5),random.randint(1,5),random.randint(1,5)) )
    return "Added a new pattern"
  def addNeuron(self):
    random.choice(self.patterns).addNeuron()
    return "Added a Neuron"
  def removeNeuron(self):
    random.choice(self.patterns).removeNeuron()
    return "Removed a neuron"
  def remapGene(self):
    random.choice(self.genes).remap()
    return "Remapped a Genes input and output"
  def copyGene(self):
    gene = CopyGene(self, random.choice(self.genes))
    gene.remap()
    self.genes.append(gene)
    return "Copied a gene and remapped its inputs and outputs"
  def addPatternToGene(self):
    random.choice(self.genes).addPattern()
    return "Added a pattern to a gene"
  def removePatternFromGene(self):
    random.choice(self.genes).removePattern()
    return "Removed a pattern from a gene"
  def removeUnusedPattern(self):
    unusedPatterns = [pattern for pattern in self.patterns]
    for gene in self.genes:
      for pattern in gene.patterns:
        if pattern in unusedPatterns:
          unusedPatterns.remove(pattern)
    if len(unusedPatterns) > 0:
      self.patterns.remove( random.choice(unusedPatterns) )
    return "Removed an unused pattern"
  def __str__(self):
    retStr = ":".join(["g", self.id, str(self.inputs), str(self.outputs)]) + "\n"
    retStr += "".join([str(pattern) for pattern in self.patterns])
    retStr += "".join([str(gene) for gene in self.genes])
    return retStr
  
class Gene(object):    
    def __init__(self, genome, numberOfPatterns = None):
      if numberOfPatterns == None: numberOfPatterns = random.randint(*config.geneDefaultNumberOfPatternsRange)
      self.genome = genome
      self.patterns = [random.choice(genome.patterns) for i in range(numberOfPatterns)]
      self.remap()
    def __str__(self):
      retStr = "x:" + ":".join([str(i) for i in self.inputMap]) + "\n"
      retStr += "y:" + ":".join([str(i) for i in self.outputMap]) + "\n"
      retStr += "z:" + ":".join([str(self.genome.patterns.index(pattern)) for pattern in self.patterns]) + "\n"
      return retStr
    def remap(self):
      inputs = range(self.genome.inputs)
      self.inputMap = [random.choice(inputs) for i in self.patterns[0].inputs]
      outputs = range(self.genome.outputs)
      self.outputMap = [random.choice(outputs) for i in self.patterns[-1].outputs]
    def addPattern(self):
      pattern = random.choice(self.genome.patterns)
      position = random.randint(0,len(self.patterns))
      self.patterns.insert(position, pattern)
      if position == 0 or position + 1 == len(self.patterns): self.remap()
    def removePattern(self):
      if len(self.patterns) == 1 : return
      position = random.randint(0,len(self.patterns)-1)
      self.patterns.pop(position)
      if position == 0 or position == len(self.patterns): self.remap()
        
class Pattern(object):
  def __init__(self, inputs, outputs, hidden):
    self.inputs = [PatternNeuron() for i in range(inputs)]
    self.outputs = [PatternNeuron() for i in range(outputs)]
    self.hidden = [PatternNeuron() for i in range(hidden)]
    self.neurons = self.inputs + self.outputs + self.hidden
    for hidden in self.hidden:
      for input in self.inputs:
        hidden.addSynapse(input, 0.0)
      for ouput in self.outputs:
        ouput.addSynapse(hidden, 0.0)
      for h2hidden in self.hidden:
        hidden.addSynapse(h2hidden, 0.0)
    for ouput in self.outputs:
      for input in self.inputs:
        ouput.addSynapse(input, 0.0)
  def perturbSynapseWeights(self, maxDisturbance, disturbanceProbability):
    for neuron in self.neurons:
      for synapseNeuron in neuron.synapses:
        if random.random() < disturbanceProbability : neuron.synapses[synapseNeuron] += maxDisturbance*( random.random()*2 - 1)
  def perturbInitialVals(self, maxDisturbance, disturbanceProbability):
    for neuron in self.neurons:
      if random.random() < disturbanceProbability : neuron.val += maxDisturbance * (random.random()*2 + 1)
  def perturbBiases(self, maxDisturbance, disturbanceProbability):
    for neuron in self.neurons:
      if random.random() < disturbanceProbability : neuron.bias += maxDisturbance * (random.random()*2 + 1)    
  def addNeuron(self):
    neuron = PatternNeuron()
    self.hidden.append( neuron )
    self.neurons.append( neuron )
    for input in self.inputs:
      neuron.addSynapse(input, 0.0)
    for ouput in self.outputs:
      ouput.addSynapse(neuron, 0.0)
    for hidden in self.hidden:
      hidden.addSynapse(neuron, 0.0)
      neuron.addSynapse(hidden, 0.0)
  def removeNeuron(self):
    if len(self.hidden) == 0: return
    neuron = random.choice(self.hidden)
    self.hidden.remove(neuron)
    self.neurons.remove(neuron)
    for otherNeuron in self.neurons:
      if neuron in otherNeuron.synapses: del otherNeuron.synapses[neuron]
  def __str__(self):
    retStr = ":".join(["p", str(len(self.inputs)), str(len(self.outputs))]) + "\n"
    retStr += "".join([str(neuron) for neuron in self.neurons])
    return retStr
      
class PatternNeuron(object):
  def __init__(self, val = 0.0, bias = 0.0):
    self.synapses = {}
    self.val = val
    self.bias = bias
    self.id = getId()
  def addSynapse(self, neuron, weight):
    self.synapses[neuron] = weight
  def __str__(self):
    retStr = [ ":".join(["n", str(self.val), str(self.bias), self.id]) ]
    retStr += [ ":".join(["s", neuron.id, str(self.synapses[neuron])]) for neuron in self.synapses]
    return "\n".join( retStr ) + "\n"
    
class CopyGenome(Genome):
  def __init__(self, parent):
    self.inputs = parent.inputs
    self.outputs = parent.outputs
    self.patterns = [CopyPattern(pattern) for pattern in parent.patterns]
    self.genes = [CopyGene(self, gene) for gene in parent.genes]
    self.id = getId()
    
class CopyPattern(Pattern):
  def __init__(self, parent):
    self.inputs = [CopyPatternNeuron(patternNeuron) for patternNeuron in parent.inputs]
    self.outputs = [CopyPatternNeuron(patternNeuron) for patternNeuron in parent.outputs]
    self.hidden = [CopyPatternNeuron(patternNeuron) for patternNeuron in parent.hidden]
    self.neurons = self.inputs + self.outputs + self.hidden
    for neuron, parentNeuron in zip(self.neurons, parent.neurons):
      for synapseNeuron in parentNeuron.synapses:
        mappedNeuron = self.neurons[ parent.neurons.index(synapseNeuron) ]
        neuron.addSynapse(mappedNeuron, parentNeuron.synapses[synapseNeuron])
    
class CopyPatternNeuron(PatternNeuron):
  def __init__(self, parent):
    self.synapses = {}
    self.val = parent.val
    self.bias = parent.bias
    self.id = getId()
    
class CopyGene(Gene):
  def __init__(self, genome, parent):
    self.patterns = [genome.patterns[ parent.genome.patterns.index(pattern) ] for pattern in parent.patterns]
    self.inputMap = [i for i in parent.inputMap]
    self.outputMap = [i for i in parent.outputMap]
    self.genome = genome
    self.id = getId()
    
class GenomeFactory(Genome):
  def __init__(self, genomeString):
    self.genes = []
    self.patterns = []
    genomeString = genomeString.split("\n")
    genomeString = [line.split(":") for line in genomeString][:-1]
    control = {
      'n': self._addNeuron,
      's': self._saveSynapseData,
      'g': self._setIO,
      'x': self._addGene,
      'y': self._geneOuputMap,
      'z': self._genePatternMap,
      'p': self._addPattern
    }
    self._patternSynapseMap = {}
    self._geneToPatternMaps = []
    self._patternNeuronMap = {}
    self._cursor = {}
    for command in genomeString:
      control[command[0]](command[1:])
    self._completeGeneToPatternMap()
    self._completePatternSynapseMap()
    self._patternIOs()
    del self._patternSynapseMap
    del self._geneToPatternMaps
    del self._patternNeuronMap
    del self._cursor
  def _addNeuron(self, data):
    neuron = NeuronFactory(float(data[0]), float(data[1]), data[2])
    self._cursor['neuron'] = neuron
    self._cursor['pattern'].neurons.append(neuron)
    self._patternNeuronMap[self._cursor['pattern']][neuron.id] = neuron
  def _saveSynapseData(self, data):
    self._patternSynapseMap[self._cursor['pattern']].append((self._cursor['neuron'], data[0], float(data[1])))
  def _setIO(self, data):
    self.id = data[0]
    self.inputs = int(data[1])
    self.outputs = int(data[2])
  def _addGene(self, data):
    self._cursor['gene'] = GeneFactory(data, self)
    self.genes.append( self._cursor['gene'] )
  def _geneOuputMap(self, data):
    self._cursor['gene'].outputMap = [int(i) for i in data]
  def _genePatternMap(self, data):
    self._geneToPatternMaps.append( (self._cursor['gene'], [int(i) for i in data]) )
  def _addPattern(self, data):
    pattern = PatternFactory()
    self._cursor['pattern'] = pattern
    pattern.inputs = int(data[0])
    pattern.outputs = int(data[1])
    self.patterns.append( pattern )
    self._patternNeuronMap[pattern] = {}
    self._patternSynapseMap[pattern] = []
  def _completeGeneToPatternMap(self):
    for gene, data in self._geneToPatternMaps:
      for index in data:
        gene.patterns.append( self.patterns[index] )
  def _completePatternSynapseMap(self):
    for pattern in self.patterns:
      for neuron, id, weight in self._patternSynapseMap[pattern]:
        neuron.addSynapse( self._patternNeuronMap[pattern][id] ,weight)
  def _patternIOs(self):
    for pattern in self.patterns:
      inputs = pattern.inputs
      outputs = pattern.outputs
      pattern.inputs = pattern.neurons[:inputs]
      pattern.outputs = pattern.neurons[inputs:inputs+outputs]
      pattern.hidden = pattern.neurons[inputs+outputs:]
    
class NeuronFactory(PatternNeuron):
  def __init__(self, val, bias, id):
    self.synapses = {}
    self.val = val
    self.bias = bias
    self.id = id
    
class GeneFactory(Gene):
  def __init__(self, inputMap, genome):
    self.inputMap = [int(i) for i in inputMap]
    self.patterns = []
    self.genome = genome
    
class PatternFactory(Pattern):
  def __init__(self):
    self.neurons = []