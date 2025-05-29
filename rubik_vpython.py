from vpython import *

scene.title = "3D Rubik's Cube"
scene.background = color.black
scene.width = 800
scene.height = 600
scene.center = vector(1, 1, 1)
scene.autoscale = False

# Colors per face
face_colors = {
    'U': color.white,    # Up
    'D': color.yellow,   # Down
    'F': color.green,    # Front
    'B': color.blue,     # Back
    'L': color.orange,   # Left
    'R': color.red       # Right
}

# Create 3x3x3 cubelets
for x in range(3):
    for y in range(3):
        for z in range(3):
            cubelet = box(
                pos=vector(x, y, z),
                size=vector(0.95, 0.95, 0.95),
                color=color.gray(0.2)
            )
