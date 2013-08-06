e = 2.71828182845904523536
logistic = lambda x: 1 / (1 + e**(-x))


class ObjectNet:
  def __init__(self, inputs, outputs):
    self.inputs = [Neuron(0,0,True) for i in range(inputs)]
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
    nonInputs = self.hidden + self.outputs
    for i in range(steps):
      for neuron in nonInputs:
        neuron.calculate()
      for neuron in nonInputs:
        neuron.step()
  def __str__(self):
    retStr = [" == Inputs =="]
    for i in range(len(self.inputs)):
      retStr.append( "I_" + str(i) + ": " + str(self.inputs[i].val))
      
    retStr.append(" == Hidden ==")
    for i in range(len(self.hidden)):
      hidden = self.hidden[i]
      retStr.append( "H_" + str(i) + ": " + str(hidden.val) + ", " + str(hidden.bias) )
      for synapseNeuron, weight in hidden.synapses:
        retStr.append("   " + self._getStrId(synapseNeuron) + ": " + str(weight) )
    
    retStr.append(" == Output ==")
    for i in range(len(self.outputs)):
      output = self.outputs[i]
      retStr.append( "H_" + str(i) + ": " + str(output.val) + ", " + str(output.bias))
      for synapseNeuron, weight in output.synapses:
        retStr.append("   " + self._getStrId(synapseNeuron) + ": " + str(weight) )
    return "\n".join(retStr)
  def _getStrId(self, neuron):
    if neuron in self.inputs: return "I_" + str(self.inputs.index(neuron))
    if neuron in self.outputs: return "O_" + str(self.outputs.index(neuron))
    if neuron in self.hidden: return "H_" + str(self.hidden.index(neuron))
    return "?_?"
  def arrayNet(self):
    arrayNet = ArrayNet(len(self.inputs), len(self.outputs), len(self.hidden))
    neurons = self.inputs + self.outputs + self.hidden
    inputs = len(self.inputs)
    for neuron in neurons:
      n = neurons.index(neuron)
      if n < arrayNet.inputs:
        arrayNet.neurons[n] = neuron.val
      else:
        arrayNet.neurons[n] = neuron.activation
      n -= inputs
      if n >= 0:
        arrayNet.synapses[n][n] = neuron.bias
        for synapse in neuron.synapses:
          s = neurons.index(synapse[0])
          v = synapse[1]
          arrayNet.synapses[n][s] = v
    return arrayNet
        
    
class Neuron:
  def __init__(self, val = 0, bias = 0, inputNeuron = False):
    self.synapses = []
    self.val = val
    self.activation = round(val)
    self.bias = bias
    self.inputNeuron = inputNeuron
  def addSynapse(self, neuron, weight):
    self.synapses.append( (neuron, weight) )
  def calculate(self):
    self._val = self.bias
    for neuron, weight in self.synapses:
      if neuron.inputNeuron:
        self._val += neuron.val * weight
      else:
        self._val += neuron.activation * weight
  def step(self):
    self.val = logistic(self._val)
    self.activation = round(self.val)
    
class ArrayNet:
  def __init__(self, inputs, outputs, hidden = 0):
    neurons = inputs + outputs + hidden
    self.inputs = inputs
    self.outputs = outputs
    self.neurons = [0 for i in range(neurons)]
    self.synapses = [ [0 for j in range(neurons)] for i in range(neurons-inputs)]
  def input(self, input):
    if ( len(input) != self.inputs): return False
    for i in range(self.inputs):
      self.neurons[i] = input[i]
  def calculate(self, iterations = 1):
    for iteration in range(iterations):
      newVals = [self.neurons[i] for i in range(self.inputs)]
      neurons = len(self.neurons)
      hidden = neurons - self.inputs - self.outputs
      for nonInputs in range(neurons - self.inputs):
        newVal = 0
        for neuron in range(neurons):
          if nonInputs+self.inputs == neuron :
            newVal += self.synapses[nonInputs][neuron] # bias
          else:
            newVal += self.synapses[nonInputs][neuron] * self.neurons[neuron]
        if nonInputs < hidden: newVal = round(newVal)
        newVals.append(logistic(newVal))
      self.neurons = newVals
  def addNeurons(self, neuronsToAdd = 1):
    oldNonInputNeuronCount = len(self.neurons) - self.inputs
    self.neurons += [0 for i in range(neuronsToAdd)]
    for i in range(oldNonInputNeuronCount):
      self.synapses[i] += [0 for j in range(neuronsToAdd)]
    newNonInputNeuronCount = oldNonInputNeuronCount + neuronsToAdd
    neurons = newNonInputNeuronCount + self.inputs
    for i in range(neuronsToAdd):
      self.synapses.append( [0 for j in range(neurons)] )