import copy

class Game(object):
  def __init__(self,board = None):
    if board == None:
      board = [ [0 for i in range(7)] for j in range(6) ]
    self.board = board
    self.turn = "white"
    self.gameOver = False
    self.winner = None
    self.moveCount = 0
  def flipBoard(self):
    for row in self.board:
      for i in range(len(row)):
        row[i] = -row[i]
  def getMove(self, i):
    returnBoard = copy.deepcopy(self.board)
    for m in range(5,-1,-1):
      if returnBoard[m][i] == 0:
        returnBoard[m][i] = 1
        return returnBoard
    return None
  def makeMove(self,i):
    tryMove = self.getMove(i)
    if tryMove:
      self.board = tryMove
    else:
      return False
    if (not self.gameOver) and self.checkForWin(i):
      self.gameOver = True
      self.winner = self.turn
    self.moveCount += 1
    if self.moveCount == 42:
      self.gameOver = True
      self.winner = "draw"
    if self.turn == "white":
      self.turn = "black"
    else:
      self.turn = "white"
    self.flipBoard()
    return True
  def display(self):
    print(" 0 1 2 3 4 5 6 ")
    for row in self.board:
      s = " "
      for i in row:
        if i == 0: s += "  "
        if i == 1: s += "# "
        if i == -1: s += "@ "
      print(s)
    print(" - - - - - - - ")
  def getAllMoves(self):
    moves = []
    for i in range(7):
      moves.append(self.getMove(i))
    return moves
  def getAllMoveIds(self):
    moves = []
    for i in range(7):
      if self.board[0][i] == 0 : moves.append(i)
    return moves
  def checkForWin(self, x):
    if self.moveCount < 6 : return False
    # get y coordinate
    for y in range(6):
      if self.board[y][x] == 1:
        break
    # Build a list of horizontal, vertical and 2 diagonal lines
    linesToTry = [
      [ (x, y+i) for i in range(4) if y+i <= 5 ],
      [ (i,y) for i in range(x-3, x+4) if i >=0 and i <=6 ],
      [ (x+i, y+i) for i in range(-3,4) if x+i >=0 and x+i <=6 and y+i >= 0 and y+i <= 5 ],
      [ (x+i, y-i) for i in range(-3,4) if x+i >=0 and x+i <=6 and y-i >= 0 and y-i <= 5 ]
    ]
    print(linesToTry[0])
    for lineToTry in linesToTry:
      count = 0
      for coord in lineToTry:
        if self.board[coord[1]][coord[0]] == 1:
          count += 1
          if (count == 4):
            return True
        else:
          count = 0
    return False
  def copy(self):
    doppleganger = Game(self.board)
    doppleganger.turn = self.turn
    doppleganger.gameOver = self.gameOver
    doppleganger.winner = self.winner
    doppleganger.moveCount = self.moveCount
    return doppleganger