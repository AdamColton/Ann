import Ann
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
    ann.input( [1,2] )
    ann.hidden[0].addSynapse( ann.inputs[0], 3)
    ann.hidden[0].addSynapse( ann.inputs[1], 4)
    ann.outputs[0].addSynapse( ann.hidden[0], 5)
    ann.outputs[1].addSynapse( ann.hidden[0], 6)
    ann.calculate(2)
    l11 = Ann.logistic(11)
    self.assertEqual( Ann.logistic(l11*5), ann.outputs[0].val)
    self.assertEqual( Ann.logistic(l11*6), ann.outputs[1].val)
    
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
unittest.main()