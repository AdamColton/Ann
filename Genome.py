import random
import Ann


"""
Todos:
* Pull magic numbers out into constants
* Gene mutation
** remove pattern
** copy & remap
** remap
* Pattern mutation
** Perturb biases

I would like a mechanism where a gene expression passes data into a gene at the time that it is expressed.
Think of fingers and toes. Toes are different than fingers and they all have different lengths, but they
could all be expressed with the same gene. They just need a finger/toe switch and a size parameter.
"""

class Genome:
  patterns = 10
  def __init__(self, inputs, outputs):
    self.inputs = inputs
    self.outputs = outputs
    self.patterns = [Pattern(random.randint(1,5),random.randint(1,5),random.randint(1,5)) for i in range(Genome.patterns)]
    self.genes = [Gene(self) for i in range(10)]
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
        for synapse in neuron.synapses:
          synapseNeuron = mapping[str(i) +  '_' + synapse[0].id]
          mapping[str(i) +  '_' + neuron.id].addSynapse(synapseNeuron, synapse[1])
  def mutate(self):
    random.choice([
      self.perturbSynapseWeights,
      self.newGene,
      self.newPattern,
      self.perturbInitialVals,
      self.perturbBiases
    ])()
  def perturbSynapseWeights(self, maxDisturbance = 0.01, disturbanceProbability = 0.01):
    for pattern in self.patterns:
      pattern.perturbSynapseWeights(maxDisturbance, disturbanceProbability)
  def perturbInitialVals(self, maxDisturbance = 0.01, disturbanceProbability = 0.01):
    for pattern in self.patterns:
      pattern.perturbInitialVals(maxDisturbance, disturbanceProbability)
  def perturbBiases(self, maxDisturbance = 0.01, disturbanceProbability = 0.01):
    for pattern in self.patterns:
      pattern.perturbBiases(maxDisturbance, disturbanceProbability)
  def newGene(self):
    self.genes.append(Gene(self))
  def newPattern(self):
    self.patterns.append( Pattern(random.randint(1,5),random.randint(1,5),random.randint(1,5)) )
  
class Gene:    
    def __init__(self, genome):
      patterns = random.randint(1,5)
      self.genome = genome
      self.patterns = [random.choice(genome.patterns) for i in range(patterns)]
      inputs = range(genome.inputs)
      self.inputMap = [random.choice(inputs) for i in self.patterns[0].inputs]
      outputs = range(genome.outputs)
      self.outputMap = [random.choice(outputs) for i in self.patterns[-1].outputs]
        
class Pattern:
  def __init__(self, inputs, outputs, hidden):
    self.inputs = [PatternNeuron() for i in range(inputs)]
    self.outputs = [PatternNeuron() for i in range(outputs)]
    self.hidden = [PatternNeuron() for i in range(hidden)]
    self.neurons = self.inputs + self.outputs + self.hidden
    for hidden in self.hidden:
      for input in self.inputs:
        hidden.addSynapse(input, 0)
      for ouput in self.outputs:
        ouput.addSynapse(hidden, 0)
      for h2hidden in self.outputs:
        hidden.addSynapse(h2hidden, 0)
    for ouput in self.outputs:
      for input in self.inputs:
        ouput.addSynapse(input, 0)
  def perturbSynapseWeights(self, maxDisturbance, disturbanceProbability):
    for neuron in self.neurons:
      for synapse in neuron.synapses:
        if random.random() < disturbanceProbability : synapse[1] += maxDisturbance*( random.random()*2 - 1 )
  def perturbInitialVals(self, maxDisturbance, disturbanceProbability):
    for neuron in self.neurons:
      if random.random() < disturbanceProbability : neuron.val += maxDisturbance * (random.random()*2 + 1)
  def perturbBiases(self, maxDisturbance, disturbanceProbability):
    for neuron in self.neurons:
      if random.random() < disturbanceProbability : neuron.bias += maxDisturbance * (random.random()*2 + 1)    
      
class PatternNeuron:
  def __init__(self, val = 0, bias = 0):
    self.synapses = []
    self.val = val
    self.bias = bias
    self.id = str(random.randint(0,2**30))
  def addSynapse(self, neuron, weight):
    self.synapses.append( [neuron, weight] )
    
class CopyGenome(Genome):
  def __init__(self, parent):
    self.inputs = parent.inputs
    self.outputs = parent.outputs
    self.patterns = [CopyPattern(pattern) for pattern in parent.patterns]
    self.genes = [CopyGene(self, gene) for gene in parent.genes]
    
class CopyPattern(Pattern):
  def __init__(self, parent):
    self.inputs = [CopyPatternNeuron(patternNeuron) for patternNeuron in parent.inputs]
    self.outputs = [CopyPatternNeuron(patternNeuron) for patternNeuron in parent.outputs]
    self.hidden = [CopyPatternNeuron(patternNeuron) for patternNeuron in parent.hidden]
    self.neurons = self.inputs + self.outputs + self.hidden
    for neuron, parentNeuron in zip(self.neurons, parent.neurons):
      for synapse in parentNeuron.synapses:
        mappedNeuron = self.neurons[ parent.neurons.index(synapse[0]) ]
        neuron.addSynapse(mappedNeuron, synapse[1])
    
class CopyPatternNeuron(PatternNeuron):
  def __init__(self, parent):
    self.synapses = []
    self.val = parent.val
    self.bias = parent.bias
    self.id = str(random.randint(0,2**30))
    
class CopyGene(Gene):
  def __init__(self, genome, parent):
    self.patterns = [genome.patterns[ parent.genome.patterns.index(pattern) ] for pattern in parent.patterns]
    self.inputMap = [i for i in parent.inputMap]
    self.outputMap = [i for i in parent.outputMap]