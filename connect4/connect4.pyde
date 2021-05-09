EMPTY = '0x0C0C3C'
RED = '0xC83C3C'
YELLOW = '0xE6E646'
PUCKSIZE = 70
PLAYERRED = 1
PLAYERYELLOW = -1

class Board:

    def __init__(self, x, y, w, h):
        self.rows = 6
        self.cols = 7
        self.spots = [[None for _ in range(self.cols)] for __ in range(self.rows)]
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.plays = []

    def display(self):
        noStroke()
        fill(25, 25, 125)
        rect(self.x, self.y, self.w, self.h)
        cellW = self.__getCellWidth()
        cellH = self.__getCellHeight()
        for row in range(len(self.spots)):
            for col in range(len(self.spots[row])):
                spot = self.spots[row][col]
                if spot == None:
                    fill(EMPTY)
                elif spot == 1:
                    fill(RED)
                else:
                    fill(YELLOW)
                circle( cellW * col + (cellW / 2) + self.x,
                        cellH * row + (cellH / 2) + self.y,
                        PUCKSIZE)

    def isValidPlay(self, pos):
        cellW = self.__getCellWidth()
        for col in range(len(self.spots[0])):
            if col * cellW < pos < (col + 1) * cellW:
                if self.spots[0][col] is None:
                    return True
        return False

    def placePuck(self, pos, player):
        cellW = self.__getCellWidth()
        r = None
        c = None
        found = False
        for col in range(len(self.spots[0])):
            if col * cellW < pos < (col + 1) * cellW:
                for row in range(len(self.spots))[::-1]:
                    if self.spots[row][col] is None:
                        self.spots[row][col] = player
                        self.plays.append((row, col))
                        return (row, col)

    def __getCellWidth(self):
        return self.w / len(self.spots[0])

    def __getCellHeight(self):
        return self.h / len(self.spots)

    def checkWin(self, placement):
        pr = placement[0]
        pc = placement[1]
        player = self.spots[pr][pc]
        directions = [(-1, 0), (-1, -1), (0, -1), (1, -1)]
        wins = []
        for row in range(len(self.spots)):
            for col in range(len(self.spots[row])):
                if self.spots[row][col] != player:
                    continue
                for d in directions:
                    currR = row
                    currC = col
                    consecutive = 0
                    while True:
                        if (not 0 <= currR < self.rows) or (not 0 <= currC < self.cols):
                            break
                        if self.spots[currR][currC] != player:
                            break
                        consecutive += 1
                        currR += d[0]
                        currC += d[1]
                    if consecutive > 3:
                        currR -= d[0]
                        currC -= d[1]
                        wins.append((row, col, currR, currC, consecutive))
        return wins

    def drawVictoryLines(self, coordinateList):
        stroke(50, 210, 70)
        strokeWeight(10)
        cellW = self.__getCellWidth()
        cellH = self.__getCellHeight()
        for coordinates in coordinateList:
            line( self.x + coordinates[1] * cellW + cellW / 2,
                  self.y + coordinates[0] * cellH + cellH / 2,
                  self.x + coordinates[3] * cellW + cellW / 2,
                  self.y + coordinates[2] * cellH + cellH / 2)

class Game:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.playerSpace = 100
        self.board = Board(0, self.playerSpace, self.w, \
                self.h - self.playerSpace)
        self.turn = 1
        self.over = False

    def display(self):
        self.board.display()
        if self.over:
            self.board.drawVictoryLines(self.victoryLines)

            textAlign(CENTER, CENTER)
            textSize(30)
            # Victory message
            stroke(0)
            strokeWeight(10)
            fill(255)
            rect(width / 2 - 100, 100, 200, 50)
            message1 = "Red wins!" if self.turn == 1 else "Yellow Wins!"
            fill(0)
            text(message1, width / 2 - 100, 100, 200, 50)
            # Restart message
            message2 = "Press R to restart"
            fill(170, 30, 30)
            text(message2, 0, 0, self.w, self.playerSpace)
        else:
            self.__drawPuck()

    def __drawPuck(self):
        # Choose the right color
        if self.turn > 0:
            fill(RED)
        else:
            fill(YELLOW)

        # calculate where the puck shoule be drawn
        if mouseX > self.w - PUCKSIZE / 2:
            self.puckX = self.w - PUCKSIZE / 2
        elif mouseX < PUCKSIZE / 2:
            self.puckX = PUCKSIZE / 2
        else:
            self.puckX = mouseX
        circle(self.puckX, 0,PUCKSIZE)

    def undoPlay(self):
        if len(self.board.plays) > 0:
            previous = self.board.plays.pop()
            self.board.spots[previous[0]][previous[1]] = None
            self.turn *= -1
            if self.over:
                self.turn *= -1
                self.over = False

    def play(self):
        # Make sure move is valid
        if self.board.isValidPlay(self.puckX) and not self.over:
            # place puck
            placement = self.board.placePuck(self.puckX, self.turn)
            #check for win
            result = self.board.checkWin(placement)
            if len(result) > 0:
                self.over = True
                # set victory line coordinates
                self.victoryLines = result
            else:
                # update turn
                self.turn *= -1

'''
Global Variables
'''
game = None

def setup():
    global game
    size(700, 700)

    game = Game(width, height)

def draw():
    global game
    background(200)
    game.display()

def mousePressed():
    global game
    game.play()

def keyPressed():
    global game
    if key == 'q':
        exit()
    if key == 'u':
        game.undoPlay()
    if game.over:
        if key in('R', 'r'):
            game = Game(width, height)
