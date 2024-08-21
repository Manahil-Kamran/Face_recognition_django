import os
import psycopg2

# Database connection details
db_connection = psycopg2.connect(
    host="localhost",
    database="faceR",
    user="myuser",
    password="gil12345"
)

# Fetch IDs from the database
cursor = db_connection.cursor()
cursor.execute("SELECT id FROM dashboard_personregistration")  # Replace 'your_table' with your actual table name
db_ids = {str(row[0]) for row in cursor.fetchall()}  # Convert IDs to strings to match folder names
cursor.close()
db_connection.close()

# List the IDs in the dataset folders
dataset_folder_path = '/home/devp/dataset'  # Replace with the path to your dataset
dataset_ids = {folder_name for folder_name in os.listdir(dataset_folder_path) if folder_name.isdigit()}

# Find the extra IDs in the dataset not present in the database
extra_ids = dataset_ids - db_ids

# Print the extra IDs
print("Extra IDs not in the database:")
for id in extra_ids:
    print(id)
