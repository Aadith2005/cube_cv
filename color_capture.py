import cv2
import numpy as np
import json

color_names = ['white', 'yellow', 'red', 'orange', 'blue', 'green']
hsv_ranges = {}

cap = cv2.VideoCapture(0)

print("Calibration Tool for Rubik's Cube Colors")
print("Hold each color in front of the camera center. Press SPACE to sample.")

for color in color_names:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        h, w, _ = frame.shape
        center = frame[h//2-10:h//2+10, w//2-10:w//2+10]
        hsv_patch = cv2.cvtColor(center, cv2.COLOR_BGR2HSV)
        avg_color = np.mean(hsv_patch.reshape(-1, 3), axis=0)

        cv2.rectangle(frame, (w//2-10, h//2-10), (w//2+10, h//2+10), (255, 255, 255), 2)
        cv2.putText(frame, f"Show {color.upper()} - Press SPACE to capture", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Calibration", frame)

        key = cv2.waitKey(1)
        if key == 32:  # SPACE
            lower = np.clip(avg_color - [10, 40, 40], 0, 255)
            upper = np.clip(avg_color + [10, 40, 40], 0, 255)
            hsv_ranges[color] = [lower.tolist(), upper.tolist()]
            print(f"Captured {color} HSV range: {hsv_ranges[color]}")
            break
        elif key == ord('q'):
            exit()

cap.release()
cv2.destroyAllWindows()

with open("cube_hsv_ranges.json", "w") as f:
    json.dump(hsv_ranges, f, indent=4)
print("HSV calibration saved to cube_hsv_ranges.json")
