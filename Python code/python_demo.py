# suppose today i wrote this code
import cv2
image = cv2.imread('image.jpg')

if image is None:
    print('Error: Unable to load image.')
else:
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# i will update this code and add in github