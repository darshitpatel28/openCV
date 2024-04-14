import cv2
import time

def click():
    main_vid = cv2.VideoCapture(0)
    counter = 1  # Initialize a counter for dynamically generating filenames

    while True:
        # Start the timer for every iteration
        start_time = time.time()
        
        while True:
            bool, video_frame = main_vid.read()

            if bool:                
                if time.time() - start_time >= 3:
                    # Generate filename dynamically
                    filename = rf"D:\opencv project\detected\detected_{counter}.jpg"
                    cv2.imwrite(filename, video_frame)
                    print(f"Saved image: {filename}")
                    counter += 1  # Increment the counter for the next image
                    break

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    main_vid.release()
    cv2.destroyAllWindows()

click()
