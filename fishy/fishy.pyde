"""
Helper function for detecting collisions
"""
def rectRect(r1x, r1y, r1w, r1h, r2x, r2y, r2w, r2h):
  return r1x + r1w >= r2x and r1x <= r2x + r2w and r1y + r1h >= r2y \
          and r1y <= r2y + r2h

SCREEN_SIZE = 700

class Player:
    speed = 10
    score = 0
    size = 25
    xAccel = 0
    yAccel = 0

    def __init__(self):
        self.x = SCREEN_SIZE / 2 - self.size / 2
        self.y = SCREEN_SIZE / 2 - self.size / 2
        self.left = LEFT
        self.right = RIGHT
        self.up = UP
        self.down = DOWN
        self.c = color(85, 190, 160)

    # def __init__(self, x, y, left, up, down, right, c):
    #     self.x = x
    #     self.y = y
    #     self.left = left
    #     self.right = right
    #     self.up = up
    #     self.down = down
    #     self.c = c

    # def move(self, code):
        # if code == self.left:
        #     self.x -= self.speed
        # elif code == self.right:
        #     self.x += self.speed
        # elif code == self.up:
        #     self.y -= self.speed
        # elif code == self.down:
        #     self.y += self.speed
    def move(self, pressing):
        # Update acceleration
        self._updateAcceleration(pressing)
        # Loop on the edges
        if self.x > SCREEN_SIZE:
            self.x = 0
        if self.y > SCREEN_SIZE:
            self.y = 0
        if self.x + self.size < 0:
            self.x = SCREEN_SIZE
        if self.y + self.size < 0:
            self.y = SCREEN_SIZE

    def _updateAcceleration(self, pressing):
        accelRate = .2
        decelRate = .08
        maxAccel = 5
        if self.right in pressing:
            self.xAccel += accelRate if self.xAccel < maxAccel else 0
        if self.left in pressing:
            self.xAccel -= accelRate if self.xAccel > -maxAccel else 0
        if self.down in pressing:
            self.yAccel += accelRate if self.yAccel < maxAccel else 0
        if self.up in pressing:
            self.yAccel -= accelRate if self.yAccel > -maxAccel else 0
        self.x += self.xAccel
        self.y += self.yAccel
        if self.xAccel > 0:
            self.xAccel -= decelRate
        if self.xAccel < 0:
            self.xAccel += decelRate
        if self.yAccel > 0:
            self.yAccel -= decelRate
        if self.yAccel < 0:
            self.yAccel += decelRate
        if -.1 < self.yAccel < .1:
            self.yAccel = 0
        if -.1 < self.xAccel < .1:
            self.xAccel = 0

    def display(self):
        fill(self.c)
        stroke(255)
        rect(self.x, self.y, self.size, self.size)


    def getPoints(self, points):
        self.score += points

class Shape:
    def __init__(self, size):
        self.direction = 'l' if int(random(2)) == 1 else 'r'
        self.size = size
        if self.direction == 'l':
            self.x = SCREEN_SIZE + self.size
        else:
            self.x = -self.size
        self.y = int(random(SCREEN_SIZE))
        # self.shape = rect if int(random(2)) == 1 else ellipse
        # self.shape = ellipse
        self.shape = rect
        self.color = color(random(255), random(255), random(255))
        self.speed = 1 + random(2)

    def display(self):
        fill(self.color)
        stroke(0)
        self.shape(self.x, self.y, self.size, self.size)

    def move(self):
        self.x += -self.speed if self.direction == 'l' else self.speed
        # Opting to remove old shapes instead of looping them
        # if self.direction == 'r' and self.x - self.size > SCREEN_SIZE:
        #     self.x = -self.size
        # if self.direction == 'l' and self.x + self.size < 0:
        #     self.x = SCREEN_SIZE + self.size
    def offScreen(self):
        if self.direction == 'l':
            return self.x + self.size < 0
        else:
            return self.x > SCREEN_SIZE

class Game:
    def __init__(self):
        self.player = Player()
        self.shapes = set()
        self.frames = 0
        self.over = False

    def play(self):
        if self.over:
            noLoop()
        self.frames += 1
        self.player.display()
        self.showScore()
        self.handleShapes()

    def showScore(self):
        fill(0)
        textSize(14)
        score = self.player.score if self.player.score >= 0 else "CHEATER"
        text("Score: {}".format(score), 30, SCREEN_SIZE - 30)

    def handleShapes(self):
        if self.frames % 30 == 0:
            # self.frames = 1
            if len(self.shapes) < 20:
                shapeSize = 5 + int(random(min(self.player.size * 2, 200)))
                self.shapes.add(Shape(shapeSize))
        remove = set()
        for s in self.shapes:
            s.move()
            s.display()
            if rectRect(s.x, s.y, s.size, s.size, self.player.x,\
                    self.player.y, self.player.size, \
                    self.player.size):
                if s.size > self.player.size:
                    self.over = True
                    textAlign(CENTER)
                    textSize(25)
                    fill(0)
                    score = self.player.score if self.player.score >= 0 else "CHEATER"
                    text("Game Over! Final Score {}".format(score),
                            SCREEN_SIZE / 2, SCREEN_SIZE / 2)
                    text("Press R to restart.", SCREEN_SIZE / 2,
                            SCREEN_SIZE / 2 + 50)
                else:
                    self.player.getPoints(s.size ** 2)
                    self.player.size += (s.size / 15)
                    remove.add(s)
            if s.offScreen():
                remove.add(s)
        for r in remove:
            self.shapes.remove(r)


g = None
# Keeps track of what keys are being pressed
pressing = set()
def setup():
    global g
    size(SCREEN_SIZE, SCREEN_SIZE)
    g = Game()

def draw():
    global g
    background(200)
    g.play()
    g.player.move(pressing)

def keyPressed():
    global g, pressing
    pressing.add(keyCode)
    # print(keyCode)
    # '\' is the cheat code key
    if keyCode == 92:
        g.player.size *= 2
        g.player.score -= 10 ** 10
    if g.over and key == 'r':
        g = Game()
        loop()

def keyReleased():
    global pressing
    pressing.remove(keyCode)
