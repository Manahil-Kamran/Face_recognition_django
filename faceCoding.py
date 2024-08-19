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
FaceCoding = apps.get_model('dashboard', 'FaceCoding')
PersonRegistration = apps.get_model('dashboard', 'PersonRegistration')

# Create engine for connecting to MySQL
engine = create_engine("mysql+pymysql://root:gil12345@localhost:3306/new01")
# engine = create_engine("mysql+pymysql://root:Kor%40spond1@localhost:3306/face_full")

# Fetch person_id and image_url from face_coding
face_coding_query = "SELECT * FROM face_coding"
merged_df = pd.read_sql(face_coding_query, engine)
print(merged_df.columns)

# Insert data into MongoDB
for index, row in merged_df.iterrows():
    person_instance = PersonRegistration.objects.filter(id=int(row["person_id"])).first()
    if person_instance:
        face = FaceCoding(
            id = row["id"],
            person = person_instance,
            face_feature = row["face_feature"], 
            blob_face_feature = row["blob_face_feature"],
            img_url =row["img_url"],
            is_current = row["is_current"],
            time_sent = row["time_sent"],
            date_created = row["date_created"]
        )
        face.save()

