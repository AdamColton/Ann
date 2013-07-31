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
    self.inputs = [Neuron() for i in range(inputs)]
    self.outputs = [Neuron() for i in range(outputs)]
    self.hidden = [Neuron() for i in range(hidden)]
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
          
class Neuron:
  def __init__(self, val = 0, bias = 0):
    self.synapses = []
    self.val = val
    self.bias = bias
  def addSynapse(self, neuron, weight):
    self.synapses.append( (neuron, weight) )