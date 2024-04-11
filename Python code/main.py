# main.py
import cv2
import borders_track
image_path = "/home/darshit/Darshit/Project/haar cascades/p/1712791875943.png"
img = borders_track.borders_track(img_path=image_path) #bordertrack function in brodertrack py file
cv2.imshow("contours",img)
cv2.waitKey(0)
cv2.destroyAllWindows()