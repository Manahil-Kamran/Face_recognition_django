from deepface import DeepFace
import os
import numpy as np
import cv2
from scipy.spatial import distance
# os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
# Load all embeddings from your dataset
dataset_path = "detection_models/images/"

images_array = []
ids_array = []
embeddings = []

# Read and process all images to compute embeddings
# model_name = "ArcFace"  # Change this to the desired model
# model_name = "SFace"
model_name = "OpenFace"
# model_name = "Facenet"
# model_name = "DeepID"



for f in os.listdir(dataset_path):
    folder = os.path.join(dataset_path, f)
    for img in os.listdir(folder):
        ids_array.append(f)
        img_path = os.path.join(folder, img)
        img = cv2.imread(img_path)
        images_array.append((img, f))  # Store image with its id

        # Extract face embedding
        embedding = DeepFace.represent(
            img_path=img,
            model_name=model_name,
            detector_backend="yolov8",
            enforce_detection=False
        )
        embeddings.append((embedding[0]["embedding"], f))

# Function to draw bounding box and label on the frame
def draw_label(image, point, label):
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    color = (0, 255, 0)  # Green color
    thickness = 1
    x, y = point
    cv2.putText(image, label, (x, y), font, scale, color, thickness, cv2.LINE_AA)

# Load video
video_path = "detection_models/deepface1.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect faces in the frame
    faces = DeepFace.extract_faces(np.array(frame), detector_backend="yolov8", enforce_detection=False)
    if not faces:
        continue  # Skip to the next frame if no face is detected

    for face in faces:
        face_img = face['face']  # Extract the face image array
        
        # Ensure the image has the correct data type
        if face_img.dtype != np.uint8:
            print("**************")
            face_img = (face_img * 255).astype(np.uint8)

        facial_area = face['facial_area']  # Extract the bounding box coordinates

        # Extract the embedding for the detected face
        face_embedding = DeepFace.represent(
            img_path=face_img,
            model_name=model_name,
            detector_backend="yolov8",
            enforce_detection=False
        )[0]["embedding"]
        
        # Find the closest match
        min_dist = float('inf')
        closest_img_id = None
        img_ids=[]
        check=[]
        for emb, img_id in embeddings:
            dist = distance.euclidean(face_embedding, emb)
            img_ids.append(img_id)
            check.append(dist)
            if dist < min_dist:
                min_dist = dist
                closest_img_id = img_id
        print(img_ids)
        print(check)
        # Draw bounding box and label on the frame
        x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
        draw_label(frame, (x, y - 10), closest_img_id)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.imshow(frame)

    # Display the frame
    cv2.imshow('Video', frame)
    
    # Press 'q' to exit the video loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
