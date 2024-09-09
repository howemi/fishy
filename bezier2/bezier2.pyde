triangles = None
lines = None
line_buffer = None
steps = 50

def setup():
    global triangles, lines, line_buffer
    triangles = [[]]
    lines = []
    line_buffer = []
    size(700, 700)

def addLines():
    triangle = triangles[-1]
    if len(triangle) == 3:
        p1x = triangle[0]["x"]
        p1y = triangle[0]["y"]

        p2x = triangle[1]["x"]
        p2y = triangle[1]["y"]

        p3x = triangle[2]["x"]
        p3y = triangle[2]["y"]

        # line(triangle[0]["x"], triangle[0]["y"],
        #         triangle[1]["x"], triangle[1]["y"])
        # line(triangle[1]["x"], triangle[1]["y"],
        #         triangle[2]["x"], triangle[2]["y"])
        # sd = step-distance
        sd1x = (p2x - p1x) / steps
        sd1y = (p2y - p1y) / steps
        sd2x = (p3x - p2x) / steps
        sd2y = (p3y - p2y) / steps
        for i in range(steps + 1):
            line_buffer.append((p1x + (sd1x * i), p1y + (sd1y * i),
                    p2x + (sd2x * i), p2y + (sd2y * i)))


def draw():
    global triangles, steps
    background(200)
    stroke(0)
    fill(0)
    circle(mouseX, mouseY, 3)
    for triangle in triangles:
        for point in triangle:
            stroke(0)
            fill(0)
            circle(point["x"], point["y"], 3)
    # if frameCount % 1 == 0 and len(line_buffer) > 0:
    if len(line_buffer) > 0:
        lines.append(line_buffer.pop(0))
    for (p1x, p1y, p2x, p2y) in lines:
        line(p1x, p1y, p2x, p2y)

def mousePressed():
    global triangles
    triangles[-1].append({"x": mouseX, "y": mouseY})
    addLines()
    if len(triangles[-1]) == 3:
        triangles.append([])
