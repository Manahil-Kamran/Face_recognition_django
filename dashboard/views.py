from django.shortcuts import redirect, render
# from .socket_handlers import sio
import threading
import socketio
from .models import *
import cv2
import pickle
import numpy as np
import os
# sio = socketio.Server(async_mode='threading', cors_allowed_origins='*')
sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
mypath2="media/attend_img"
# sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
# redis_host = 'localhost'  # Redis server host
# redis_port = 6379  # Redis server port
# redis_client = redis.Redis(host='localhost', port=6379, db=0)
# threading_dict = {}
# vehicle_counting_dict = {}



def Main_Dashboard(request):
    if request.method == "GET":
        template_name = "dashboard/index.html"
    if request.method == "POST":
        template_name = "dashboard/index.html"
    return render(request, template_name)

def run_socketio_server():
    from eventlet import wsgi
    import eventlet
    app = socketio.WSGIApp(sio)
    wsgi.server(eventlet.listen(('localhost', 8009)), app)


@sio.on('connect')
def on_connect(sid, environ):
    print('Client connected:', sid)


# Define an event handler for the 'disconnect' event
@sio.on('disconnect')
def on_disconnect(sid):
    print('Client disconnected:', sid)
    # send disconect message to client
    sio.emit('disconnect',sid)

@sio.on('attend')
def attend(sid,data):
    ## Reading Image
    # f = request.files['image']
    # json_data = request.files['json_data']
    pictures = data['image']
    json_data = data['json_data']
    img_data = pickle.loads(pictures, fix_imports=True, encoding="bytes")
    img_data = cv2.imdecode(img_data, cv2.IMREAD_COLOR)

    print("_________Attend____________")
    # print(json_data)
    #meta_data = json.load(json_data)
    meta_data = json_data
    print('_________meta______')
    #print(json_data[0])
    c_data=PersonAttend.objects.create(
        person_id=meta_data['person_id'],
        camera_id = meta_data['camera_id'], time_sent=meta_data["time_sent"],
                        face_feature=meta_data["face_feature"],
                        blob_face_feature=np.ndarray.dumps(np.array(meta_data["blob_face_feature"])))
    
    ## Get ID of person Data
    c_id = c_data.id
    print('______CID_______')
    ## Storing the pic
    # f.save(os.path.join(
    #     current_app.config['UPLOAD_FOLDER2'], str(c_id) + ".jpg"))
    cv2.imwrite(os.path.join(mypath2, str(c_id) + ".jpg"), img_data)

    c_data.img_url = str(c_id) + ".jpg"
    


# def run_socketio_server():
#     # global model
#     # model = YOLO('best.pt')
#     app = socketio.WSGIApp(sio)
#     wsgi.server(eventlet.listen(('localhost', 8009)), app)