# 1:31 push
import cv2
import numpy as np
import time
import mysql.connector
import face_recognition

def save_to_database(timestamp, person_name, image_path, outfit_color):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="opencv"
        )
        cursor = connection.cursor()

        # Inserting data into the opencv_table without specifying the id
        sql = "INSERT INTO opencv_table (time_column, person_name, image, outfit_colour) VALUES (%s, %s, %s, %s)"
        val = (timestamp, person_name, image_path, outfit_color)
        cursor.execute(sql, val)

        connection.commit()
        print("Data successfully inserted into the database")

    except mysql.connector.Error as error:
        print("Failed to insert data into MySQL table:", error)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def click(main_vid, counter, darshit_encoding):
    start_time = time.time()

    while True:
        bool, video_frame = main_vid.read()
        if bool:
            cv2.imshow("output", cv2.resize(video_frame, (650, 650)))
            if time.time() - start_time >= 3:
                filename = f"D:/opencv project/detected/detected_{counter}.jpg"
                cv2.imwrite(filename, video_frame)
                print(f"Image {counter} saved")

                x_upper, y_upper, w_upper, h_upper = 0, 0, video_frame.shape[1], int(video_frame.shape[0] * 0.5)
                roi_upper = video_frame[y_upper:y_upper+h_upper, x_upper:x_upper+w_upper]

                b, g, r = np.mean(roi_upper, axis=(0, 1)).astype(int)
                outfit_color = f"({r}, {g}, {b})"
                print(f"Outfit RGB values: {outfit_color}")
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                # Perform face recognition
                face_encoding = face_recognition.face_encodings(video_frame)
                if len(face_encoding) > 0:
                    match = face_recognition.compare_faces([darshit_encoding], face_encoding[0])
                    if match[0]:
                        person_name = "Darshit"
                    else:
                        person_name = "Anonymous"
                else:
                    person_name = "Anonymous"

                save_to_database(timestamp, person_name, filename, outfit_color)

                counter += 1  # Incrementing the counter

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    return counter



def detect(user_video):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    ref_img = cv2.imread(r"D:\opencv project\openCV\mainribbon.png")
    darshit_image = face_recognition.load_image_file(r'C:\Users\darsh\Downloads\myimg.jpg')
    darshit_encoding = face_recognition.face_encodings(darshit_image)[0]
    x, y, w, h = 302, 1, 660 - 302, 940 - 1
    t = (x, y, w, h)
    roi = ref_img[y:y + h, x:x + w]

    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([105, 106, 192])
    upper_bound = np.array([255, 240, 231])

    mask_roi = cv2.inRange(hsv_roi, lower_bound, upper_bound)

    hist = cv2.calcHist([hsv_roi], [0], mask_roi, [180], [0, 180])
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    terminate = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5, 1)
    main_video = cv2.VideoCapture(user_video)
    prev_center = None
    confidence = 0
    counter = 1
    start_time = time.time()

    while main_video.isOpened():
        bool, video_frames = main_video.read()
        if bool:
            gray_frame = cv2.cvtColor(video_frames, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face_encoding = face_recognition.face_encodings(video_frames, [(y, x+w, y+h, x)])[0]
                match = face_recognition.compare_faces([darshit_encoding], face_encoding)

                if match[0]:
                    name = "Darshit"
                else:
                    name = "Anonymous"

                cv2.rectangle(video_frames, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(video_frames, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            hsv_video_frames = cv2.cvtColor(video_frames, cv2.COLOR_BGR2HSV)
            lb_video_frames = np.array([60, 119, 187])
            ub_video_frames = np.array([255, 255, 250])
            mask_video = cv2.inRange(hsv_video_frames, lb_video_frames, ub_video_frames)
            video_frame_hist = cv2.calcHist([hsv_video_frames], [0], mask_video, [180], [0, 180])

            bitwise_video_frames = cv2.bitwise_and(video_frames, video_frames, mask=mask_video)
            searching = cv2.calcBackProject([hsv_video_frames], [0], video_frame_hist, [0, 180], 1)
            bool_shift, frames_shift = cv2.CamShift(searching, t, terminate)
            rect_points = cv2.boxPoints(bool_shift) if cv2.__version__.startswith('4') else cv2.cv.BoxPoints(bool_shift)
            rect_points = np.int0(rect_points)
            x, y, w, h = cv2.boundingRect(rect_points)

            center_x = x + w // 2
            center_y = y + h // 2

            if cv2.pointPolygonTest(rect_points, (center_x, center_y), False) >= 0:
                confidence = w * h
            else:
                confidence = 0

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
                if confidence < 60:
                    state = "Less possibility"
                    state_color = (0, 0, 255)

                output = cv2.rectangle(video_frames, (x, y), (x + w, y + h), state_color, 2)
                text = f'Possibility: {int((confidence / (w * h)) * 100)}%'
                text_position = (x, y - 20)  # Adjusted position to be above the rectangle
                cv2.putText(output, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(output, state, (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, state_color, 2)  # Placing text above rectangle

                output = cv2.resize(output, (650, 650))
                cv2.imshow("output", output)
                prev_center = (center_x, center_y)
                print("detecting")
                start_time = time.time()
            else:
                masked_video_frames = cv2.resize(video_frames, (650, 650))
                cv2.imshow("output", masked_video_frames)
                print("not detecting")
                if time.time() - start_time >= 3:
                    click(main_video, counter,darshit_encoding)
                    counter += 1
                    start_time = time.time()

            if cv2.waitKey(25) & 0xff == ord("q"):
                break
        else:
            break

    main_video.release()
    cv2.destroyAllWindows()

    ref_img = cv2.imread(r"D:\opencv project\openCV\mainribbon.png")
    x, y, w, h = 302, 1, 660 - 302, 940 - 1
    t = (x, y, w, h)
    roi = ref_img[y:y + h, x:x + w]

    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([105, 106, 192])
    upper_bound = np.array([255, 240, 231])

    mask_roi = cv2.inRange(hsv_roi, lower_bound, upper_bound)

    hist = cv2.calcHist([hsv_roi], [0], mask_roi, [180], [0, 180])
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    terminate = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5, 1)
    main_video = cv2.VideoCapture(user_video)
    prev_center = None
    confidence = 0
    counter = 1
    start_time = time.time()

    while main_video.isOpened():
        bool, video_frames = main_video.read()
        if bool:
            hsv_video_frames = cv2.cvtColor(video_frames, cv2.COLOR_BGR2HSV)
            lb_video_frames = np.array([60, 119, 187])
            ub_video_frames = np.array([255, 255, 250])
            mask_video = cv2.inRange(hsv_video_frames, lb_video_frames, ub_video_frames)
            video_frame_hist = cv2.calcHist([hsv_video_frames], [0], mask_video, [180], [0, 180])

            bitwise_video_frames = cv2.bitwise_and(video_frames, video_frames, mask=mask_video)
            searching = cv2.calcBackProject([hsv_video_frames], [0], video_frame_hist, [0, 180], 1)
            bool_shift, frames_shift = cv2.CamShift(searching, t, terminate)
            rect_points = cv2.boxPoints(bool_shift) if cv2.__version__.startswith('4') else cv2.cv.BoxPoints(bool_shift)
            rect_points = np.int0(rect_points)
            x, y, w, h = cv2.boundingRect(rect_points)

            center_x = x + w // 2
            center_y = y + h // 2

            if cv2.pointPolygonTest(rect_points, (center_x, center_y), False) >= 0:
                confidence = w * h
            else:
                confidence = 0

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
                if confidence < 60:
                    state = "Less possibility"
                    state_color = (0, 0, 255)

                output = cv2.rectangle(video_frames, (x, y), (x + w, y + h), state_color, 2)
                text = f'Possibility: {int((confidence / (w * h)) * 100)}%'
                text_position = (x, y - 20)
                cv2.putText(output, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(output, state, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, state_color, 2)

                output = cv2.resize(output, (650, 650))
                cv2.imshow("output", output)
                prev_center = (center_x, center_y)
                print("detecting")
                start_time = time.time()
            else:
                masked_video_frames = cv2.resize(video_frames, (650, 650))
                cv2.imshow("output", masked_video_frames)
                print("not detecting")
                if time.time() - start_time >= 3:
                    click(main_video, counter)
                    counter += 1
                    start_time = time.time()

            if cv2.waitKey(25) & 0xff == ord("q"):
                break
        else:
            break

    main_video.release()
    cv2.destroyAllWindows()

