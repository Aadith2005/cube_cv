def process_frame(self, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    contours = self._find_squares(frame)

    if len(contours) != 9:
        return frame, []  # Only proceed if a full face is visible

    face_colors = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        square_patch = hsv[y:y+h, x:x+w]
        center_patch = square_patch[h//4:3*h//4, w//4:3*w//4]
        avg_color = np.mean(center_patch, axis=(0, 1))
        color = self.detector.detect(avg_color)
        if color:
            face_colors.append(((x, y), color))
            cv2.putText(frame, color, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

    return frame, face_colors
