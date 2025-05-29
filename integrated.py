import cv2
import numpy as np
import json
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# ---------------------- Load HSV Ranges ----------------------
with open("cube_hsv_ranges.json", "r") as f:
    HSV_RANGES = json.load(f)

# ---------------------- Cube State ----------------------
cube_faces = {}
face_order = ["U", "D", "F", "B", "L", "R"]
face_index = 0

# ---------------------- Color Detection ----------------------
def get_color_name(hsv_pixel):
    for color, (lower, upper) in HSV_RANGES.items():
        lower = np.array(lower)
        upper = np.array(upper)
        if np.all(lower <= hsv_pixel) and np.all(hsv_pixel <= upper):
            return color
    return "unknown"

# ---------------------- Grid Detection ----------------------
def detect_cube_face(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, w, _ = frame.shape
    step = 40
    size = 20
    colors = []
    start_x = w // 2 - step
    start_y = h // 2 - step

    for i in range(3):
        for j in range(3):
            x = start_x + j * step
            y = start_y + i * step
            patch = hsv[y-size//2:y+size//2, x-size//2:x+size//2]
            avg_hsv = np.mean(patch.reshape(-1, 3), axis=0)
            color = get_color_name(avg_hsv)
            colors.append(color)
            cv2.rectangle(frame, (x-size//2, y-size//2), (x+size//2, y+size//2), (255,255,255), 1)
            cv2.putText(frame, color, (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)

    return frame, colors

# ---------------------- OpenGL Cube Renderer ----------------------
angle = 0

def draw_cube():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Camera setup
    gluLookAt(4, 4, 6, 0, 0, 0, 0, 1, 0)

    glRotatef(angle, 1, 1, 0)  # Simple animation
    angle += 0.5  # Continuous rotation

    face_positions = {
        "F": (0, 0, 1), "B": (0, 0, -1), "U": (0, 1, 0),
        "D": (0, -1, 0), "L": (-1, 0, 0), "R": (1, 0, 0)
    }

    face_rotations = {
        "F": (0, 0, 0), "B": (180, 0, 1, 0), "U": (-90, 1, 0, 0),
        "D": (90, 1, 0, 0), "L": (90, 0, 1, 0), "R": (-90, 0, 1, 0)
    }

    color_map = {
        "white": (1, 1, 1), "yellow": (1, 1, 0), "red": (1, 0, 0),
        "orange": (1, 0.5, 0), "blue": (0, 0, 1), "green": (0, 1, 0), "unknown": (0.2, 0.2, 0.2)
    }

    for face, colors in cube_faces.items():
        glPushMatrix()
        rot = face_rotations[face]
        glRotatef(rot[0], rot[1], rot[2], rot[3])
        glTranslatef(*face_positions[face])
        for i in range(3):
            for j in range(3):
                idx = i * 3 + j
                glColor3fv(color_map.get(colors[idx], (0.2, 0.2, 0.2)))
                x = j * 0.33 - 0.5
                y = -i * 0.33 + 0.5
                glBegin(GL_QUADS)
                glVertex3f(x, y, 0)
                glVertex3f(x + 0.3, y, 0)
                glVertex3f(x + 0.3, y - 0.3, 0)
                glVertex3f(x, y - 0.3, 0)
                glEnd()
        glPopMatrix()

    glutSwapBuffers()

# ---------------------- GLUT Setup ----------------------
def init_glut():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Rubik's Cube")
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1)

    # Set perspective projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(draw_cube)
    glutIdleFunc(draw_cube)
    glutMainLoop()

# ---------------------- Main ----------------------
def main():
    cap = cv2.VideoCapture(0)
    print("Press SPACE to capture face. Order: U, D, F, B, L, R")

    global face_index
    while face_index < 6:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, colors = detect_cube_face(frame.copy())
        face_name = face_order[face_index]
        cv2.putText(processed_frame, f"Show face: {face_name}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Capture Face", processed_frame)

        key = cv2.waitKey(1)
        if key == 32:  # SPACE key
            if len(colors) == 9:
                cube_faces[face_name] = colors
                face_index += 1
            else:
                print("Could not detect 9 stickers. Try again.")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if len(cube_faces) == 6:
        init_glut()

if __name__ == "__main__":
    main()
