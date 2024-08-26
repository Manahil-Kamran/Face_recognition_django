import csv
import os
import gc
import psutil
import random
import numpy as np
import cv2
from PIL import Image
import torch
from my_utils.base import Resnet50
from my_utils.transform import make_transform
from django.utils.timezone import now
import warnings
import psycopg2
import os
import pandas as pd  
from sqlalchemy import create_engine
from django.conf import settings
from django.apps import apps

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configurations.settings')
import django
django.setup()

# Import your Django models
PersonRegistration = apps.get_model('dashboard', 'PersonRegistration')
FaceCoding = apps.get_model('dashboard', 'FaceCoding')
warnings.filterwarnings("ignore")

# Set random seeds for reproducibility
seed = 1
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

# Monitor memory usage before loading the model
process = psutil.Process(os.getpid())
print(f"Before torch.load: {process.memory_info().rss / 1e6:.2f} MB")

# Load the face detection model (ResNet SSD)
prototxt_file = 'Resnet_SSD_deploy.prototxt'
caffemodel_file = 'Res10_300x300_SSD_iter_140000.caffemodel'
net = cv2.dnn.readNetFromCaffe(prototxt_file, caffemodel_file)
print('ResNetSSD caffe model loaded successfully')

# Load the ResNet50 model for face embedding extraction
model = Resnet50(embedding_size=512)
checkpoint = torch.load("/home/devp/Downloads/FR.pth", map_location=torch.device("cpu"))
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()  # Set the model to evaluation mode
model.to(torch.device("cpu"))  # Move the model to CPU
gc.collect()
print(f"After torch.load: {process.memory_info().rss / 1e6:.2f} MB")
# Directory containing the dataset
dataset_path = '/home/devp/dataset'
# Loop through each employee folder in the dataset
for employee_id in os.listdir(dataset_path):
    employee_folder = os.path.join(dataset_path, employee_id)
    
    if not os.path.isdir(employee_folder):
        continue  # Skip if it's not a directory

    # Get list of image file paths for the employee
    image_paths = [os.path.join(employee_folder, f) for f in os.listdir(employee_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Loop over each image for the current employee
    for img_path in image_paths:
        print(f"Processing image: {img_path} for employee ID: {employee_id}")
        
        # Load the image using OpenCV
        image = cv2.imread(img_path)
        if image is None:
            print(f"Failed to load image {img_path}")
            continue
        small_frame = cv2.resize(image, (0, 0), fx=0.65, fy=0.65, interpolation=cv2.INTER_AREA)
        origin_h, origin_w = small_frame.shape[:2]
        blob = cv2.dnn.blobFromImage(small_frame)
        net.setInput(blob)
        detections = net.forward()

        face_locations = []
        face_encodings = []
        face_names = []

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                bounding_box = detections[0, 0, i, 3:7] * np.array([origin_w, origin_h, origin_w, origin_h])
                left, top, right, bottom = bounding_box.astype('int')
                face_frame = np.ascontiguousarray(image[max(0, top-60):min(origin_h, bottom+60), max(0, left-60):min(origin_w, right+60)])
                
                pil_img = Image.fromarray(face_frame)
                transformed_img = make_transform(is_train=False)(pil_img).unsqueeze(0)  # Apply transformation

                # Extract embeddings from the model
                embedding = model(transformed_img).detach().cpu().numpy()[0]

            # (h, w) = image.shape[:2]

            # Prepare the image for face detection
        #     blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
        #     net.setInput(blob)
        #     detections = net.forward()

        # # Loop over the detections
        # for i in range(detections.shape[2]):
        #     confidence = detections[0, 0, i, 2]
            
        #     if confidence > 0.5:  # Filter out weak detections
        #         box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        #         (startX, startY, endX, endY) = box.astype("int")

        #         # Extract the detected face ROI
        #         face = image[startY:endY, startX:endX]

        #         # Convert the face ROI to RGB and then to a PIL Image
        #         face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        #         face = Image.fromarray(face)

        #         # Apply the necessary transformations to the face
        #         transform = make_transform()
        #         face = transform(face)

        #         # Add a batch dimension and move the tensor to the CPU
        #         face = face.unsqueeze(0)
        #         face = face.to(torch.device("cpu"))

        #         # Perform face embedding extraction
        #         with torch.no_grad():
        #             embedding = model(face).cpu().numpy().flatten()  # Flatten the embedding

                # Fetch the person object (foreign key) from PersonRegistration
                try:
                    person = PersonRegistration.objects.get(id=employee_id)
                except PersonRegistration.DoesNotExist:
                    print(f"Person with ID {employee_id} not found in PersonRegistration")
                    continue

                # Save to FaceCoding model
                face_coding = FaceCoding(
                    person=person,  # Assign the foreign key person
                    face_feature=embedding.tolist(),  # Store the face embedding
                    img_url=img_path,  # Store the image URL
                    date_created=now()  # Store current timestamp
                )
                face_coding.save()
                print(f"Saved embedding for employee ID: {employee_id} from image: {img_path}")
