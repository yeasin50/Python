import cv2
import time
import numpy as np
import pickle 


cam = cv2.VideoCapture(0)  # camera id
cam.set(3, 640)  # weidth
cam.set(4, 480)  # height
cam.set(10, 130)  # brightness


# cascade
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')


reconiger = cv2.face.LBPHFaceRecognizer_create()
reconiger.read("trainer.yml")

labels ={}
with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

while True:
    success, img = cam.read()
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayImg, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        # print(x,y,w,h)
        roigon_gray = grayImg[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        cv2.imwrite("cam_sface.png", roigon_gray)

        id_, conf = reconiger.predict(roigon_gray)
        if conf>=45:# and conf <=85:
            print(id_)
            print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (244,244,0)
            stroke =2
            cv2.putText(img, "acc="+str(int(conf))+ name, (x,y),font, 1, color, stroke, cv2.LINE_AA)

        color = (255, 0, 0)
        stroke =2
        cv2.rectangle(img, (x,y),(x+w, y+h), color, stroke)

        subItem = smile_cascade.detectMultiScale(roigon_gray)
        for (ex, ey, ew, eh) in subItem:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0),2)

    
    cv2.imshow("vide", img)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
        
cam.release()
cv2.destroyAllWindows()
