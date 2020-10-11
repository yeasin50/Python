import os
from PIL import Image
import numpy as np
import cv2
import pickle 

# cascade
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(BASE_DIR, "images")

currrent_id = 0
label_ids = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(img_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("JPG"):
            path = os.path.join(root, file)
            label = os.path.basename(os.path.dirname(path)).replace(" ","-").lower()
            # print(label)

            if not label in label_ids:
                label_ids[label] = currrent_id
                currrent_id +=1
            id_ = label_ids[label]
            # print(label_ids)

            pil_img =  Image.open(path).convert("L") # L convert into gray
            size = (550,550)
            final_img = pil_img.resize(size, Image.ANTIALIAS)
            img_array = np.array(final_img, "uint8")
            # print(img_array)

            faces = face_cascade.detectMultiScale(img_array, scaleFactor=1.5,minNeighbors=5)

            for (x, y, w, h) in faces:
                roign = img_array[y:y+h, x:x+w]
                x_train.append(roign)
                y_labels.append(id_)

# print(y_labels, x_train)

with open("labels.pickle", 'wb') as f:
    pickle.dump(label_ids, f)

reconiger = cv2.face.LBPHFaceRecognizer_create()
reconiger.train(x_train, np.array(y_labels))
reconiger.save("trainer.yml")
