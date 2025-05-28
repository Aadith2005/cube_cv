import cv2
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Couldn't access camera")
else:
    print("Camera working! Press 'q' to exit")
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera Test', frame)
        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()