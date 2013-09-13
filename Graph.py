from PIL import Image
from PIL import ImageDraw

Width = 500
Height = 300
Max = 1
Fill = "rgb(0,0,0)"
Spacing = 10 #spacing between bars on a bar graph

def new(data = None):
  if data is None: data = []
  return Graph(data)

class Graph:
  def __init__(self, data = None):
    if data is None: data = []
    self.data = data
  def line_graph(self, name, strFill = None, maxValue = None, width = None, height = None):
    if strFill is None: strFill = Fill
    if maxValue is None: maxValue = Max
    if width is None: width = Width
    if height is None: height = Height    
    im = Image.new("RGBA",(width,height))
    draw = ImageDraw.Draw(im)
    xScale = float(width) / (len(self.data)-1)
    yScale = float(height) / maxValue
    index = 0
    lastX = 0
    lastY = height - int( self.data[0] * yScale ) - 1
    for value in self.data[1:]:
      index += 1
      y = Height - int( value*yScale ) - 1
      x = int( index*xScale )
      draw.line( (x,y , lastX,lastY), fill = strFill)
      lastY = y
      lastX = x
    im.save(name+".png","PNG")
  def bar_graph(self, name, strFill = None, maxValue = None, width = None, height = None):
    if strFill is None: strFill = Fill
    if maxValue is None: maxValue = Max
    if width is None: width = Width
    if height is None: height = Height
    im = Image.new("RGBA", (width,height) )
    draw = ImageDraw.Draw(im)
    bar_width = (width - Spacing * (len(self.data)+1) ) / len(self.data)
    c = 0
    for i in self.data:
      y = height - int( (float(i) / maxValue) * height ) - 1
      x_pos = Spacing + c * (Spacing + bar_width)
      draw.rectangle( (x_pos,height,x_pos+bar_width, y), fill = strFill)
      c += 1
    im.save(name+".png","PNG")