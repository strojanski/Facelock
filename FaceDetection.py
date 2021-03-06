import cv2              #pip install opencv-python
import numpy as np
import os, sys
import time
import cherrypy
import webbrowser

# cascades taken from: https://github.com/Itseez/opencv/tree/master/data/haarcascades


url = "http://127.0.0.1:8080/"

def logout():
    if (os.name == "posix"):
        os.system("gnome-screensaver-command -l")
        os.system("xscreensaver-command -lock")
        os.system("exit")
    os.system("rundll32.exe user32.dll,LockWorkStation")
    
    print(os.name)
    print(os.getlogin())
# camera feed is in at cca 8 fps

class FaceDetect(object):

    webbrowser.open("http://127.0.0.1:8080")
    @cherrypy.expose
    def index(self, cas=0):
        if(cas):
            try:
                frontface_default = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
                frontface_alt = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')
                frontface_profile = cv2.CascadeClassifier('cascades/haarcascade_profileface.xml')
                eyes_def = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
                eyes_glasses = cv2.CascadeClassifier('cascades/haarcascade_eye_tree_eyeglasses.xml')
                print(frontface_default)

                camera = cv2.VideoCapture(0)
                # we read frames until escape key is pressed
                time1 = time.time()
                while True:
                    ret, img = camera.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # returns an array of rectangles around found objects in a given image
                    faces_def = frontface_default.detectMultiScale(gray, 1.2, 5)
                    faces_alt = frontface_alt.detectMultiScale(gray, 1.2, 5)
                    faces_profile = frontface_profile.detectMultiScale(gray, 1.2, 5)
                    if (len(faces_alt) != 0):
                        for (x, y, w, h) in faces_alt:
                            # draw a rectangle around detected faces
                            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2) 
                            roi_gray = gray[y:y+h, x:x+w]
                            roi_color = img[y:y+h, x:x+w]
                            eyes_detect = eyes_def.detectMultiScale(roi_gray)
                            glasses_detect = eyes_glasses.detectMultiScale(roi_gray)
                            for (ex, ey, ew, eh) in eyes_detect:
                                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                            for (ex, ey, ew, eh) in glasses_detect:
                                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)
                    elif (len(faces_def) != 0):
                        for (x, y, w, h) in faces_def:
                            # draw a rectangle around detected faces
                            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2) 
                            roi_gray = gray[y:y+h, x:x+w]
                            roi_color = img[y:y+h, x:x+w]
                            eyes_detect = eyes_def.detectMultiScale(roi_gray)
                            glasses_detect = eyes_glasses.detectMultiScale(roi_gray)
                            for (ex, ey, ew, eh) in eyes_detect:
                                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                            for (ex, ey, ew, eh) in glasses_detect:
                                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)
                    else: 
                        for (x, y, w, h) in faces_profile:
                                # draw a rectangle around detected faces
                            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2) 
                            roi_gray = gray[y:y+h, x:x+w]
                            roi_color = img[y:y+h, x:x+w]
                            eyes_detect = eyes_def.detectMultiScale(roi_gray)
                            glasses_detect = eyes_glasses.detectMultiScale(roi_gray)
                            for (ex, ey, ew, eh) in eyes_detect:
                                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                            for (ex, ey, ew, eh) in glasses_detect:
                                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)
                        
                    cv2.imshow('canvas', img)
                    if len(faces_alt) != 0 or len(faces_def) != 0 or len(faces_profile) != 0:
                        time1 = time.time()
                    k = cv2.waitKey(30) & 0xff
                    if (k == 27):
                        break
                    if len(faces_alt) == 0 and len(faces_def) == 0 and len(faces_profile) == 0:
                        time2 = time.time()
                        total_time = time2 - time1
                        if (int(cas) != 0):
                            if (total_time >= int(cas)):
                                logout()
                                sys.exit("No face detected. Exiting ...")
                        elif (total_time > 5):
                            print("Time: " + str(total_time))
                            logout()
                            sys.exit("No face detected. Exiting ...")
                camera.release()
                cv2.destroyAllWindows()
            except BaseException as e:
                print(e)
                return open('set.html', encoding="utf8")
            return open('set.html', encoding="utf8")
            
            
        return open('index.html', encoding="utf8")
   


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/style': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './style'
        },
        '/ico': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './ico'
        }
    }
    cherrypy.quickstart(FaceDetect(), '/', conf)
