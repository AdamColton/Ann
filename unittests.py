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
  def test_withSingleHiddenNode(self):
    ann = Ann.ObjectNet(1,1)
    hidden = ann.addNeuron()
  def test_calculate_withAddNeuron(self):
    ann = Ann.ObjectNet(2,2)
    ann.addNeuron()
    ann.input( [7,2] )
    ann.hidden[0].addSynapse( ann.inputs[0], 3)
    ann.hidden[0].addSynapse( ann.inputs[1], 4)
    ann.outputs[0].addSynapse( ann.hidden[0], 5)
    ann.outputs[1].addSynapse( ann.hidden[0], 6)
    ann.calculate(2)
    self.assertEqual( Ann.logistic(5), ann.outputs[0].val)
    self.assertEqual( Ann.logistic(6), ann.outputs[1].val)
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
    pattern1 = genome1.patterns[0]
    pattern2 = genome2.patterns[0]
    self.assertEqual(pattern1.hidden[0].synapses[pattern1.inputs[0]], pattern2.hidden[0].synapses[pattern2.inputs[0]])
  def test_mutate(self):
    genome = Genome.Genome(4,4)
    for i in range(100):
      genome.mutate()
    ann = genome.generate()
  def test_newGene(self):
    genome = Genome.Genome(4,4)
    genes = len( genome.genes )
    genome.newGene()
    self.assertEqual(genes + 1, len(genome.genes))
  def test_newPattern1(self):
    genome = Genome.Genome(4,4)
    patterns = len(genome.patterns)
    genome.newPattern()
    self.assertEqual(patterns + 1, len(genome.patterns))
  def test_patternNeuronStr(self):
    genome = self.getConstructedGenome()
    neuronString = str(genome.patterns[0].outputs[0])
    expectedSegments = [
      'n:4.1:4.2:0004',
      's:0002:4.0',
      's:0003:5.0',
      's:0001:3.0'
    ]
    for segment in expectedSegments:
      self.assertIn(segment, neuronString)
  def test_patternStr(self):
    genome = self.getConstructedGenome()
    patternString = str(genome.patterns[0])
    expectedSegments = [
      'p:2:2',
      'n:4.1:4.2:0004',
      's:0003:5.0',
      's:0001:3.0',
      's:0002:4.0',
      'n:5.1:5.2:0004',
      's:0003:5.0',
      's:0001:3.0',
      's:0002:4.0',
      'n:1.1:1.2:0001',
      'n:2.1:2.2:0002',
      'n:3.1:3.2:0003',
      's:0001:1.0',
      's:0002:2.0'
    ]
    for segment in expectedSegments:
      self.assertIn(segment, patternString)
  def test_saveAndRestoreGenome(self):
    genome = self.getConstructedGenome()
    genomeString = str(genome)
    clonedGenome = Genome.GenomeFactory(genomeString)
    clonedGenomeString = str(clonedGenome).split("\n")
    for line in clonedGenomeString:
      self.assertTrue(line in genomeString)
  def test_saveAndRestoreGenome2(self):
    genome1 = Genome.Genome(4,4)
    for i in range(100):
      genome1.mutate()
    genome1string = str(genome1)
    genome2 = Genome.GenomeFactory(genome1string)
    genome2string = str( genome2 ).split("\n")
    for line in genome2string:
      self.assertTrue(line in genome1string)
  def test_perturbSynapseWeights(self):
    genome = self.getConstructedGenome()
    before = genome.patterns[0].outputs[0].synapses[genome.patterns[0].hidden[0]]
    genome.perturbSynapseWeights(1,0)
    after = genome.patterns[0].outputs[0].synapses[genome.patterns[0].hidden[0]]
    self.assertEqual(before, after)
    genome.perturbSynapseWeights(1,1)
    after = genome.patterns[0].outputs[0].synapses[genome.patterns[0].hidden[0]]
    self.assertNotEqual(before, after)
  def test_perturbInitialVals(self):
    genome = self.getConstructedGenome()
    before = genome.patterns[0].hidden[0].val
    genome.perturbInitialVals(1,0)
    after = genome.patterns[0].hidden[0].val
    self.assertEqual(before, after)
    genome.perturbInitialVals(1,1)
    after = genome.patterns[0].hidden[0].val
    self.assertNotEqual(before, after)
  def test_perturbBiases(self):
    genome = self.getConstructedGenome()
    before = genome.patterns[0].hidden[0].bias
    genome.perturbBiases(1,0)
    after = genome.patterns[0].hidden[0].bias
    self.assertEqual(before, after)
    genome.perturbBiases(1,1)
    after = genome.patterns[0].hidden[0].bias
    self.assertNotEqual(before, after)
  def test_addNeuron(self):
    genome = self.getConstructedGenome()
    before = len(genome.patterns[0].hidden)
    genome.addNeuron()
    after = len(genome.patterns[0].hidden)
    self.assertEqual(before + 1, after)
  def test_removeNeuron(self):
    genome = self.getConstructedGenome()
    before = len(genome.patterns[0].hidden)
    genome.removeNeuron()
    after = len(genome.patterns[0].hidden)
    self.assertEqual(before - 1, after)
  def test_remapGene(self):
    genome = self.getConstructedGenome()
    inputBefore = genome.genes[0].inputMap
    outputsBefore = genome.genes[0].outputMap
    genome.remapGene()
    inputAfter = genome.genes[0].inputMap
    outputsAfter = genome.genes[0].outputMap
    self.assertFalse(inputBefore is inputAfter)
    self.assertFalse(outputsBefore is outputsAfter)
  def test_copyGene(self):
    genome = self.getConstructedGenome()
    before = len(genome.genes)
    genome.copyGene()
    after = len(genome.genes)
    self.assertEqual(before+1, after)
  def test_addPatternToGene(self):
    genome = self.getConstructedGenome()
    before = len(genome.genes[0].patterns)
    genome.addPatternToGene()
    after = len(genome.genes[0].patterns)
    self.assertEqual(before+1, after)
  def test_removePatternFromGene(self):
    genome = self.getConstructedGenome()
    before = len(genome.genes[0].patterns)
    genome.addPatternToGene()
    genome.removePatternFromGene()
    after = len(genome.genes[0].patterns)
    self.assertEqual(before, after)
  def test_removeUnusedPattern(self):
    genome = self.getConstructedGenome()
    before = len(genome.patterns)
    genome.newPattern()
    genome.removeUnusedPattern()
    after = len(genome.patterns)
    self.assertEqual(before, after)
  def test_newPattern(self):
    genome = self.getConstructedGenome()
    before = len(genome.patterns)
    genome.newPattern()
    after = len(genome.patterns)
    self.assertEqual(before+1, after)
  def getConstructedGenome(self):
    genome = Genome.Genome(2,2,0,0)
    i1 = Genome.PatternNeuron(1.1,1.2)
    i1.id = "0001"
    i2 = Genome.PatternNeuron(2.1,2.2)
    i2.id = "0002"
    h1 = Genome.PatternNeuron(3.1,3.2)
    h1.id = "0003"
    o1 = Genome.PatternNeuron(4.1,4.2)
    o1.id = "0004"
    o2 = Genome.PatternNeuron(5.1,5.2)
    o2.id = "0004"
    h1.addSynapse(i1, 1.0)
    h1.addSynapse(i2, 2.0)
    o1.addSynapse(i1, 3.0)
    o1.addSynapse(i2, 4.0)
    o1.addSynapse(h1, 5.0)
    o2.addSynapse(i1, 3.0)
    o2.addSynapse(i2, 4.0)
    o2.addSynapse(h1, 5.0)
    pattern = Genome.Pattern(0, 0, 0)
    pattern.outputs = [o1,o2]
    pattern.inputs = [i1,i2]
    pattern.hidden = [h1]
    pattern.neurons = pattern.outputs + pattern.inputs + pattern.hidden
    genome.patterns = [pattern]
    gene = Genome.Gene(genome, 2)
    gene.inputMap = [0,1]
    gene.outputMap = [0,1]
    genome.genes = [gene]
    return genome


unittest.main()