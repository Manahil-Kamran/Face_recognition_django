from django.shortcuts import redirect, render
# from .socket_handlers import sio
import threading
import socketio
from .models import *


# sio = socketio.Server(async_mode='threading', cors_allowed_origins='*')
sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')

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


# def run_socketio_server():
#     # global model
#     # model = YOLO('best.pt')
#     app = socketio.WSGIApp(sio)
#     wsgi.server(eventlet.listen(('localhost', 8009)), app)