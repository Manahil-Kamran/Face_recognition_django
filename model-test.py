from imutils.video import FPS
import numpy as np
import time
import os
import urllib
import requests, json
import pickle
from collections import deque, Counter
import torch
from my_utils.base import Resnet50
from my_utils.transform import make_transform
import cv2 as cv
from PIL import Image
from collections import deque, Counter
import socketio
import queue
import ast

# SocketIO setup
sio = socketio.Client()
q = queue.Queue()

# Load custom face recognition model on CPU
model = Resnet50(embedding_size=512)
checkpoint = torch.load("/home/devp/Downloads/FR.pth", map_location=torch.device("cpu"))
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()
model.to(torch.device("cpu"))
print("Model loaded")

base_url = "http://127.0.0.1:8000/"
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep

# SSD model loading
prototxt_file = file_path + 'Resnet_SSD_deploy.prototxt'
caffemodel_file = file_path + 'Res10_300x300_SSD_iter_140000.caffemodel'
net = cv.dnn.readNetFromCaffe(prototxt_file, caffeModel=caffemodel_file)
print('ResNetSSD model loaded successfully')

# Video path
path = '/home/devp/Videos/90.mp4'
cap = cv.VideoCapture(path)


def get_all_knn():
    URL = base_url + "dashboard/api/get_face_codings_testknn"

    with urllib.request.urlopen(URL) as url:
        data = json.loads(url.read().decode())
        

    all_sig = deque()
    id_name = {}
    emp_data = []
    person_id = []

    for d in data:
        sig = d["face_feature"]
        p_id = d["person_id"]
        emp_data.append(d["person_name"] + "("+ d["department_name"] +")")
        id_name[p_id] = d["person_name"] + "("+ d["department_name"] +")"
        person_id.append(p_id)
        all_sig.append(sig)

    return emp_data, all_sig, person_id, id_name

# Load KNN data
person_names, known_face_encodings, ids_for_person_ids, knn_id_n = get_all_knn()

def minkowski_distance(a, b, p):
    # Convert both arrays to float for numeric operations
    a = np.array(a, dtype=np.float32)
    
    b = np.array(b, dtype=np.float32)
   
    
    # Calculate Minkowski distance
    distance=np.power(np.sum(np.abs(a - b)**p), 1/p)
    
    return distance

 # KNN classifier implementation
def knn_classifier(unknown_encodings, known_face_encodings, ids_for_person_ids, k=3, p=2, threshold=0.5):
    distances = np.array([minkowski_distance(unknown_encodings, ast.literal_eval(encoding), p) for encoding in known_face_encodings])
    print(distances)
    filtered_indices = np.where(distances < threshold)
    filtered_distances = distances
    [filtered_indices]
    

    

    
    if filtered_distances.any():
        try:
            closest_indices = np.argpartition(filtered_distances, k)[:k]
            closest_person_ids = [ids_for_person_ids[i] for i in filtered_indices[0][closest_indices]]
            person_id_counts = Counter(closest_person_ids)
            most_common_person_id, _ = person_id_counts.most_common(1)[0]
            print(most_common_person_id, "try condition")
           
            return most_common_person_id, filtered_distances[closest_indices]
        except:
            closest_indices = np.argpartition(distances, k)[:k]
            closest_person_ids = [ids_for_person_ids[i] for i in closest_indices]
            person_id_counts = Counter(closest_person_ids)
            most_common_person_id, _ = person_id_counts.most_common(1)[0]
            print(most_common_person_id, "except6 condition")
            
            return most_common_person_id, distances[closest_indices]
    else:
        return 'unknown', 0


# fps = FPS().start()  # Start FPS counter

# Face detection and recognition process
thresholdfordetection = 0.5
fps = FPS().start()  # Start FPS counter

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    small_frame = cv.resize(frame, (0, 0), fx=0.65, fy=0.65, interpolation=cv.INTER_AREA)
    origin_h, origin_w = small_frame.shape[:2]
    blob = cv.dnn.blobFromImage(small_frame)
    net.setInput(blob)
    detections = net.forward()

    face_locations = []
    face_encodings = []
    face_names = []

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > thresholdfordetection:
            bounding_box = detections[0, 0, i, 3:7] * np.array([origin_w, origin_h, origin_w, origin_h])
            left, top, right, bottom = bounding_box.astype('int')
            face_frame = np.ascontiguousarray(frame[max(0, top-60):min(origin_h, bottom+60), max(0, left-60):min(origin_w, right+60)])
            
            pil_img = Image.fromarray(face_frame)
            transformed_img = make_transform(is_train=False)(pil_img).unsqueeze(0)  # Apply transformation

            # Extract embeddings from the model
            embedding = model(transformed_img).detach().cpu().numpy()[0]
            # print(embedding)
            # print(embedding.shape)
            # print(type(embedding))
          
            face_locations.append((left, top, right, bottom))
            face_encodings.append(embedding)

            # Use KNN to classify the face
            person_id, _ = knn_classifier(embedding, known_face_encodings, ids_for_person_ids)
            print(person_id)
            predicted_class = knn_id_n.get(person_id, "Unknown")
            print(person_id,predicted_class)
            # Draw bounding box and label on the imageqqq
            cv.rectangle(small_frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv.putText(small_frame, predicted_class, (left, top-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     small_frame = cv.resize(frame, (0, 0), fx=0.65, fy=0.65, interpolation=cv.INTER_AREA)
#     origin_h, origin_w = small_frame.shape[:2]
#     blob = cv.dnn.blobFromImage(small_frame)
#     net.setInput(blob)
#     detections = net.forward()

#     face_locations = []
#     face_encodings = []
#     face_names = []

#     for i in range(0, detections.shape[2]):
#         confidence = detections[0, 0, i, 2]
#         if confidence > thresholdfordetection:
#             bounding_box = detections[0, 0, i, 3:7] * np.array([origin_w, origin_h, origin_w, origin_h])
#             left, top, right, bottom = bounding_box.astype('int')
#             face_frame = np.ascontiguousarray(frame[max(0, top-60):min(origin_h, bottom+60), max(0, left-60):min(origin_w, right+60)])
            
#             pil_img = Image.fromarray(face_frame)
#             transformed_img = make_transform(pil_img).unsqueeze(0)
#             embedding = model(transformed_img).detach().cpu().numpy()[0]

#             face_locations.append((left, top, right, bottom))
#             face_encodings.append(embedding)

#             # Use KNN to classify the face
#             person_id, _ = knn_classifier(embedding, known_face_encodings, ids_for_person_ids)
#             predicted_class = knn_id_n.get(person_id, "Unknown")

#             # Draw bounding box and label on the image
#             cv.rectangle(small_frame, (left, top), (right, bottom), (0, 0, 255), 2)
#             cv.putText(small_frame, predicted_class, (left, top-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

#     # Update FPS counter
  
    fps.update()  # Update FPS counter


    # Display FPS on the frame

    fps.stop()  # Stop FPS counter

    # Display FPS on the frame
    text = "FPS: {:.2f}".format(fps.fps())
    cv.putText(small_frame, text, (15, int(origin_h * 0.92)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv.imshow('Frame', small_frame)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# Stop the FPS counter and release resources
# fps.stop()
print("Elapsed time: {:.2f}".format(fps.elapsed()))
print("FPS: {:.2f}".format(fps.fps()))

cap.release()
cv.destroyAllWindows()