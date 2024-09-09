triangles = None
steps = 20

def setup():
    global triangles
    triangles = [[]]
    size(700, 700)

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
                line(p1x + (sd1x * i), p1y + (sd1y * i),
                        p2x + (sd2x * i), p2y + (sd2y * i))

def mousePressed():
    global triangles
    if len(triangles[-1]) == 3:
        triangles.append([])
    triangles[-1].append({"x": mouseX, "y": mouseY})
