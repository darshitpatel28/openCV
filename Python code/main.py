import cv2
import ribbon_detect as detect

user_video = "http//100.115.87.19:8080/video"
detect.id_card_detect(user_video)

cv2.destroyAllWindows()