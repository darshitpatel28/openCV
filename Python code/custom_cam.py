import cv2

link = "http://100.73.67.154:8080/video"
cap = cv2.VideoCapture(link)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame , (600,400))
    if not ret:
        print("Error: Unable to read frame.")
        break

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
