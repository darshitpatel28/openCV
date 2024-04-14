import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(image): # a
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return image

cap = cv2.VideoCapture(0)

img_counter = 0

while True:
    ret, frame = cap.read()
    frame_copy = frame.copy()
    frame_without_rect = detect_faces(frame_copy)
    cv2.imshow('Face Detection', frame_without_rect)
    
    key = cv2.waitKey(1)
    
    if key & 0xFF == ord('q'):
        break
    
    if key & 0xFF == ord(' '):
        img_counter += 1
        file_path = f'D:/opencv project/detected/photo_{img_counter}.jpg'
        cv2.imwrite(file_path, frame)
        print(f"Saved: {file_path}")

cap.release()
cv2.destroyAllWindows()
