from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import time
import os
import urllib
import pickle
from collections import deque, Counter
import queue
from datetime import datetime
import cv2 
import base64
import socketio
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import time
import os
import cv2
import urllib
import requests, json
import pickle
from collections import deque
import torch
from model_utils.base import Resnet50
from model_utils.transform import make_transform
from deepface import DeepFace
from PIL import Image
import ast
from collections import deque, Counter



sio = socketio.Client()
q=queue.Queue()
# Load the custom face recognition model on CPU
model_name = "OpenFace"

base_url = "http://127.0.0.1:8000/"
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
thresholdfordetection = 0.5

def response(host):
    global res
    res = os.system(host)
    while res !=0:
        res = os.system(host)
        if res == 0: 
            return 0
    return res



def get_last_id_of_person():
    # print(base_url + 'api/max/person_registration/id')
    url = base_url + 'api/max/person_registration/id/'
    # print("Fetching unknown ID from the database ("+ url +")")
    with urllib.request.urlopen(url) as url:
        data = url.read().decode()
    return str(data)


def get_all_embeddings():
    URL = base_url + "dashboard/api/get_face_codings_testknn"

    with urllib.request.urlopen(URL) as url:
        data = json.loads(url.read().decode())
    #all_sig = []
    all_sig = deque()
    i = 0
    id_name = {}
    emp_data = []
    person_id = []
    for d in data:
        sig = d["face_feature"]
        p_id = d["person_id"]
        emp_data.append(d["person_name"] + "("+ d["department_name"] +")")
        # id_name = {d["person_name"] + "("+ d["department_name"] +")":p_id}
        id_name[p_id] = d["person_name"] + "("+ d["department_name"] +")"
        person_id.append(p_id)
        #all_sig.append(sig)
        all_sig.append(sig)
    print("all embeddings arrived",len(all_sig))
    return emp_data,all_sig,person_id,id_name

person_names, known_face_encodings, ids_for_person_ids, knn_id_n = get_all_embeddings()


def minkowski_distance(a, b, p):
    # return distance.euclidean(b, a)
    return np.power(np.sum(np.abs(np.array(a) - np.array(b))**p), 1/p)

def knn_classifier(unknown_encodings, known_face_encodings, ids_for_person_ids, k=3, p=2, threshold=0.9):
    distances = np.array([minkowski_distance(unknown_encodings, encoding, p) for encoding in known_face_encodings])
    # print("distance",distances)
    # print(ids_for_person_ids)
    # print(distances)
    filtered_indices = np.where(distances < threshold)
    # print(filtered_indices)
    filtered_distances = distances
    # print(filtered_distances)
    # [filtered_indices]    
    # print(filtered_indices)
    print(filtered_distances.any())
    if filtered_distances.any():
        try:
            closest_indices = np.argpartition(filtered_distances, k)[:k]
            closest_person_ids = [ids_for_person_ids[i] for i in filtered_indices[0][closest_indices]]
            person_id_counts = Counter(closest_person_ids)
            # print(person_id_counts)
            most_common_person_id, _ = person_id_counts.most_common(1)[0]
            print(most_common_person_id, "try condition")
           
            return most_common_person_id, filtered_distances[closest_indices]
        except:
            closest_indices = np.argpartition(distances, k)[:k]
            closest_person_ids = [ids_for_person_ids[i] for i in closest_indices]
            person_id_counts = Counter(closest_person_ids)
            # print(person_id_counts)
            most_common_person_id, _ = person_id_counts.most_common(1)[0]
            print(most_common_person_id, "excepion condition")
            
            return most_common_person_id, distances[closest_indices]
    else:
        return 'unknown', 0


from scipy.spatial import distance
def draw_label(image, point, label):
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    color = (0, 255, 0)  # Green color
    thickness = 1
    x, y = point
    cv2.putText(image, label, (x, y), font, scale, color, thickness, cv2.LINE_AA)

@sio.event
def connect():
    # res = response('ping 192.168.1.64 -c 4')  
    # if res == 0:

        # path = 'rtsp://admin:zohaib123@192.168.1.64:554/Streaming/channels/101/'
    path = 'detection_models/deepface1.mp4'
    cap = cv2.VideoCapture(path)
         
        # cap = VideoStream(src='rtsp://admin:zohaib123@192.168.1.64:554/Streaming/channels/101/', resolution=(640,480),
        # framerate=13).start()
    # else:
    #     # res = response('ping 192.168.1.64 -c 4')
    #     # if res == 0:
    #     #     res = 0

    # time.sleep(1.0)
    # fps = FPS().start()
    # size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # out_fps = 30

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    dep_name = "P&D"

    record_person = {} 
    time_for_wait = 1
    thread_index = 0
    res = 0
    while res == 0:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            continue

        if frame is not None:
            try:
                thread_index += 1
                face_embeddings = []
                face_names = []
                
                # Detect faces in the frame
                faces = DeepFace.extract_faces(np.array(frame), detector_backend="yolov8", enforce_detection=False)
                if not faces:
                    continue  # Skip to the next frame if no face is detected

                for face in faces:
                    face_img = face['face']  # Extract the face image array
                    if face_img.dtype != np.uint8:
                        # print("**************")
                        face_img = (face_img * 255).astype(np.uint8)
                    origin_h, origin_w = frame.shape[:2]
                    bounding_box = face['facial_area']
                    confidence = face['confidence']
                    # print("ret",confidence)    
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
                            # # Find the closest match
                            # min_dist = float('inf')
                            # closest_img_id = None
                            # check = []
                            # for idx,emb in enumerate(known_face_encodings):
                            #     print(type(emb))
                            #     dist = distance.euclidean(embeddings, emb)
                            #     check.append(dist)
                            # print(check)
                            # mins=min(check)
                            # closest_img_id=check.index(mins)
                            # Draw bounding box and label on the frame
                            x, y, w, h = bounding_box['x'], bounding_box['y'], bounding_box['w'], bounding_box['h']
                            predicted_class, closest_distances = knn_classifier(embeddings, known_face_encodings, ids_for_person_ids, k=3, p=2)
                            print(predicted_class,closest_distances)
                            # draw_label(frame, (x, y - 10), str(closest_img_id))
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            draw_label(frame, (x, y - 10), predicted_class)

                            # cv2.putText(frame, predicted_class, (15, int(origin_h * 0.92)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                            # cv2.imshow("testing",frame)

                        except Exception as e:
                            print('Error:', e)
                        
                        if face_img.any() and len(embeddings) > 0:
                            try:
                                if closest_distances != 0:
                                    label = '{0:.2f}%'.format(min(closest_distances) * 100)
                                    print(label)
                                else:
                                    label = 'High'
                            except:
                                if len(closest_distances) > 0:
                                    label = '{0:.2f}%'.format(min(closest_distances) * 100)
                                else:
                                    label = 'High'
                            if predicted_class !='unknown':
                                incoming_person_name = knn_id_n[predicted_class]
                            else:
                                incoming_person_name = 'unknown'
                            face_embeddings.append(embeddings)
                            face_names.append(incoming_person_name)
                            for name, fe, in zip(face_names, face_embeddings):
                                print(name)
                                # blob_fe = fe.tolist()
                                if name=="unknown":
                                    result, img_encoded = cv2.imencode('.jpg', face_img, encode_param)
                                    img_data = pickle.dumps(img_encoded, 0)                
                                    name_n = 'unknown--'+ str(get_last_id_of_person())+"-" + str(thread_index)
                                    meta_data = {'full_name': str(name_n), 'department_name': dep_name\
                                    , "face_feature": str(fe),  "blob_face_feature": fe, }
                                    my_img = {'image':img_data, 'json_data':meta_data}
                                    sio.emit('posting',my_img)
                                    name = 'unknown--'+ str(get_last_id_of_person())
                            
                                if name in list(record_person.keys()):
                                    if time.time() - record_person[name] > (time_for_wait * 60):
                                        result, img_encoded = cv2.imencode('.jpg', face_img, encode_param)
                                        img_data = pickle.dumps(img_encoded, 0)
                                        record_person[name] = time.time()
                                        if name in person_names:
                                            result, img_encoded = cv2.imencode('.jpg', face_img, encode_param)
                                            img_data = pickle.dumps(img_encoded, 0)
                                            from datetime import datetime
                                            now = datetime.now()                    
                                            meta_data = {'person_id': ids_for_person_ids[person_names.index(name)], 'camera_id': dep_name,
                                            "time_sent": str(now), "face_feature": str(fe),  "blob_face_feature": fe }
                                            my_img1 = {'image':img_data,'json_data':meta_data}
                                            sio.emit('attend',my_img1)
                                else:
                                    record_person[name] = time.time()
                                    if name in person_names:
                                        result, img_encoded = cv2.imencode('.jpg', face_img, encode_param)
                                        print(img_encoded, result)
                                        img_data = pickle.dumps(img_encoded, 0)
                                        from datetime import datetime
                                        now = datetime.now()
                                        meta_data = {'person_id':  ids_for_person_ids[person_names.index(name)], 'camera_id': dep_name,"time_sent": str(now)\
                                            , "face_feature": str(fe),  "blob_face_feature": fe }
                                        my_img1 = {'image':img_data,'json_data':meta_data}

                                        sio.emit('attend', my_img1)
            
                cv2.imshow('Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except Exception as e:
                print("error last",e)
#         else:
#             res = response('ping 192.168.1.64 -c 4')
#             if res == 0:
#                 res = 0
#                 cap = VideoStream(src='rtsp://admin:zohaib123@192.168.1.64:554/Streaming/channels/101/', resolution=(640,480), framerate=13).start()

cv2.destroyAllWindows()


  
  




@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://127.0.0.1:8009')
sio.wait()

                

                    
