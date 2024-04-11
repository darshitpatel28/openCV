import cv2

def borders_track(img_path):

    img = cv2.imread(img_path)
    img = cv2.resize(img , (451,451))
    new_img = img.copy()
    gray_img = cv2.cvtColor(img , cv2.COLOR_BGRA2GRAY)
    _ , thresh = cv2.threshold(gray_img , 40 , 255 , cv2.THRESH_BINARY)
    contours , hax = cv2.findContours(thresh,cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
    final_img = cv2.drawContours(new_img,contours , -1 , (255,0,0) , 2 )
    
    return final_img