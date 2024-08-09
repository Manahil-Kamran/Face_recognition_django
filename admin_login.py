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
AdminLogin = apps.get_model('dashboard', 'AdminLogin')

# Create engine for connecting to MySQL
engine = create_engine("mysql+pymysql://root:gil12345@localhost:3306/new01")

# Fetch person_id and image_url from person_registration
face_coding_query = "SELECT * FROM admin_login"
merged_df = pd.read_sql(face_coding_query, engine)
print(merged_df)

# # Insert data into MongoDB
for index, row in merged_df.iterrows():
    admin = AdminLogin(
        id = row["id"],
        username = row["username"],
        email = row["email"],
        password =row["password"],
        is_active = row["is_active"],
        avatar_url = row["avatar_url"],
        created_by = row["created_by"],
        date_created = row["date_created"],
    )
    admin.save()
