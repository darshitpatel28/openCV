# current status : id card detection tracking
import cv2
import ribbon_detect as detect # detect vadi file... ( ctrl + mouse left click on ribbon_detect to redirect there )

main_video = 0  # declare dummy var

detect.id_card_detect(main_video) #call kyro che function in ribbon_detect file

cv2.destroyAllWindows()