import cv2
import numpy as np
import json

# ========== LOAD HSV RANGES ==========
with open('cube_hsv_ranges.json', 'r') as f:
    hsv_ranges = json.load(f)

# Convert to NumPy arrays
for color in hsv_ranges:
    hsv_ranges[color] = [np.array(hsv_ranges[color][0], dtype=np.uint8),
                         np.array(hsv_ranges[color][1], dtype=np.uint8)]

# ========== FIND EXACTLY 9 CONTOURS ==========
def find_9_squares(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    squares = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.05 * cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        if len(approx) == 4 and area > 1000:
            squares.append(cv2.boundingRect(approx))

    # Sort by area and pick 9 most centered ones
    squares = sorted(squares, key=lambda b: b[2]*b[3], reverse=True)
    squares = sorted(squares[:15], key=lambda b: (b[1], b[0]))[:9]  # sort by top-left corner
    return squares

# ========== COLOR DETECTION ==========
def detect_color(hsv_patch):
    avg = np.mean(hsv_patch.reshape(-1, 3), axis=0).astype(np.uint8)
    for color, (lower, upper) in hsv_ranges.items():
        if np.all(avg >= lower) and np.all(avg <= upper):
            return color
    return "?"

# ========== MAIN ==========
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    squares = find_9_squares(frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for (x, y, w, h) in squares:
        patch = hsv[y:y+h, x:x+w]
        color = detect_color(patch)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Rubik's Cube Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
