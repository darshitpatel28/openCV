import cv2
import face_recognition

def detect_faces_from_video(video_capture, known_encodings=[], known_names=[]):
    face_cascade = cv2.CascadeClassifier('Haarcascade_frontalface_default.xml')

    while True:
        ret, frame = video_capture.read()
        frame = cv2.resize(frame, (600 , 370))
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces using cascade classifier
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Extract face ROI
            face_roi = frame[y:y+h, x:x+w]

            # Convert BGR image to RGB
            face_roi_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)

            face_encoding = face_recognition.face_encodings(face_roi_rgb)

            name = "Anonymous"

            for known_encoding, known_name in zip(known_encodings, known_names):
                if len(face_encoding) > 0:
                    match = face_recognition.compare_faces([known_encoding], face_encoding[0])
                    if match[0]:
                        name = known_name
                        break  # Break loop if a match is found

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Annotate the frame with name
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
