import cv2
import numpy as np
import time
import urllib
import json
import pickle
from collections import deque, Counter
from deepface import DeepFace
from scipy.spatial import distance
import socketio
from datetime import datetime
# Initialize SocketIO client
sio = socketio.Client()

# Configuration variables
base_url = "http://127.0.0.1:8000/"
model_name = "Facenet512"
thresholdfordetection = 0.5

# Function to get the last ID of a person (used for assigning IDs to unknown individuals)
def get_last_id_of_person():
    url = base_url + 'api/max/person_registration/id/'
    with urllib.request.urlopen(url) as url:
        data = url.read().decode()
    return str(data)

# Function to retrieve all known face embeddings and corresponding IDs from the database
def get_all_embeddings():
    URL = base_url + "dashboard/api/get_face_codings_testknn"
    with urllib.request.urlopen(URL) as url:
        data = json.loads(url.read().decode())

    all_sig = deque()
    id_name = {}
    person_id = []
    person_names = []

    for d in data:
        sig = d["face_feature"]
        p_id = d["person_id"]
        person_names.append(d["person_name"] + "("+ d["department_name"] +")")
        id_name[p_id] = d["person_name"] + "("+ d["department_name"] +")"
        person_id.append(p_id)
        all_sig.append(sig)

    print("All embeddings loaded:", len(all_sig))
    return person_names, all_sig, person_id, id_name

# Load all known embeddings and corresponding IDs
person_names, known_face_encodings, ids_for_person_ids, knn_id_n = get_all_embeddings()

# Minkowski distance function
def minkowski_distance(a, b, p):
    return np.power(np.sum(np.abs(np.array(a) - np.array(b))**p), 1/p)

def calculate_distance(embedding1, embedding2):
    return np.linalg.norm(np.array(embedding1) - np.array(embedding2))

# def knn_classifier(embedding, registered_embeddings,ids_for_person_ids, threshold=0.5,k=3,p=2):
#     min_distance = float('inf')
#     closest_id = None
#     closest_ids=[]
#     for user_id, user_embedding in zip(ids_for_person_ids,registered_embeddings):
#         distance = calculate_distance(embedding, user_embedding)
#         if distance < min_distance:
#             closest_ids.append(user_id)
#             min_distance = distance
#             closest_id = user_id
#     # print(min_distance)
#     # return closest_id if min_distance <= threshold else 'unknown'
#     # if len(closest_ids):
#     print("closests ids",Counter(closest_ids))
#     if min_distance<=threshold:
#         return  closest_id,np.array([0])
#     else:
#         return "unknow",np.array([])
# KNN classifier for identifying the person
def knn_classifier(unknown_encodings, known_face_encodings, ids_for_person_ids, k=3, p=2, threshold=0.5):
    distances = np.array([minkowski_distance(unknown_encodings, encoding, p) for encoding in known_face_encodings])
    filtered_indices = np.where(distances > threshold)
    filtered_distances = distances
    # for idx,emb in enumerate(known_face_encodings):
    #     verify = DeepFace.verify(
    #         img1_path=unknown_encodings,
    #         img2_path=emb,
    #         threshold=0.4,
    #         model_name=model_name,
    #         detector_backend='yolov8',
    #         distance_metric = "euclidean",
    #         enforce_detection = False,
    #     )
    #     if verify['verified']:
    #         print(verify)
    #         return ids_for_person_ids[idx],np.array([verify['distance']])
    # return "unknow",np.array([0])
    if filtered_distances.any():
        try:
            closest_indices = np.argpartition(filtered_distances, k)[:k]
            closest_person_ids = [ids_for_person_ids[i] for i in filtered_indices[0][closest_indices]]
            person_id_counts = Counter(closest_person_ids)
            most_common_person_id, _ = person_id_counts.most_common(1)[0]
            return most_common_person_id, filtered_distances[closest_indices]
        except:
            closest_indices = np.argpartition(distances, k)[:k]
            closest_person_ids = [ids_for_person_ids[i] for i in closest_indices]
            person_id_counts = Counter(closest_person_ids)
            most_common_person_id, _ = person_id_counts.most_common(1)[0]
            return most_common_person_id, distances[closest_indices]
    else:
        print("#"*100)
        return 'unknown', 0
# # DeepFace.verify
# Function to draw a label on the frame
def draw_label(image, point, label):
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    color = (0, 255, 0)  # Green color
    thickness = 1
    x, y = point
    cv2.putText(image, label, (x, y), font, scale, color, thickness, cv2.LINE_AA)

# SocketIO event handling
@sio.event
def connect():
    path = '/home/devp/Videos/Recordings/2.mp4'  # Path to the video file
    cap = cv2.VideoCapture(path)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    dep_name = "P&D"

    record_person = {}
    time_for_wait = 1
    thread_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            continue

        if frame is not None:
            # try:
                thread_index += 1
                face_embeddings = []
                face_names = []

                # Detect faces in the frame
                faces = DeepFace.extract_faces(np.array(frame), detector_backend="yolov8", enforce_detection=False)
                if not faces:
                    continue  # Skip to the next frame if no face is detected

                for face in faces:
                    face_img = face['face']
                    if face_img.dtype != np.uint8:
                        face_img = (face_img * 255).astype(np.uint8)
                    bounding_box = face['facial_area']
                    confidence = face['confidence']

                    if confidence > thresholdfordetection:
                        try:
                            left = bounding_box['x']
                            top = bounding_box['y']
                            right = bounding_box['x'] + bounding_box['w']
                            bottom = bounding_box['y'] + bounding_box['h']
                            embeddings = DeepFace.represent(
                                img_path=face_img,
                                model_name=model_name,
                                detector_backend="yolov8",
                                enforce_detection=False
                            )[0]["embedding"]

                            x, y, w, h = bounding_box['x'], bounding_box['y'], bounding_box['w'], bounding_box['h']
                            predicted_class, closest_distances = knn_classifier(embeddings, known_face_encodings, ids_for_person_ids, k=3, p=2)
                            print(predicted_class,type(predicted_class))
                            print(closest_distances,type(closest_distances))
                            # print(predicted_class, closest_distances)

                            # Draw bounding box and label on the frame
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            draw_label(frame, (x, y - 10), predicted_class)

                        except Exception as e:
                            print('Error a:', e)

                        if face_img.any() and len(embeddings) > 0:
                            label = 'High'
                            if closest_distances.any():
                                label = '{0:.2f}%'.format(min(closest_distances) * 100)

                            incoming_person_name = knn_id_n.get(predicted_class, 'unknown')

                            face_embeddings.append(embeddings)
                            face_names.append(incoming_person_name)

                            for name, fe in zip(face_names, face_embeddings):
                                if name == "unknown":
                                    result, img_encoded = cv2.imencode('.jpg', face_img, encode_param)
                                    img_data = pickle.dumps(img_encoded, 0)
                                    name_n = 'unknown--'+ str(23)+"-" + str(thread_index)
                                    meta_data = {
                                        'full_name': str(name_n),
                                        'department_name': dep_name,
                                        "face_feature": fe,
                                        "blob_face_feature": fe,
                                    }
                                    my_img = {'image': img_data, 'json_data': meta_data}
                                    sio.emit('posting', my_img)
                                    name = name_n

                                if name in list(record_person.keys()):
                                    if time.time() - record_person[name] > (time_for_wait * 60):
                                        record_person[name] = time.time()
                                        if name in person_names:
                                            result, img_encoded = cv2.imencode('.jpg', face_img, encode_param)
                                            img_data = pickle.dumps(img_encoded, 0)
                                            now = datetime.now()
                                            meta_data = {
                                                'person_id': ids_for_person_ids[person_names.index(name)],
                                                'camera_id': dep_name,
                                                "time_sent": str(now),
                                                "face_feature": fe,
                                                "blob_face_feature": fe
                                            }
                                            my_img1 = {'image': img_data, 'json_data': meta_data}
                                            sio.emit('attend', my_img1)
                                else:
                                    record_person[name] = time.time()
                                    if name in person_names:
                                        result, img_encoded = cv2.imencode('.jpg', face_img, encode_param)
                                        img_data = pickle.dumps(img_encoded, 0)
                                        now = datetime.now()
                                        meta_data = {
                                            'person_id': ids_for_person_ids[person_names.index(name)],
                                            'camera_id': dep_name,
                                            "time_sent": str(now),
                                            "face_feature": fe,
                                            "blob_face_feature": fe
                                        }
                                        my_img1 = {'image': img_data, 'json_data': meta_data}
                                        sio.emit('attend', my_img1)

                cv2.imshow('Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            # except Exception as e:
            #     print("Error b:", e)

    cv2.destroyAllWindows()

@sio.event
def disconnect():
    print('Disconnected from server')

# Connect to the SocketIO server
sio.connect('http://127.0.0.1:8009')
sio.wait()
