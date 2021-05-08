EMPTY = '0x0C0C3C'
RED = '0xC83C3C'
YELLOW = '0xE6E646'
PUCKSIZE = 70
'''
During the game, I use 1 for red and -1 for yellow
'''

class Board:

    def __init__(self):
        self.spots = [[None for _ in range(7)] for __ in range(6)]

    def display(self, x, y, w, h):
        noStroke()
        fill(25, 25, 125)
        rect(x, y, w, h)
        cellW = w / len(self.spots[0])
        cellH = h / len(self.spots)
        for row in range(len(self.spots)):
            for col in range(len(self.spots[row])):
                spot = self.spots[row][col]
                if spot == None:
                    fill(EMPTY)
                elif spot == 1:
                    fill(RED)
                else:
                    fill(YELLOW)
                circle( cellW * col + (cellW / 2) + x,
                        cellH * row + (cellH / 2) + y,
                        PUCKSIZE)

class Game:

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.board = Board()
        self.playerSpace = 100
        self.turn = 1

    def display(self):
        self.board.display(0, self.playerSpace, self.width, \
                self.height - self.playerSpace)
        if self.turn > 0:
            fill(RED)
        else:
            fill(YELLOW)
        circle(mouseX, 0,PUCKSIZE)

    def play(self):
        pos = mouseX
        # place puck
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

def keyPressed():
    if key == 'q':
        exit()
