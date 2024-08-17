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

# Create engine for connecting to MySQL
engine = create_engine("mysql+pymysql://root:Kor%40spond1@localhost:3306/face_full")

# Fetch person_id and image_url from person_registration
face_coding_query = "SELECT * FROM person_registration"
merged_df = pd.read_sql(face_coding_query, engine)
print(merged_df)

# Insert data into MongoDB
for index, row in merged_df.iterrows():
    person = PersonRegistration(
        id=row["id"],
        full_name=row["full_name"],
        cnic=row["cnic"],
        department_name=row["department_name"],
        date_created=row["date_created"]
    )
    person.save()
