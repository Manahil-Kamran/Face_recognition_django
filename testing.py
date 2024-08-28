# %%
from deepface import DeepFace
import os
import numpy as np
import cv2


# %%
dataset_path = "detection_models/images/"

# %%
images_array = []
for f in os.listdir(dataset_path):
    folder = os.path.join(dataset_path,f)
    for img in os.listdir(folder):
        # print(img)
        img = os.path.join(folder,img)
        img = cv2.imread(img)
        images_array.append(images_array)


# %%
len(images_array)

# %%
models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
  "GhostFaceNet",
]

embeddings = []
for img in images_array:
    #face recognition
    face = DeepFace.find(
                # img,
                img_path = np.array(img),
                db_path = "detection_models/images/1628", 
                model_name = models[1],
                detector_backend="opencv",
                enforce_detection=False
                )



# %%



