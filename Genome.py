import random

# Right now there are a lot of magic numbers in here. These need to be pulled out.

class Genome:
  def __init__(self):
    patterns = 10
    self.patterns = [Pattern(random.randint(1,5),random.randint(1,5),random.randint(0,5),random.random()*0.5 + 0.25) for i in range(patterns)]
    self.genes = [Gene(self) for i in range(10)]
  def apply(self, network):
    for gene in self.genes:
      self._applyGene(gene.patterns, network)
  def _applyGene(self, patterns, network):
    mapping = {}
    
    numberOfInputs = min( len(network.inputs), len(patterns[0].inputs) )
    inputs = [network.inputs[i] for i in range(numberOfInputs)]
    for i in range(len(patterns[0].inputs)):
      mapping['0_' + patterns[0].inputs[i].id] = inputs[i%numberOfInputs]
    
    numberOfOutputs = min( len(network.outputs), len(patterns[-1].outputs) )
    outputs = [network.outputs[i] for i in range(numberOfOutputs)]
    for i in range(len(patterns[-1].outputs)):
      mapping[str(len(patterns)-1) + '_' + patterns[-1].outputs[i].id] = outputs[i%numberOfOutputs]
    
    self._mapHiddenNodes(patterns, network, mapping)
    self._mapIOnodes(patterns, network, mapping)
    self._mapSynapses(patterns, mapping)
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

class Gene:    
    def __init__(self, parent):
      patterns = random.randint(1,5)
      self.patterns = [random.choice(parent.patterns) for i in range(patterns)]
        
        
class Pattern:
  def __init__(self, inputs, outputs, hidden, density):
    self.inputs = [PatternNeuron() for i in range(inputs)]
    self.outputs = [PatternNeuron() for i in range(outputs)]
    self.hidden = [PatternNeuron() for i in range(hidden)]
    self.neurons = self.inputs + self.outputs + self.hidden
    for hidden in self.hidden:
      for input in self.inputs:
        if random.random() < density:
          hidden.addSynapse(input, random.random()*2 - 1)
      for ouput in self.outputs:
        if random.random() < density:
          ouput.addSynapse(hidden, random.random()*2 - 1)
      for h2hidden in self.outputs:
        if h2hidden != hidden and random.random() < density:
          hidden.addSynapse(h2hidden, random.random()*2 - 1)
    for ouput in self.outputs:
      for input in self.inputs:
        if random.random() < density:
          ouput.addSynapse(input, random.random()*2 - 1)
          
class PatternNeuron:
  def __init__(self, val = 0, bias = 0):
    self.synapses = []
    self.val = val
    self.bias = bias
    self.id = str(random.randint(0,2**30))
  def addSynapse(self, neuron, weight):
    self.synapses.append( (neuron, weight) )