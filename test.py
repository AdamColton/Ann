import Ann
import Genome
import unittest

class TestHelperFunctions(unittest.TestCase):
  def test_logisticOfzero_EqualsOneHalf(self):
    logisticZero = Ann.logistic(0)
    self.assertTrue( abs(logisticZero-0.5) < 0.0001, "Ann.logistic(0) should be 0.5 +/- 0.0001, got " + str(logisticZero) )

class TestObjectNet(unittest.TestCase):
  def test_settingInputs(self):
    ann = Ann.ObjectNet(3,0)
    ann.input( [1,2,3] );
    [self.assertEqual(neuron.val, val) for (neuron, val) in zip(ann.inputs, [1,2,3])]
  def test_addSynapse(self):
    ann = Ann.ObjectNet(2,0)
    ann.inputs[0].addSynapse( ann.inputs[1], 1)
    self.assertEqual( len(ann.inputs[0].synapses), 1)
  def test_calculate(self):
    ann = Ann.ObjectNet(1,1)
    ann.outputs[0].addSynapse( ann.inputs[0], 3)
    ann.input( [2] )
    ann.calculate()
    self.assertEqual( Ann.logistic(6), ann.outputs[0].val)
  def test_calculate_withAddNeuron(self):
    ann = Ann.ObjectNet(2,2)
    ann.addNeuron()
    ann.input( [7,2] )
    ann.hidden[0].addSynapse( ann.inputs[0], 3)
    ann.hidden[0].addSynapse( ann.inputs[1], 4)
    ann.outputs[0].addSynapse( ann.hidden[0], 5)
    ann.outputs[1].addSynapse( ann.hidden[0], 6)
    ann.calculate(2)
    L_29 = Ann.logistic(29)
    self.assertEqual( Ann.logistic(L_29*5), ann.outputs[0].val)
    self.assertEqual( Ann.logistic(L_29*6), ann.outputs[1].val)
  def test_arrayNet(self):
    ann = Ann.ObjectNet(2,2)
    ann.addNeuron()
    ann.input( [7,2] )
    ann.hidden[0].addSynapse( ann.inputs[0], 3)
    ann.hidden[0].addSynapse( ann.inputs[1], 4)
    ann.outputs[0].addSynapse( ann.hidden[0], 5)
    ann.outputs[1].addSynapse( ann.hidden[0], 6)
    arrayNet = ann.arrayNet()
    arrayNet.calculate(4)
    ann.calculate(4)
    self.assertEqual(ann.outputs[0].val, arrayNet.neurons[arrayNet.inputs + 0])
    
class TestArrayNet(unittest.TestCase):
  def test_settingInputs(self):
    ann = Ann.ArrayNet(3,0)
    ann.input( [1,2,3] );
    [self.assertEqual(neuronVal, val) for (neuronVal, val) in zip(ann.neurons[:2], [1,2,3])]
  def test_calculate(self):
    ann = Ann.ArrayNet(1,1)
    ann.input( [2] )
    ann.synapses[0][0] = 3
    ann.calculate()
    self.assertEqual( Ann.logistic(6), ann.neurons[1])
  def test_calculate_advanced(self):
    ann = Ann.ArrayNet(2,2)
    ann.input( [2,3] )
    ann.synapses[0][0] = 5
    ann.synapses[0][1] = 11
    ann.synapses[1][0] = 7
    ann.synapses[1][1] = 13
    ann.calculate()
    self.assertEqual( Ann.logistic(2*5+3*11), ann.neurons[2])
    self.assertEqual( Ann.logistic(2*7+3*13), ann.neurons[3])
  def test_calculate_advanced(self):
    ann = Ann.ArrayNet(2,2)
    ann.input( [2,3] )
    ann.synapses[0][0] = 5
    ann.synapses[0][1] = 11
    ann.synapses[1][0] = 7
    ann.synapses[1][1] = 13 
    ann.addNeurons(4)
    ann.calculate()
    self.assertEqual( Ann.logistic(2*5+3*11), ann.neurons[2])
    self.assertEqual( Ann.logistic(2*7+3*13), ann.neurons[3])
    
class TestGenome(unittest.TestCase):
  def test_genome(self):
    genome = Genome.Genome(4,4)
    self.assertEqual( len(genome.genes[0].inputMap), len(genome.genes[0].patterns[0].inputs))
    self.assertEqual( len(genome.genes[0].outputMap), len(genome.genes[0].patterns[-1].outputs))
    ann = genome.generate()
    self.assertTrue(  len(ann.hidden) > 0 )
  def test_copy(self):
    genome1 = Genome.Genome(4,4)
    genome1.perturbSynapseWeights(1,1)
    genome2 = Genome.CopyGenome(genome1)
    ann1 = genome1.generate()
    ann2 = genome2.generate()
    ann1.calculate(50)
    ann2.calculate(50)
    self.assertEqual(ann1.outputs[0].val, ann2.outputs[0].val)
    self.assertEqual(genome1.patterns[0].hidden[0].synapses[0][1], genome2.patterns[0].hidden[0].synapses[0][1])
    
unittest.main()