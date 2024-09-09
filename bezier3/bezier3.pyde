points = None
lines = None
line_buffer = None
steps = 20
max_curves = 7
fps = 30
paused = False

def setup():
    global points, lines, line_buffer, fps
    lines = []
    line_buffer = []
    size(1400, 700)
    points = [(random(width), random(height)),
            (random(width), random(height)),
            (random(width), random(height))]
    stroke(0)
    fill(0)
    frameRate(fps)

def addLines():
    global points, line_buffer, steps
    last_3_points = points[-3:]
    p1x, p1y = last_3_points[0]
    p2x, p2y = last_3_points[1]
    p3x, p3y = last_3_points[2]

    sd1x = (p2x - p1x) / steps
    sd1y = (p2y - p1y) / steps
    sd2x = (p3x - p2x) / steps
    sd2y = (p3y - p2y) / steps
    for i in range(steps + 1):
        line_buffer.append((p1x + (sd1x * i), p1y + (sd1y * i),
                p2x + (sd2x * i), p2y + (sd2y * i)))


def draw():
    global points, lines, max_curves, steps
    background(200)
    if frameCount % 10 == 0:
        points.append((random(width), random(height)))
        if len(points) > 2 + max_curves :
            points.pop(0)
        if len(points) > 2:
            addLines()
    # for point in points:
    #     x, y = point
    #     stroke(0)
    #     fill(0)
    #     circle(x, y, 3)

    if len(line_buffer) > 0:
        lines.append(line_buffer.pop(0))
        if len(lines) > steps * max_curves:
            lines.pop(0)
    for (p1x, p1y, p2x, p2y) in lines:
        line(p1x, p1y, p2x, p2y)

def mousePressed():
    global points
    points.append((mouseX, mouseY))
    if len(points) > 2:
        addLines()

def keyPressed():
    global paused
    # Toggle pause/resume when spacebar is pressed
    if key == ' ':
        if paused:
            loop()  # Resume the draw loop
        else:
            noLoop()  # Pause the draw loop
        paused = not paused  # Toggle the paused state
