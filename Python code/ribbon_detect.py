#ctrl + mouse left click karso je variable function to jya variable , function decralre ke use thyo haase....
# tya automatic cursor vay jase

import cv2
import numpy as np

def id_card_detect(user_video):

    ref_img = cv2.imread("/home/darshit/Darshit/Studies/python/completePy/opencv/mainribbon.png")
    x, y, w, h = 302, 1, 660 - 302, 940 - 1
    t = (x, y, w, h)
    roi = ref_img[y:y + h, x:x + w]

    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([80, 100, 100])
    upper_bound = np.array([120, 255, 255])

    mask = cv2.inRange(hsv_roi, lower_bound, upper_bound)

    hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])

    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

    terminate = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    main_video = cv2.VideoCapture(user_video)# <----------- ama user no video input thase

    prev_rect = None

    while main_video.isOpened():
        bool, video_frames = main_video.read()

        if bool == True:
            hsv_video_frames = cv2.cvtColor(video_frames, cv2.COLOR_BGR2HSV)

            searching = cv2.calcBackProject([hsv_video_frames], [0], hist, [0, 180], 1)

            bool_shift, frames_shift = cv2.CamShift(searching, t, terminate)

            x, y, w, h = frames_shift
            (center_x, center_y), (width, height), angle = bool_shift
            confidence = width * height

            if confidence > 1000:  # Adjust this threshold as needed
                if prev_rect is not None:
                    x = int((x + prev_rect[0]) / 2)
                    y = int((y + prev_rect[1]) / 2)
                    w = int((w + prev_rect[2]) / 2)
                    h = int((h + prev_rect[3]) / 2)

                state = "Id card detected"
                state_color = (0, 0, 255)
                if confidence < 60:
                    state = "Less possibility"
                    state_color = (0, 0, 255)

                output = cv2.rectangle(video_frames, (x, y), (x + w, y + h), state_color, 2)

                text = f'Possibility: {int((confidence / (w * h)) * 100)}%'
                cv2.putText(output, text, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)
                cv2.putText(output, state, (x, y + h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, state_color, 2)
                output = cv2.resize(output,(650,650))
                cv2.imshow("output", output)
                prev_rect = (x, y, w, h)
            else:
                video_frames = cv2.resize(video_frames , (650,650))
                cv2.imshow("output", video_frames)

            if cv2.waitKey(25) & 0xff == ord("q"):
                break
        else:
            break

    cv2.destroyAllWindows()
    return output


