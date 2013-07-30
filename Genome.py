import Ann

# geneome is an Ann constructor. It has genes and a set of fragments the genes instruct how to composite the fragments into a neural net
class Genome:
  def __init__(self, inputs, outputs):
    self.inputs = inputs
    self.outputs = outputs

# A fragment is a pattern for mapping a set of inputs through some number of hidden neurons, and to a set of ouputs
# the input and output neurons of a fragment do not need to be the input and output neurons of a neural net, they can be a subset
# or fragments can be stacked with the output of one serving as the input for the next.
class Fragment:
  def __init__(self, inputs, outputs, hidden):
    self.inputs = inputs
    self.outputs = outputs
    self.hidden = hidden