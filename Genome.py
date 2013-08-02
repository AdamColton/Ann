import random

class Genome:
  def __init__(self, inputs, outputs):
    self.inputs = inputs
    self.outputs = outputs
    fragments = 10
    self.fragments = [Pattern(random.randint(0,5),random.randint(0,5),random.randint(0,5),random.random()*0.5 + 0.25) for i in range(fragments)]
    self.genes = [Gene(self) for i in range(10)]

class Gene:    
    def __init__(self, parent):
      pass
        
        
class Pattern:
  def __init__(self, inputs, outputs, hidden, density):
    self.inputs = [PatternNeuron() for i in range(inputs)]
    self.outputs = [PatternNeuron() for i in range(outputs)]
    self.hidden = [PatternNeuron() for i in range(hidden)]
    for hidden in self.hidden:
      for input in self.inputs:
        if random.random() < density:
          hidden.addSynapse(input, random.random())
      for ouput in self.outputs:
        if random.random() < density:
          ouput.addSynapse(hidden, random.random())
      for h2hidden in self.outputs:
        if h2hidden != hidden and random.random() < density:
          hidden.addSynapse(h2hidden, random.random())
    for ouput in self.outputs:
      for input in self.inputs:
        if random.random() < density:
          ouput.addSynapse(input, random.random())
          
class PatternNeuron:
  def __init__(self, val = 0, bias = 0):
    self.synapses = []
    self.val = val
    self.bias = bias
    self.id = str(random.randint(0,2**30))
  def addSynapse(self, neuron, weight):
    self.synapses.append( (neuron, weight) )
    
class Scaffold:
  def __init__(self, inputs, outputs, patterns, network):
    self.mapping = {}
    #if there's more neural inputs than pattern[0] inputs -> ignore extra neural inputs
    #if there's more pattern[0] inputs, than neural inputs, multiple pattern[0] inputs will map to one neural inputs
    numberOfInputs = min( len(inputs), len(patterns[0].inputs) )
    self.inputs = [inputs[i] for i in range(numberOfInputs)]
    for i in range(len(pattern[0].inputs)):
      self.mapping['0_' + patterns[0].inputs[i].id] = self.inputs[i%numberOfInputs]
    
    numberOfOutputs = min( len(outputs), len(patterns[-1].outputs) )
    self.outputs = [outputs[i] for i in range(numberOfOutputs)]
    for i in range(len(patterns[-1].outputs)):
      self.mapping[str(len(patterns)-1) + '_' + patterns[-1].outputs[i].id] = self.outputs[i%numberOfOutputs]
      
  def _mapHiddenNodes(self, patterns, network):
    for i in range(len(patterns)):
      for hidden in patterns[i].hidden:
        self.mapping[str(i) + "_" + hidden.id] = network.addNeuron()
  def _mapIOnodes(self, patterns, network):
    for i in range(len(patterns)-1):
      outputs = patterns[i].outputs
      inputs = pattern[i+1].inputs
      numberOfNeurons = min(outputs, inputs)
      neurons = [network.addNeuron() for i in range(numberOfNeurons)]
      for j in range(len(outputs)):
        self.mapping[str(i) + "_" + outputs[j].id] = neurons[j%numberOfNeurons]
      for j in range(len(inputs)):
        self.mapping[str(i+1) + "_" + inputs[j].id] = neurons[j%numberOfNeurons]