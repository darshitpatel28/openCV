import cv2
import numpy as np


def detect(user_video):

    ref_img = cv2.imread(r"D:\opencv project\openCV\mainribbon.png") #WARNING sample image maro path bijo haase tamaro change karjo mainribbon.png no
    x, y, w, h = 302, 1, 660 - 302, 940 - 1
    t = (x, y, w, h)

    #starting of tracking ROI
    roi = ref_img[y:y + h, x:x + w]

    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # perfect bounds che... lower (105,106,192) , upper(255,240,231)
    lower_bound = np.array([105, 106, 192])
    upper_bound = np.array([255, 240, 231])

    mask_roi = cv2.inRange(hsv_roi, lower_bound, upper_bound)

    hist = cv2.calcHist([hsv_roi], [0], mask_roi, [180], [0, 180])
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    terminate = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5, 1) 
    main_video = cv2.VideoCapture(user_video)                                         # <----------------- user video
    prev_center = None
    confidence = 0

    # video start recording
    while main_video.isOpened():
        bool, video_frames = main_video.read()
        if bool == True:
            #masking and background noise remove video_frames 
            hsv_video_frames = cv2.cvtColor(video_frames, cv2.COLOR_BGR2HSV)
            lb_video_frames = np.array([60, 119, 187])
            ub_video_frames = np.array([255, 255, 250])
            mask_video = cv2.inRange(hsv_video_frames, lb_video_frames, ub_video_frames)
            video_frame_hist = cv2.calcHist([hsv_video_frames], [0], mask_video, [180], [0, 180])

            # bitwise and optional
            bitwise_video_frames = cv2.bitwise_and(video_frames, video_frames, mask=mask_video)
            
            #matching as per hsv and histogram
            searching = cv2.calcBackProject([hsv_video_frames], [0], video_frame_hist, [0, 180], 1)
            bool_shift, frames_shift = cv2.CamShift(searching, t, terminate)

            # reduce vibation rect and made stable
            rect_points = cv2.boxPoints(bool_shift) if cv2.__version__.startswith('4') else cv2.cv.BoxPoints(bool_shift)
            rect_points = np.int0(rect_points)
            x, y, w, h = cv2.boundingRect(rect_points)

            center_x = x + w // 2
            center_y = y + h // 2

            if cv2.pointPolygonTest(rect_points, (center_x, center_y), False) >= 0:
                confidence = w * h
            else:
                confidence = 0

            #decide the possiblity of ribbon or not between 1 to 100 in live screen
            if confidence > 1000:
                if prev_center is not None:
                    distance = np.sqrt((center_x - prev_center[0]) ** 2 + (center_y - prev_center[1]) ** 2)
                    scale_factor = max(0.9, 1 - 0.1 * (distance / 50)) 
                    w = int(w * scale_factor)
                    h = int(h * scale_factor)
                    x = max(0, center_x - w // 2)
                    y = max(0, center_y - h // 2)

                state = "Id card detected"
                state_color = (0, 0, 255)

                #possiblity less than 60 detect person and chnage color or text 
                if confidence < 60:
                    state = "Less possibility"
                    state_color = (0, 0, 255)

                output = cv2.rectangle(video_frames, (x, y), (x + w, y + h), state_color, 2)
                text = f'Possibility: {int((confidence / (w * h)) * 100)}%'
                cv2.putText(output, text, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(output, state, (x, y + h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, state_color, 2)
                output = cv2.resize(output, (650, 650))
                cv2.imshow("output", output)
                prev_center = (center_x, center_y)
                print("detecting")
                
                # if not detecting rectangle dont come in else part
            else:
                masked_video_frames = cv2.resize(video_frames, (650, 650))
                cv2.imshow("output", masked_video_frames)
                print("not detecting")

            if cv2.waitKey(25) & 0xff == ord("q"):
                break
        else:
            break
    return output
    cv2.destroyAllWindows()
