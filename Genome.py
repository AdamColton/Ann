import random

# Right now there are a lot of magic numbers in here. These need to be pulled out.

class Genome:
  def __init__(self):
    patterns = 10
    self.patterns = [Pattern(random.randint(1,5),random.randint(1,5),random.randint(0,5),random.random()*0.5 + 0.25) for i in range(patterns)]
    self.genes = [Gene(self) for i in range(10)]
  def apply(self, network):
    for gene in self.genes:
      Scaffold(gene.patterns, network)

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
    
class Scaffold:
  def __init__(self, patterns, network):
    inputs = network.inputs
    outputs = network.outputs
    self.mapping = {}
    
    numberOfInputs = min( len(inputs), len(patterns[0].inputs) )
    self.inputs = [inputs[i] for i in range(numberOfInputs)]
    for i in range(len(patterns[0].inputs)):
      self.mapping['0_' + patterns[0].inputs[i].id] = self.inputs[i%numberOfInputs]
    
    numberOfOutputs = min( len(outputs), len(patterns[-1].outputs) )
    self.outputs = [outputs[i] for i in range(numberOfOutputs)]
    for i in range(len(patterns[-1].outputs)):
      self.mapping[str(len(patterns)-1) + '_' + patterns[-1].outputs[i].id] = self.outputs[i%numberOfOutputs]
    
    self._mapHiddenNodes(patterns, network)
    self._mapIOnodes(patterns, network)
    self._mapSynapses(patterns)
  def _mapHiddenNodes(self, patterns, network):
    for i in range(len(patterns)):
      for hidden in patterns[i].hidden:
        self.mapping[str(i) + "_" + hidden.id] = network.addNeuron()
  def _mapIOnodes(self, patterns, network):
    for i in range(len(patterns)-1):
      outputs = patterns[i].outputs
      inputs = patterns[i+1].inputs
      numberOfNeurons = min(len(outputs), len(inputs))
      neurons = [network.addNeuron() for i in range(numberOfNeurons)]
      for j in range(len(outputs)):
        self.mapping[str(i) + "_" + outputs[j].id] = neurons[j%numberOfNeurons]
      for j in range(len(inputs)):
        self.mapping[str(i+1) + "_" + inputs[j].id] = neurons[j%numberOfNeurons]
  def _mapSynapses(self, patterns):
    for i in range(len(patterns)):
      for neuron in patterns[i].neurons:
        for synapse in neuron.synapses:
          synapseNeuron = self.mapping[str(i) +  '_' + synapse[0].id]
          self.mapping[str(i) +  '_' + neuron.id].addSynapse(synapseNeuron, synapse[1])