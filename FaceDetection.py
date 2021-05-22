import cv2
import numpy as np
import os
# cascades taken from: https://github.com/Itseez/opencv/tree/master/data/haarcascades

def logout():
    global k
    if (os.name == "posix"):
        os.system("gnome-screensaver-command -l")
        os.system("exit")
        k = 27
    os.system("shutdown -l")
    
    print(os.name)
    print(os.getlogin())


frontface_default = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
frontface_alt = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
frontface_profile = cv2.CascadeClassifier('haarcascade_profileface.xml')

eyes_def = cv2.CascadeClassifier('haarcascade_eye.xml')
eyes_glasses = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses')
print(frontface_default)

camera = cv2.VideoCapture(0)
time_without_faces = 0
# we read frames until escape key is pressed
while True:
    ret, img = camera.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # returns an array of rectangles around found objects in a given image
    faces_def = frontface_default.detectMultiScale(gray, 1.2, 5)
    faces_alt = frontface_alt.detectMultiScale(gray, 1.3, 5)
    faces_profile = frontface_default.detectMultiScale(gray, 1.3, 5)
    if (len(faces_alt) != 0):
        for (x, y, w, h) in faces_alt:
            # draw a rectangle around detected faces
            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2) 
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes_detect = eyes_def.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes_detect:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
    elif (len(faces_def) != 0):
        for (x, y, w, h) in faces_def:
            # draw a rectangle around detected faces
            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2) 
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes_detect = eyes_def.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes_detect:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
    else: 
        for (x, y, w, h) in faces_profile:
                # draw a rectangle around detected faces
            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2) 
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes_detect = eyes_def.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes_detect:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
    cv2.imshow('img', img)
    global k
    k = cv2.waitKey(30) & 0xff
    if (k == 27):
        break
    if len(faces_alt) == 0 and len(faces_def) == 0 and len(faces_profile) == 0:
        time_without_faces += 1
    else:
        time_without_faces = 0
    if (time_without_faces >= 30):
        logout()




camera.release()
cv2.destroyAllWindows()

