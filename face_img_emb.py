import os
import gc
import psutil
import random
import numpy as np
import cv2
from PIL import Image
import torch
from utils.base import Resnet50
from utils.transform import make_transform
import pandas as pd  
import sqlalchemy 
from sqlalchemy import create_engine

from sqlalchemy.sql import text
import warnings
warnings.filterwarnings("ignore")


seed = 1
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed) 


process = psutil.Process(os.getpid())
print(f"Before torch.load: {process.memory_info().rss / 1e6:.2f} MB")

model = Resnet50(embedding_size=512)  

checkpoint = torch.load("/home/devp/Downloads/FR.pth", map_location=torch.device("cuda:0"))
model.load_state_dict(checkpoint['model_state_dict'])
model.eval() 
model.to(torch.device("cuda:0"))  
gc.collect()
print(f"After torch.load: {process.memory_info().rss / 1e6:.2f} MB")

# create engine for connecting sql
engine = create_engine("mysql+pymysql://root:gil12345@localhost:3306/new01")

# Fetch id from person_registration
person_registration_query = "SELECT id FROM person_registration"
person_registration_df = pd.read_sql(person_registration_query, engine)

# Fetch person_id and image_url from face_coding
face_coding_query = "SELECT person_id AS id, img_url FROM face_coding"
face_coding_df = pd.read_sql(face_coding_query, engine)
# Merge the DataFrames on the id column
merged_df = pd.merge(person_registration_df, face_coding_df, on='id', how='inner')

# Reset face_features column in the face_coding table
with engine.connect() as connection:
    try:
        connection.execute(text("UPDATE face_coding SET face_feature = NULL"))
    except Exception as e:
        print(f"An error occurred: {e}")

# Print merged DataFrame for debugging
print(merged_df)

# Iterate through the merged DataFrame and fetch image 
for index, row in merged_df.iterrows():
    image_url = row['img_url']
    image_path = "/home/devp/app_p/static/camera_img/"+image_url
    image = cv2.imread(image_path)
    print(image_path)
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    transform = make_transform()

    image = transform(image)

    image = image.unsqueeze(0)
    image = image.to(torch.device("cuda:0"))

    with torch.no_grad():
        output = model(image)

    output = output.cpu().numpy().tolist() 
    with engine.connect() as connection:
        update_query = text("""
            UPDATE face_coding
            SET face_feature = :face_features
            WHERE id = :id
        """)
        connection.execute(update_query, {"face_features": str(output), "id": row['id']})