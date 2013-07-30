e = 2.71828182845904523536
logistic = lambda x: 1 / (1 + e**(-x))


class ObjectNet:
  def __init__(self, inputs, outputs):
    self.inputs = [Neuron() for i in range(inputs)]
    self.outputs = [Neuron() for i in range(outputs)]
    self.hidden = []
  def input(self, input):
    if ( len(input) != len(self.inputs)): return False
    for neuron, val in zip(self.inputs, input):
      neuron.val = val
  def addNeuron(self):
    neuron = Neuron()
    self.hidden.append(neuron)
    return neuron
  def calculate(self, steps = 1):
    for i in range(steps):
      for neuron in self.hidden:
        neuron.calculate()
      for neuron in self.outputs:
        neuron.calculate()
      for neuron in self.hidden:
        neuron.step()
      for neuron in self.outputs:
        neuron.step()
      
class Neuron:
  def __init__(self, val = 0, bias = 0):
    self.synapses = []
    self.val = val
    self.bias = bias
  def addSynapse(self, neuron, weight):
    self.synapses.append( (neuron, weight) )
  def calculate(self):
    self._val = self.bias
    for neuron, weight in self.synapses:
      self._val += neuron.val * weight
  def step(self):
    self.val = logistic(self._val)
    
class ArrayNet:
  def __init__(self, inputs, outputs):
    neurons = inputs + outputs
    self.inputs = inputs
    self.outputs = outputs
    self.neurons = [0 for i in range(neurons)]
    self.synapses = [ [0 for j in range(neurons)] for i in range(outputs)]
  def input(self, input):
    if ( len(input) != self.inputs): return False
    for i in range(self.inputs):
      self.neurons[i] = input[i]
  def calculate(self):
    newVals = [self.neurons[i] for i in range(self.inputs)]
    neurons = len(self.neurons)
    for i in range(neurons - self.inputs):
      newVal = 0
      for j in range(neurons):
        if i+self.inputs == j :
          newVal += self.synapses[i][j]
        else :
          newVal += self.synapses[i][j] * self.neurons[j]
      newVals.append(logistic(newVal))
    self.neurons = newVals