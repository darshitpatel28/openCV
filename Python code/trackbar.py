import cv2
import numpy as np

def image(x):
    pass

img=np.zeros((500,500,3),np.uint8)*255

cv2.namedWindow("colour")

cv2.createTrackbar("R","colour",0,255,image)
cv2.createTrackbar("G","colour",0,255,image)
cv2.createTrackbar("B","colour",0,255,image)

while True:
    cv2.imshow("colour",img)
    if cv2.waitKey(1) & 0xff ==ord("p"):
        break
    r=cv2.getTrackbarPos("R","colour")
    g = cv2.getTrackbarPos("G", "colour")
    b = cv2.getTrackbarPos("B", "colour")

    img[:]=[b,g,r]

cv2.destroyAllWindows()