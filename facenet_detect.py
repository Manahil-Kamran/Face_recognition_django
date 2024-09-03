from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import time
import os
import urllib
import requests, json
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
import cv2 as cv
import urllib
import requests, json
import pickle
from collections import deque
import torch
from my_utils.base import Resnet50
from my_utils.transform import make_transform

from PIL import Image
import ast
from collections import deque, Counter



sio = socketio.Client()
q=queue.Queue()
# Load the custom face recognition model on CPU
model = Resnet50(embedding_size=512)
checkpoint = torch.load("detection_models/FR.pth", map_location=torch.device("cpu"))
model.load_state_dict(checkpoint['model_state_dict'])
model.eval() 
model.to(torch.device("cpu"))
print("model loaded")



base_url = "http://127.0.0.1:8000/"
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep

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


def get_all_knn():
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
        
    return emp_data,all_sig,person_id,id_name

person_names, known_face_encodings, ids_for_person_ids, knn_id_n = get_all_knn()


def minkowski_distance(a, b, p):
    return np.power(np.sum(np.abs(np.array(a) - np.array(b))**p), 1/p)

def knn_classifier(unknown_encodings, known_face_encodings, ids_for_person_ids, k=3, p=2, threshold=0.5):
    distances = np.array([minkowski_distance(unknown_encodings, encoding, p) for encoding in known_face_encodings])
    # print(distances)
    filtered_indices = np.where(distances > threshold)
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
        print("*"*100)
        return 'unknown', 0

  
thresholdfordetection = 0.5  

prototxt_file = 'detection_models/Resnet_SSD_deploy.prototxt'
caffemodel_file =  'detection_models/Res10_300x300_SSD_iter_140000.caffemodel'
net = cv.dnn.readNetFromCaffe(prototxt_file, caffeModel=caffemodel_file)
print('ResNetSSD caffe model loaded successfully')


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
    # size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
    # out_fps = 30

    encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 90]
    dep_name = "P&D"

    record_person = {} 
    time_for_wait = 1
    thread_index = 0
    res = 0
    while res == 0:
        _,frame = cap.read()
        if frame is not None:    
            print("frame ",len(frame))

            thread_index +=1
            face_locations = []
            face_embeddings = []
            face_names = []
         
            small_frmae = cv2.resize(frame, (0,0),fx=0.65,fy=0.65, interpolation=cv2.INTER_AREA)

            origin_h, origin_w = small_frmae.shape[:2]
            blob = cv2.dnn.blobFromImage(small_frmae)
            net.setInput(blob)
            detections = net.forward()
            embedding = []
            for i in range(0, detections.shape[2]): #5
                confidence = detections[0, 0, i, 2]
                if confidence > thresholdfordetection:
                    try:
                        # Extract bounding box coordinates
                        bounding_box = detections[0, 0, i, 3:7]  # Normalized coordinates [x_min, y_min, x_max, y_max]
                        x_min, y_min, x_max, y_max = bounding_box

                        # Scale the coordinates to the image dimensions
                        left = int(x_min * origin_w)
                        top = int(y_min * origin_h)
                        right = int(x_max * origin_w)
                        bottom = int(y_max * origin_h)

                        # Ensure coordinates are within the image bounds
                        left, top = max(0, left - 60), max(0, top - 60)
                        right, bottom = min(origin_w, right + 60), min(origin_h, bottom + 60)
                        
                        # Crop the face frame from the image
                        face_frame = np.ascontiguousarray(frame[top:bottom, left:right])
                        
                        pil_img = Image.fromarray(face_frame)
                        transformed_img = make_transform(is_train=False)(pil_img).unsqueeze(0)  # Apply transformation

                        # Extract embeddings from the model
                        embeddings = model(transformed_img).detach().cpu().numpy()[0]

                        # Perform KNN classification
                        predicted_class, closest_distances = knn_classifier(embeddings, known_face_encodings, ids_for_person_ids, k=3, p=2)
                        print(predicted_class, closest_distances, "helloooo")

                        # Draw rectangle around the face
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        # Optionally, add text to the frame
                        name = ids_for_person_ids.index(predicted_class)
                        name = person_names[name]
                        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        
            
                        
                    except Exception as e:
                        print('Error',e)
            cv.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                    # label = None
                    # closest_distances = []
                    # incoming_person_name = None
                    
                    # if face_frame.any() and len(embeddings) > 0:
                    #     try: 
                    #         if closest_distances != 0:
                    #             label = '{0:.2f}%'.format(min(closest_distances) * 100)
                    #             print(label)
                    #         else:
                    #             label = 'High'
                    #     except: 
                    #         if len(closest_distances) > 0:
                    #             label = '{0:.2f}%'.format(min(closest_distances) * 100)
                    #         else:
                    #             label = 'High'
                    #     if predicted_class !='unknown':
                    #         incoming_person_name = knn_id_n[predicted_class]
                    #     else:
                    #         incoming_person_name = 'unknown'
                    #     face_embeddings.append(embeddings)
                    #     face_names.append(incoming_person_name)
                    #     for name, fe, in zip(face_names, face_embeddings):
                    #         print(name)
                            # blob_fe = fe.tolist()
                            # if name=="unknown":
                            #     result, img_encoded = cv.imencode('.jpg', face_frame, encode_param)
                            #     img_encoded_str = base64.b64encode(img_encoded).decode('utf-8')
                                               
                            #     name_n = 'unknown--'+ str(get_last_id_of_person())+"-" + str(thread_index)
                            #     meta_data = {'full_name': str(name_n), 'department_name': dep_name\
                            #     , "face_feature": str(fe),  "blob_face_feature": fe, }
                            #     my_img = { 'json_data':meta_data}
                            #     sio.emit('posting',img_encoded_str) 
                            #     name = 'unknown--'+ str(get_last_id_of_person())
                            
                            # if name in list(record_person.keys()):
                            #     if time.time() - record_person[name] > (time_for_wait * 60):
                            #         result, img_encoded = cv.imencode('.jpg', face_frame, encode_param)
                            #         img_data = pickle.dumps(img_encoded, 0)
                            #         record_person[name] = time.time()
                            #         if name in person_names:
                            #             result, img_encoded = cv.imencode('.jpg', face_frame, encode_param)
                            #             img_encoded_str = base64.b64encode(img_encoded).decode('utf-8')

                            #             # img_data = pickle.dumps(img_encoded, 0)
                            #             from datetime import datetime
                            #             now = datetime.now()                    
                            #             meta_data = {'person_id': ids_for_person_ids[person_names.index(name)], 'camera_id': dep_name,
                            #             "time_sent": str(now), "face_feature": str(fe),  "blob_face_feature": fe }
                            #             my_img1 = {'json_data':meta_data}
                            #             sio.emit('attend',my_img1)
                            # else:
                            #     record_person[name] = time.time()
                            #     if name in person_names:
                            #         import base64
                            #         result, img_encoded = cv.imencode('.jpg', face_frame, encode_param)
                            #         img_encoded_str = base64.b64encode(img_encoded).decode('utf-8')
                            #         print(img_encoded, result)
                            #         img_data = pickle.dumps(img_encoded_str, 0)
                            #         from datetime import datetime
                            #         now = datetime.now()
                            #         meta_data = {'person_id':  ids_for_person_ids[person_names.index(name)], 'camera_id': dep_name,"time_sent": str(now)\
                            #             , "face_feature": str(fe),  "blob_face_feature": fe }
                            #         my_img1 = {'json_data':meta_data}

                            #         sio.emit('attend', my_img1)
        else:
            print("^^^^^^^^^^^^^^^^^^^^6")
            res = response('ping 192.168.1.64 -c 4')
            if res ==0:
                res = 0
                print("#################################3")
                # path =  'rtsp://admin:zohaib123@192.168.1.64:554/Streaming/channels/101/'
                cap = VideoStream(src='rtsp://admin:zohaib123@192.168.1.64:554/Streaming/channels/101/', resolution=(640,480),
                framerate=13).start()

        #         x_start, y_start, x_end, y_end = bounding_box.astype('int')

        #         cv.rectangle(small_frmae, (x_start, y_start), (x_end, y_end),(0, 0, 255), 2)
                    
        #         cv.rectangle(small_frmae, (x_start, y_start-18), (x_end, y_start), (0, 0, 255), -1)
        #             # cv.putText(small_frmae, label, (x_start+2, y_start-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        #         cv.putText(small_frmae, name, (x_start+7, y_start-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        #     fps.update()
        #     fps.stop()
            # text = "FPS: {:.2f}".format(fps.fps())
           
        # cv2.imshow('Frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #             break
        #     # except Exception as e:
        #     #     print("Error b:", e)

    cv2.destroyAllWindows()
  
  




@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://127.0.0.1:8009')
sio.wait()

                

                    
