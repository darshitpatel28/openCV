# Meanshift
#calcbackprject


import cv2
import numpy as np

ref_img = cv2.imread("/home/darshit/Darshit/Studies/python/completePy/opencv/1712792170455.png")

x , y , w , h = 283,26 , 761-283 , 811-26
t = (x , y ,w , h)
roi = ref_img[y:y+h , x:x+w]


hsv_roi = cv2.cvtColor(roi , cv2.COLOR_BGR2HSV) 

mask = cv2.inRange(hsv_roi , np.array((0.,60.,32.)) , np.array((180.,255.,255.))) # ama thodu color change avse

hist = cv2.calcHist([hsv_roi],[0],mask,[180] , [0,180])

cv2.normalize(hist , hist , 0 ,255 , cv2.NORM_MINMAX)

terminate = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT , 10 , 1)



main_video = cv2.VideoCapture(0)

while main_video.isOpened():
    bool , video_frames = main_video.read()

    if bool == True:
        hsv_video_frames = cv2.cvtColor(video_frames,cv2.COLOR_BGR2HSV)
        searching = cv2.calcBackProject([hsv_video_frames] , [0] , hist , [0 , 180] , 1)
        bool_shift , frames_shift = cv2.CamShift(searching , t , terminate)
        x , y , w , h = frames_shift
        output = cv2.rectangle(video_frames , (x , y) , (x+w , y+h) , (0,255,0) , 2)
        cv2.imshow("output",output)
        if cv2.waitKey(25) & 0xff == ord("q"):
            break
    else:
        break

cv2.destroyAllWindows()
