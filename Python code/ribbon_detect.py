#INCOMPLETE 12:46 AM
# bounds chnge karvana che line 12,13
# only detecting attributes of id card
import cv2
import numpy as np

ref_img = cv2.imread(r"/home/darshit/Darshit/Studies/python/completePy/opencv/1712792170455.png")
hsv_ref = cv2.cvtColor(ref_img, cv2.COLOR_BGR2HSV)

hist_ref = cv2.calcHist([hsv_ref], [0], None, [256], [0, 256])
cv2.normalize(hist_ref, hist_ref, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

lower_green = np.array([40, 40, 40]) # Bounds change karvana che
upper_green = np.array([70, 255, 255]) # Boundschange karvanu che

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hist_frame = cv2.calcHist([hsv_frame], [0], None, [256], [0, 256])
    cv2.normalize(hist_frame, hist_frame, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    match = cv2.compareHist(hist_ref, hist_frame, cv2.HISTCMP_BHATTACHARYYA)

    threshold = 0.7
    if match < threshold:
        print("Ribbon detected!")

        contours, _ = cv2.findContours(cv2.inRange(hsv_frame, lower_green, upper_green), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Ribbon Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
