import os
import random
import numpy as np
import cv2
from PIL import Image
from django.utils.timezone import now
import warnings
from django.apps import apps
from deepface import DeepFace
# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configurations.settings')
import django
django.setup()

# Import your Django models
PersonRegistration = apps.get_model('dashboard', 'PersonRegistration')
FaceCoding = apps.get_model('dashboard', 'FaceCoding')
warnings.filterwarnings("ignore")
model_name = "OpenFace" # 1 ,1 ,1 , 1 , 1

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
        print(f"Processing image: {img_path} for employee ID: {employee_id}-------{img_path}")
        
        # Load the image using OpenCV
        image = cv2.imread(img_path)
        if image is None:
            print(f"Failed to load image {img_path}")
            continue

        embedding = DeepFace.represent(
                    img_path=image,
                    model_name=model_name,
                    detector_backend="yolov8",
                    enforce_detection=False)
        embedding=embedding[0]["embedding"]
        
        try:
            person = PersonRegistration.objects.get(id=employee_id)
        except PersonRegistration.DoesNotExist:
            print(f"Person with ID {employee_id} not found in PersonRegistration")
            continue

        # Save to FaceCoding model
        face_coding = FaceCoding(
            person=person,  # Assign the foreign key person
            face_feature=embedding,  # Store the face embedding
            img_url=img_path,  # Store the image URL
            date_created=now()  # Store current timestamp
        )
        face_coding.save()
        print(f"Saved embedding for employee ID: {employee_id} from image: {img_path}")
