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
PersonAttend = apps.get_model('dashboard', 'PersonAttend')
PersonRegistration = apps.get_model('dashboard', 'PersonRegistration')

# Create engine for connecting to MySQL
engine = create_engine("mysql+pymysql://root:gil12345@localhost:3306/march")
# engine = create_engine("mysql+pymysql://root:Kor%40spond1@localhost:3306/face_full")

# Fetch data from MySQL
face_coding_query = "SELECT * FROM person_attend"
merged_df = pd.read_sql(face_coding_query, engine)
print(merged_df.columns)

# Insert data into MongoDB
for index, row in merged_df.iterrows():
    # Fetch the PersonRegistration instance
    person_instance = PersonRegistration.objects.filter(id=int(row["person_id"])).first()
    if person_instance:
        # Create a PersonAttend instance
        face = PersonAttend(
            id  = row["id"],
            person = person_instance,  # Assign the PersonRegistration instance
            face_feature = row["face_feature"], 
            blob_face_feature = row["blob_face_feature"],
            img_url = row["img_url"],
            camera_id  = row["camera_id"],
            time_sent = row["time_sent"],
            date_created = row["date_created"],
            T1 = row["T1"],
            T2 = row["T2"],
            T3 = row["T3"],
            score = row["score"],
            is_moved = row["is_moved"]
        )
        face.save()
