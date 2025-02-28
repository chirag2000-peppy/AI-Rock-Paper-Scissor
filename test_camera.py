import cv2

cap = cv2.VideoCapture(0)  # Open webcam (0 for default camera)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Webcam Test", frame)  # Show video feed

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()