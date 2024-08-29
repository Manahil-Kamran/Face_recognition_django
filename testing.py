from deepface import DeepFace
import os
import numpy as np
import cv2
import random
from scipy.spatial import distance

dataset_path = "detection_models/images/"

images_array = []
ids_array = []

# Read and process all images
for f in os.listdir(dataset_path):
    folder = os.path.join(dataset_path, f)
    for img in os.listdir(folder):
        ids_array.append(f)
        img_path = os.path.join(folder, img)
        img = cv2.imread(img_path)
        # if not img:
        print(img_path)
            # break
        images_array.append((img, f))  # Store image with its id

# Choose the model
model_name = "Facenet"  # Change this to the desired model
# print(images_array)
embeddings = []
for img, img_id in images_array:
    # Extract face embedding
    print("img",img)
    embedding = DeepFace.represent(
        img_path=img,
        model_name=model_name,
        detector_backend="yolov8",
        enforce_detection=False
    )
    embeddings.append((embedding[0]["embedding"], img_id))
print(embeddings)
# Pick a random image
random_img, random_img_id = cv2.imread("detection_models/27597.jpg"),1630
random_img_embedding = DeepFace.represent(
    img_path=np.array(random_img),
    model_name=model_name,
    detector_backend="yolov8",
    enforce_detection=False
)[0]["embedding"]

# Find the closest match
min_dist = float('inf')
closest_img_id = None

for emb, img_id in embeddings:
    dist = distance.euclidean(random_img_embedding, emb)
    if dist < min_dist:
        min_dist = dist
        closest_img_id = img_id

print(f"Closest match ID: {closest_img_id}, Original random image ID: {random_img_id}")
